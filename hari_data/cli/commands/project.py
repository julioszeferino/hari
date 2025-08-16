"""
Module for creating a new Hari project structure.
"""

import os
from typing import Dict, List

from hari_data import __version__

DIRECTORIES_FILES = {
    'configs': ['configs.yaml'],
    'utils': ['helpers.py', 'validators.py'],
    '.': ['job.py', 'README.md'],
}

TEMPLATES_DIR = './hari_data/cli/templates'


def project(project_name: str) -> Dict[str, List[str]]:
    """
    Create a new project structure with the given name.

    Parameters:
        project_name (str): The name of the project.

    Returns:
        Dict[str, List[str]]: A dictionary containing the created
            directories and files.

    Raises:
        FileNotFoundError: If the template directory does not exist.
        PermissionError: If there are permission issues while creating
            files or directories.
        Exception: For any other unexpected errors.

    Examples:
        >>> project("my_project") # doctest: +SKIP
        {
            "dirs_created": [
                "my_project/configs",
                "my_project/utils",
            ],
            "files_created": [
                "my_project/configs/configs.yaml",
                "my_project/utils/helpers.py",
                "my_project/utils/validators.py",
                "my_project/job.py",
                "my_project/README.md"
            ]
        }
    """

    dirs_created: List[str] = []
    files_created: List[str] = []

    try:
        for dir, files in DIRECTORIES_FILES.items():
            if dir != '.':
                dir_path = os.path.join(project_name, dir)
                os.makedirs(dir_path, exist_ok=True)
                dirs_created.append(dir_path)
            else:
                dir_path = project_name
            for file in files:
                file_template_path = os.path.join(TEMPLATES_DIR, file)
                file_path = os.path.join(dir_path, file)
                with open(file_template_path, 'r') as template_file:
                    content = template_file.read().format(
                        project_name=project_name
                    )
                with open(file_path, 'w') as new_file:
                    new_file.write(content)
                files_created.append(file_path)

        # create a hari.lock file
        lock_file_path = os.path.join(project_name, 'hari.lock')
        with open(lock_file_path, 'w') as lock_file:
            lock_file.write(f'Hari project: {project_name}\n')
            lock_file.write(f'Created with Hari CLI version: {__version__}\n')

        return {'dirs_created': dirs_created, 'files_created': files_created}

    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Template directory '{TEMPLATES_DIR}' not found: {e}"
        ) from e
    except PermissionError as e:
        raise PermissionError(
            f'Permission denied while creating files/directories: {e}'
        ) from e
    except Exception as e:
        raise Exception(f'An unexpected error occurred: {e}') from e
