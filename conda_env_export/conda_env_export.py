"""Main module."""
import os
import sys
from collections import OrderedDict
from itertools import chain
from subprocess import Popen, PIPE

import click
import yaml

from pip._internal.utils.misc import get_installed_distributions

from importlib import import_module

flatten = chain.from_iterable


def _dict_representer(dumper, data):
    return dumper.represent_mapping(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        data.items())


class CustomDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(CustomDumper, self).increase_indent(flow, False)


CustomDumper.add_representer(OrderedDict, _dict_representer)


class Node(object):

    def __init__(self, key, version):
        self.key = key
        self.version = version

    def __hash__(self):
        return hash(str(self))


class CondaNode(Node):

    def __init__(self, key, version, channel):
        super(CondaNode, self).__init__(key, version)
        self.channel = channel

    def __str__(self):
        return '='.join(filter(lambda x: x, [self.key, self.version]))


class PipNode(Node):

    def __init__(self, key, version, project_name=None):
        super(PipNode, self).__init__(key, version)
        self.project_name = project_name

    def __str__(self):
        return '=='.join([self.project_name, self.version])


class CondaEnvExport(object):

    def __init__(self):
        self.name = 'conda-env-export'

    @property
    def is_windows(self):
        return sys.platform == 'win32'

    def call_cmd(self, cmd, extra_args):
        cmd_list = [cmd]
        cmd_list.extend(extra_args)
        try:
            p = Popen(cmd_list, shell=self.is_windows, stdout=PIPE, stderr=PIPE)
        except OSError:
            raise Exception("could not invoke %r\n", cmd_list)
        return p.communicate()

    def get_env_name(self):
        return os.getenv('CONDA_DEFAULT_ENV')

    def get_python_path(self, name=None):
        if name:
            prefix = self.get_conda_prefix(name)
            if self.is_windows:
                cmd = os.path.join(prefix, 'python')
            else:
                cmd = os.path.join(prefix, 'bin/python')
        else:
            cmd = os.getenv('CONDA_PYTHON_EXE')
        return cmd

    def get_current_conda(self):
        return os.getenv('CONDA_EXE')

    def locate_prefix(self, name):
        cmd = self.get_current_conda()
        args = ['env', 'list']
        stdout, stderr = self.call_cmd(cmd, args)
        data = stdout.decode()
        data = list(filter(lambda x: x.startswith(name), data.split('\n')))
        if data:
            prefix = data[0][len(name):].strip().replace('*', '').strip()
        else:
            prefix = None
        return prefix

    def get_conda_prefix(self, name=None):
        if name and name != self.get_env_name():
            prefix = self.locate_prefix(name)
        else:
            prefix = os.getenv('CONDA_PREFIX')
        return prefix

    def get_pip_paths(self, name, conda_prefix):
        cmd = self.get_python_path(name)
        args = ['-c', "import sys;print(';'.join(sys.path))"]
        stdout, stderr = self.call_cmd(cmd, args)
        data = stdout.decode()
        paths = list(map(lambda x: x.strip(), data.split(';')))
        # filter by env prefix
        paths = list(filter(lambda x: x.startswith(conda_prefix), paths))
        return paths

    def get_python_version(self, name):
        cmd = self.get_python_path(name)
        args = ['-c', "import sys; print(sys.version[: sys.version.index(' ')])"]
        stdout, stderr = self.call_cmd(cmd, args)
        data = stdout.decode().strip()
        return data

    def get_pip_deps(self, paths, all=False, include=(), exclude=()):
        def guess_version(key):
            default = None
            try:
                m = import_module(key)
            except:
                return default
            else:
                return getattr(m, '__version__', default)

        pkgs = get_installed_distributions(paths=paths)
        nodes = {}
        for pkg in pkgs:
            key = pkg.key
            version = pkg.version
            deps = pkg.requires()
            children = {}
            for dep in deps:
                k = dep.key
                # version
                specs = dep.specs
                specs = sorted(specs, reverse=True)
                v = ','.join([''.join(sp) for sp in specs]) if specs else None
                v = v if v else guess_version(k)
                children[k] = v
            node = PipNode(key, version, project_name=pkg.project_name)
            nodes[node] = children
        if not all:
            branch_keys = set(r for r in flatten(nodes.values()))
            nodes = [p for p in nodes if p.key not in branch_keys or p.project_name.lower() in include]
            nodes = [p for p in nodes if p.project_name.lower() not in exclude]
        nodes = sorted(nodes, key=lambda x: x.project_name.lower())
        return nodes

    def get_conda_deps(self, name, prefix, all=False, include=(), exclude=()):
        if not self.is_windows:
            base_sp_path = self.get_base_sp_path()
            sys.path.insert(0, base_sp_path)
        import conda.exports
        cache = conda.exports.linked_data(prefix=prefix)
        nodes = {}
        python_str = 'python'
        # for Windows
        found_python = False
        for k in cache.keys():
            n = cache[k]['name']
            v = cache[k]['version']
            c = cache[k]['schannel']
            deps = cache[k]['depends']
            children = {}
            for dep in deps:
                n2 = dep.split(' ')[0]
                v2 = dep.split(' ')[1:]
                children[n2] = v2
            node = CondaNode(n, v, c)
            nodes[node] = children

            if not found_python and n.lower() == python_str:
                found_python = True

        # add python if not exists
        if not found_python:
            python_node = CondaNode(python_str, self.get_python_version(name), '')
            nodes[python_node] = {}

        if not all:
            branch_keys = set(r for r in flatten(nodes.values()))
            nodes = [p for p in nodes if p.key not in branch_keys or p.key.lower() == python_str
                     or p.key.lower() in include]
            nodes = [p for p in nodes if p.key.lower() not in exclude]

        nodes = sorted(nodes, key=lambda x: x.key.lower())
        return nodes

    def make_yml(self, conda_nodes, pip_nodes, prefix, name, remove_duplicates=True, no_prefix=False):
        if remove_duplicates:
            # remove duplicates between conda and pip
            conda_keys = set(map(lambda x: x.key, conda_nodes))
            pip_nodes = [n for n in pip_nodes if n.project_name not in conda_keys]

        func = lambda x: [str(n) for n in x]
        conda_deps = func(conda_nodes)
        pip_deps = func(pip_nodes)

        dict = OrderedDict()
        dict['name'] = name
        dict['channels'] = sorted(filter(lambda x: len(x), set(map(lambda x: x.channel, conda_nodes))))

        deps = conda_deps + [{'pip': pip_deps}]
        dict['dependencies'] = deps
        if not no_prefix:
            dict['prefix'] = prefix
        return dict, pip_deps

    def get_base_sp_path(self):
        cmd = self.get_python_path('base')
        args = ['-c', "import os;print(os.path.dirname(os.__file__))"]
        stdout, stderr = self.call_cmd(cmd, args)
        data = os.path.join(stdout.decode().strip(), 'site-packages')
        return data

    def check(self, name=None):

        def _check(name, func, *args):
            click.secho('Checking %s......' % name, fg='white')
            path = func(*args)
            assert path, click.secho('Failed', fg='red')
            click.secho(path, fg='green')

        def _check_package_by_conda_cmd(package_name):
            cmd = self.get_current_conda()
            args = ['list', '-f', package_name]
            stdout, stderr = self.call_cmd(cmd, args)
            output = stdout.decode().split()
            matched = list(filter(lambda x: x.startswith(package_name), output))
            return matched and len(matched) > 0

        def _check_and_try_installing(package_name, install_cmd, install_args):
            click.secho('Checking package %s......' % package_name, fg='white')
            matched = _check_package_by_conda_cmd(package_name)
            if not matched:
                click.secho('Not found %s, try to install automatically...' % package_name, fg='yellow')
                _, _ = self.call_cmd(install_cmd, install_args)
                # check again
                matched = _check_package_by_conda_cmd(package_name)
                assert matched, \
                    click.secho('Failed to install %s, please install it manually' % package_name)
                click.secho('Installing %s is done' % package_name, fg='green')
            else:
                click.secho('Found %s' % package_name, fg='green')

        def check_menuinst():
            if self.is_windows:
                package_name = 'menuinst'
                install_cmd = self.get_current_conda()
                install_args = ['install', '-c', 'anaconda', package_name, '-q', '-y']
                _check_and_try_installing(package_name, install_cmd, install_args)

        def check_pip_conda():
            if self.is_windows:
                package_name = 'conda'
                install_cmd = 'pip'
                install_args = ['install', package_name, '-q']
                _check_and_try_installing(package_name, install_cmd, install_args)
                # For windows, the new installed conda will conflict with the default conda.
                # It means that conda command will fail when executing.
                # To fix this, just to remove the new installed conda locating in {prefix}/Scripts/
                new_conda_exe_file = os.path.join(self.get_conda_prefix(name), 'Scripts/conda.exe')
                if os.path.exists(new_conda_exe_file):
                    os.remove(new_conda_exe_file)

        _check('conda', self.get_current_conda)
        # menuinst is a package managed by conda, it's required in windows
        check_menuinst()
        # conda is required in windows
        check_pip_conda()
        _check('conda prefix', self.get_conda_prefix, name)
        _check('conda base site-packages', self.get_base_sp_path)
        _check('python', self.get_python_path, name)

    def run(self, name=None, conda_all=False, pip_all=False, remove_duplicates=True,
            include=(), exclude=(), extra_pip_requirements=False, no_prefix=False):

        click.secho('Exporting......', fg='white')
        try:
            name = name or self.get_env_name()
            conda_prefix = self.get_conda_prefix(name)
            conda_nodes = self.get_conda_deps(name, conda_prefix, all=conda_all, include=include, exclude=exclude)
            pip_paths = self.get_pip_paths(name, conda_prefix)
            pip_nodes = self.get_pip_deps(pip_paths, all=pip_all, include=include, exclude=exclude)
            data, pip_data = self.make_yml(conda_nodes, pip_nodes, conda_prefix, name,
                                           remove_duplicates=remove_duplicates, no_prefix=no_prefix)

            filename = '%s.yml' % name
            with open(filename, 'w') as f:
                yaml.dump(data, f, Dumper=CustomDumper)
            click.secho('Done. Saved to ./%s.' % filename, fg='green')
            if extra_pip_requirements:
                filename = 'requirements.txt'
                with open(filename, 'w') as f:
                    f.write('\n'.join(pip_data))
                click.secho('Done. Saved an extra ./%s.' % filename, fg='green')
        except:
            import traceback
            click.secho(traceback.format_exc(), fg='red')
