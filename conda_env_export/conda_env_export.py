"""Main module."""
import os
from collections import OrderedDict
from subprocess import Popen, PIPE

import click
import yaml


def _dict_representer(dumper, data):
    return dumper.represent_mapping(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        data.items())


class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


MyDumper.add_representer(OrderedDict, _dict_representer)


class CondaEnvExport(object):

    def __init__(self):
        self.conda_path = None
        self.env_prefix = None
        self.python_path = None
        self.name = 'conda-env-export'

    def call_cmd(self, cmd, extra_args):
        cmd_list = [cmd]
        cmd_list.extend(extra_args)
        try:
            p = Popen(cmd_list, stdout=PIPE, stderr=PIPE)
        except OSError:
            raise Exception("could not invoke %r\n", cmd_list)
        return p.communicate()

    def drop_duplicates(self, conda_deps, pip_deps):
        # remove duplicates between conda and pip
        conda_deps = list(
            map(lambda x: x.split('=')[0].replace('_', '-').upper(), filter(lambda x: isinstance(x, str), conda_deps)))
        pip_deps = {x.split('==')[0].replace('_', '-').upper(): x for x in pip_deps}
        diff_keys = set(pip_deps.keys()).difference(conda_deps)
        pip_deps = list(map(lambda x: pip_deps[x], diff_keys))
        return pip_deps

    def get_env_name(self):
        return os.getenv('CONDA_DEFAULT_ENV')

    def get_current_python(self, name=None):
        if name:
            prefix = self.get_conda_prefix(name)
            cmd = os.path.join(prefix, 'bin/python')
        else:
            cmd = os.getenv('CONDA_PYTHON_EXE')
        return cmd

    def get_current_conda(self):
        return os.getenv('CONDA_EXE')

    def remove_self(self, pip_deps):
        name = self.name
        pip_deps = list(filter(lambda x: not x.startswith(name), pip_deps))
        return pip_deps

    def merge_data(self, conda_data, pip_data):
        dep_key = 'dependencies'
        conda_dict = OrderedDict(yaml.load(conda_data, Loader=yaml.FullLoader))
        deps = conda_dict[dep_key]
        # find pip dict
        pip_dicts = list(filter(lambda x: isinstance(x, dict) and 'pip' in x, deps))
        pip_data = pip_data.strip().split('\n')
        if pip_dicts:
            pip_dict = list(pip_dicts[0].values())[0]
            pip_deps = set(pip_dict).union(pip_data)
        else:
            pip_deps = pip_data
        pip_deps = self.drop_duplicates(deps, pip_deps)
        pip_deps = self.remove_self(pip_deps)
        # sort
        pip_deps = sorted(pip_deps, key=lambda x: x[0].lower())
        # replace in source conda data
        if isinstance(deps[-1], dict) and 'pip' in deps[-1]:
            deps[-1]['pip'] = pip_deps
        else:
            deps.append(dict(pip=pip_deps))

        conda_dict[dep_key] = deps
        return conda_dict

    def locate_prefix(self, name):
        cmd = self.get_current_conda()
        args = ['env', 'list']
        stdout, stderr = self.call_cmd(cmd, args)
        data = stdout.decode()
        data = list(filter(lambda x: x.startswith(name), data.split('\n')))
        if data:
            prefix = data[0][len(name):].strip()
        else:
            prefix = None
        return prefix

    def get_conda_prefix(self, name=None):
        if name and name != self.get_env_name():
            prefix = self.locate_prefix(name)
        else:
            prefix = os.getenv('CONDA_PREFIX')
        return prefix

    def pip_list(self, name=None):
        cmd = self.python_path or self.get_current_python(name)
        args = ['-m', 'pip', 'list', '--format=freeze']
        stdout, stderr = self.call_cmd(cmd, args)
        data = stdout.decode()
        return data

    def conda_export(self, name=None):
        cmd = self.conda_path or self.get_current_conda()
        env = name or self.get_env_name()
        args = ['env', 'export', '-n', env, '--no-builds']
        stdout, stderr = self.call_cmd(cmd, args)
        data = stdout.decode()
        return data

    def check_and_run(self, name=None):
        click.secho('Checking conda......', fg='white')
        self.conda_path = self.get_current_conda()
        assert self.conda_path, click.secho('Failed', fg='red')
        click.secho(self.conda_path, fg='green')

        click.secho('Checking env prefix......', fg='white')
        self.env_prefix = self.get_conda_prefix(name)
        assert self.env_prefix, click.secho('Failed', fg='red')
        click.secho(self.env_prefix, fg='green')

        click.secho('Checking python python......', fg='white')
        self.python_path = self.get_current_python(name)
        assert self.python_path, click.secho('Failed', fg='red')
        click.secho(self.python_path, fg='green')

        click.secho('Exporting......', fg='white')
        try:
            filename = self.run(name)
            click.secho('Done. Saved to ./%s.' % filename, fg='green')
        except:
            import traceback
            click.secho(traceback.format_exc(), fg='red')

    def run(self, name=None):
        name = name or self.get_env_name()
        conda_data = self.conda_export(name)
        pip_data = self.pip_list(name)
        data = self.merge_data(conda_data, pip_data)
        filename = '%s.yml' % name
        with open(filename, 'w') as f:
            yaml.dump(data, f, Dumper=MyDumper)
        return filename


if __name__ == '__main__':
    cee = CondaEnvExport()
    cee.check_and_run(name='base')
