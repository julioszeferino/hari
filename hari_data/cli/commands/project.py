"""
Module for creating a new Hari project structure.
"""

from typing import Dict, List

from hari_data.cli.templates.__templates__ import (
    HariTemplate,
    HariTemplateConfigs,
    HariTemplateHelpers,
    HariTemplateJob,
    HariTemplateLock,
    HariTemplateReadme,
    HariTemplateValidators,
)


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

    files_created: List[str] = []

    directory_files: List[HariTemplate] = [
        HariTemplateValidators(project_name),
        HariTemplateJob(project_name),
        HariTemplateHelpers(project_name),
        HariTemplateConfigs(project_name),
        HariTemplateLock(project_name),
        HariTemplateReadme(project_name),
    ]

    # Create dirs
    dirs_created: List[str] = directory_files[0].create_directories()

    # Create files
    for template in directory_files:
        files_created.append(template.save_to_file())

    return {'dirs_created': dirs_created, 'files_created': files_created}
