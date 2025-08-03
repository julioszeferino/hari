import os
import shutil
import tempfile
from typing import Dict, List

import pytest

from hari.cli.commands.project import (
    TEMPLATES_DIR,
    project,
)


class TestProject:
    @pytest.fixture
    def temp_dir(self, tmp_path):
        tmp_path = tempfile.mkdtemp()
        original_path = os.getcwd()
        templates_dir = os.path.join(tmp_path, 'templates')
        shutil.copytree(TEMPLATES_DIR, templates_dir)
        os.chdir(tmp_path)
        yield tmp_path, templates_dir
        os.chdir(original_path)
        shutil.rmtree(tmp_path)

    def test_output_project_structure(self, temp_dir, monkeypatch):
        # Given
        tmp_path, templates_dir = temp_dir
        monkeypatch.setattr(
            'hari.cli.commands.project.TEMPLATES_DIR', templates_dir
        )
        project_name = 'project_test'
        expected_result = {
            'dirs_created': [
                f'{project_name}/configs',
                f'{project_name}/utils',
            ],
            'files_created': [
                f'{project_name}/configs/configs.yaml',
                f'{project_name}/utils/helpers.py',
                f'{project_name}/utils/validators.py',
                f'{project_name}/job.py',
                f'{project_name}/README.md',
            ],
        }
        # When
        result: Dict[str, List[str]] = project(project_name)

        # Then
        assert result == expected_result

    def test_file_not_found(self, temp_dir):
        # Given
        project_name = 'project_test'
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(
            'hari.cli.commands.project.TEMPLATES_DIR', 'non_existent_dir'
        )

        # When / Then
        with pytest.raises(FileNotFoundError):
            project(project_name)

    def test_permission_error(self, temp_dir):
        # Given
        project_name = 'project_test'
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(
            'hari.cli.commands.project.TEMPLATES_DIR', temp_dir[1]
        )
        # Simulate permission error by trying to create a file in a
        # read-only directory
        os.chmod(temp_dir[0], 0o400)

        # When / Then
        with pytest.raises(PermissionError):
            project(project_name)
        # Restore permissions so fixture teardown can clean up
        os.chmod(temp_dir[0], 0o700)

    def test_generic_exception(self, temp_dir):
        # Given
        project_name = 'project_test'
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(
            'hari.cli.commands.project.TEMPLATES_DIR', temp_dir[1]
        )
        # Simulate a generic exception by raising an exception in the
        # project function
        monkeypatch.setattr('os.makedirs', lambda *args, **kwargs: 1 / 0)

        # When / Then
        with pytest.raises(Exception) as excinfo:
            project(project_name)
        assert 'division by zero' in str(excinfo.value)
