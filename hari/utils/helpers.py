import os

import yaml


def is_hari_project() -> bool:
    return os.path.exists('hari.lock')


def create_yaml_from_dict(data: dict, dir: str, file_name: str) -> None:

    if not os.path.exists(dir):
        os.makedirs(dir)

    file_dir = os.path.join(dir, f'{file_name}.yaml')

    with open(file_dir, 'w') as file:
        yaml.dump(
            data,
            file,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
