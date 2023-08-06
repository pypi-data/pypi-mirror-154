import os
import tal
from tal.util import local_file_path
import datetime


def create_nlos_scene(folder_name):
    folder_name = os.path.abspath(folder_name)
    path, name = os.path.split(folder_name)
    assert os.path.isdir(path), f'{path} does not exist'
    try:
        os.mkdir(folder_name)
    except OSError as exc:
        raise AssertionError(f'Invalid permissions: {exc}')

    config_name = os.path.join(folder_name, f'{name}.yaml')
    default_yaml_data = open(local_file_path(
        'render/scene_defaults.yaml'), 'w').readlines()
    default_yaml_data = '\n'.join(list(
        map(lambda l: l if l.startswith('#') else f'#{l}', default_yaml_data)))

    with open(config_name, 'w') as f:
        f.write(
            '# TAL v{v} NLOS scene description file: {r}\n'.format(
                v=tal.__version__, r='https://github.com/diegoroyo/tal'))
        f.write('# Created on {d} with experiment name {n}\n'.format(
                d=datetime.datetime.now(), n=name))
        f.write('#\n')
        f.write('# All commented variables show their default value\n')
        f.write('# To render the scene with this configuration, execute:\n')
        f.write('# Usage: python3 -m tal {c}\n'.format(
                c=config_name))
        f.write('\n')
        f.write(default_yaml_data)

    print(f'Success! Now:'
          f'1) Edit the configuration file in {config_name}'
          f'2) Render with python3 -m tal {config_name}')


def render_nlos_scene(config_filename):
    pass
