import os

import yaml


def is_hari_project() -> bool:
    """
    Check if the current directory is a Hari project by looking for the
    presence of a 'hari.lock' file.

    Returns:
        bool: True if 'hari.lock' exists, indicating a Hari project; False otherwise.

    Examples:
        >>> is_hari_project() # doctest: +SKIP
        True
    """
    return os.path.exists('hari.lock')


def create_yaml_from_dict(data: dict, dir: str, file_name: str) -> None:
    """
    Create a YAML file from a dictionary.

    Parameters:
        data (dict): The dictionary to convert to YAML.
        dir (str): The directory where the YAML file will be created.
        file_name (str): The name of the YAML file (without extension).

    Examples:
        >>> create_yaml_from_dict( # doctest: +SKIP
        ... {'key': 'value'},
        ... '/path/to/dir',
        ... 'file_name'
        )
        YAML file created at: /path/to/dir/file_name.yaml

    Raises:
        OSError: If the directory cannot be created or written to.
        yaml.YAMLError: If there is an error in writing the YAML file.
    """
    try:
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
            print(f'YAML file created at: {file_dir}')
    except OSError as e:
        raise OSError(f'Error creating YAML file: {e}')
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f'Error writing YAML file: {e}')


def read_yaml_to_dict(file_path: str) -> dict:
    """
    Read a YAML file and convert its contents to a dictionary.

    Parameters:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The contents of the YAML file as a dictionary.

    Examples:
        >>> read_yaml_to_dict('/path/to/file.yaml') # doctest: +SKIP
        {'key': 'value'}

    Raises:
        FileNotFoundError: If the specified file does not exist.
        yaml.YAMLError: If there is an error in reading the YAML file.
    """
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data if data is not None else {}
    except FileNotFoundError as e:
        raise FileNotFoundError(f'YAML file not found: {e}')
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f'Error reading YAML file: {e}')
