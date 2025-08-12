import os
import shutil

import pytest

from hari.cli.commands.project import (
    TEMPLATES_DIR,
    project,
)


def _generic_exception(*args, **kwargs):
    """
    Mock function to raise a generic exception.
    """
    raise Exception('Generic error')


@pytest.fixture(scope='session')
def tmp_dir_shared(tmp_path_factory):
    """
    Create a temp dir that can be shared across tests.
    """
    original_templates_dir = TEMPLATES_DIR
    tmp_dir = tmp_path_factory.mktemp('tmp', numbered=True)
    tmp_templates_dir = tmp_dir / 'templates'
    shutil.copytree(original_templates_dir, tmp_templates_dir)
    return str(tmp_dir)


def test_project_structure(tmp_dir_shared, monkeypatch):
    # ---- Arrange ----
    # change the workdir
    os.chdir(tmp_dir_shared)
    # change the TEMPLATES_DIR variable
    monkeypatch.setattr(
        'hari.cli.commands.project.TEMPLATES_DIR',
        f'{tmp_dir_shared}/templates',
    )
    project_name = 'test_project'
    dirs_expected = [
        f'{project_name}/configs',
        f'{project_name}/utils',
    ]
    files_expected = [
        f'{project_name}/configs/configs.yaml',
        f'{project_name}/utils/helpers.py',
        f'{project_name}/utils/validators.py',
        f'{project_name}/job.py',
        f'{project_name}/README.md',
    ]
    # ---- Act ----
    result = project(project_name)
    # ---- Assert ----
    assert result['dirs_created'] == dirs_expected
    assert result['files_created'] == files_expected


def test_file_not_found_error(tmp_dir_shared, monkeypatch):
    # ---- Arrange ----
    # change the workdir
    os.chdir(tmp_dir_shared)
    # change the TEMPLATES_DIR variable to a non-existent dir
    monkeypatch.setattr(
        'hari.cli.commands.project.TEMPLATES_DIR',
        f'{tmp_dir_shared}/non_existent_dir',
    )
    project_name = 'test_project'

    # ---- Act / Assert ----
    with pytest.raises(FileNotFoundError):
        project(project_name)


def test_permission_error(tmp_dir_shared, monkeypatch):
    # ---- Arrange ----
    # change the workdir
    os.chdir(tmp_dir_shared)
    # change the TEMPLATES_DIR variable
    monkeypatch.setattr(
        'hari.cli.commands.project.TEMPLATES_DIR',
        f'{tmp_dir_shared}/templates',
    )
    project_name = 'test_project'
    # Change permissions to read-only
    os.chmod(tmp_dir_shared, 0o400)

    # ---- Act / Assert ----
    with pytest.raises(PermissionError):
        project(project_name)

    # Restore permissions
    os.chmod(tmp_dir_shared, 0o700)


def test_generic_error(tmp_dir_shared, monkeypatch):
    # ---- Arrange ----
    # change the workdir
    os.chdir(tmp_dir_shared)
    # change the TEMPLATES_DIR variable
    monkeypatch.setattr(
        'hari.cli.commands.project.TEMPLATES_DIR',
        f'{tmp_dir_shared}/templates',
    )
    project_name = 'test_project'
    # change a function os.path.join in the module
    # project() to raise a generic exception
    monkeypatch.setattr(
        'hari.cli.commands.project.os.path.join',
        _generic_exception,
    )
    # ---- Act / Assert ----
    with pytest.raises(Exception) as exc_info:
        project(project_name)
    assert 'Generic error' in str(exc_info.value)
