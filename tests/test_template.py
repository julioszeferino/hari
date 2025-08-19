import os
import shutil
import textwrap

import pytest

from hari_data.cli.templates.__templates__ import (
    HariTemplate,
    HariTemplateConfigs,
    HariTemplateHelpers,
    HariTemplateJob,
    HariTemplateLock,
    HariTemplateReadme,
    HariTemplateValidators,
)
from hari_data.exceptions import HariDirectoryCreationError

project_name = 'test_project'


@pytest.fixture
def tmp_dir_shared(tmp_path):
    """
    Create a temp dir that can be shared across tests.
    """
    tmp_dir = tmp_path / project_name
    tmp_dir.mkdir()
    yield str(tmp_dir)
    # Clean up the temporary directory after tests
    shutil.rmtree(str(tmp_dir), ignore_errors=True)


def raise_oserror(*args, **kwargs):
    raise OSError('Mocked error')


class DummyTemplate(HariTemplate):
    def get_filename(self) -> str:
        return f'{self.project_name}/dummy.txt'

    def get_text(self) -> str:
        return """
        # Hello, Hari!
        # This is a dummy template for testing purposes.
        """


def test_hari_template_configs_filename():
    # ---- Arrange ----
    template = HariTemplateConfigs(project_name)
    expected_filename = f'{project_name}/configs/configs.yaml'
    # ---- Act ----
    filename = template.get_filename()
    # ---- Assert ----
    assert filename == expected_filename


def test_hari_template_configs_get_text(monkeypatch):
    # ---- Arrange ----
    template = HariTemplateConfigs(project_name)
    expected_text = textwrap.dedent(
        f"""
        # This is a config file template for the Hari CLI project.
        project_name: "{project_name}"
        version: "1.0.0"
        job_name: ""
        job_description: ""
        job_type: "batch"  # Options: 'batch', 'streaming'
        job_priority: "normal"  # Options: 'low', 'normal', 'high'
        job_timeout: 3600  # Timeout in seconds
        job_retry_limit: 3  # Number of retries on failure
        job_resources:
        cpu: 2  # Number of CPU cores
        memory: "4GB"  # Memory allocation
        logging_level: "INFO"  # Options: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        input_datasets:
        - dataset_name: ""
            dataset_path: ""  # e.g. s3_path, local_path, catalog_uri
            dataset_format: "parquet"  # e.g. 'parquet', 'json', 'csv'
        output_datasets:
        - dataset_name: ""
            dataset_path: ""  # e.g. s3_path, local_path, catalog_uri
            dataset_format: "parquet"  # e.g. 'parquet', 'json', 'csv'
            partition_by: []  # e.g. ['year', 'month']
            load_strategy: "overwrite"  # Options: 'append', 'overwrite', 'upsert'
        """
    )[1:]
    # set the version
    monkeypatch.setattr(
        'hari_data.cli.templates.hari_template_configs.HariTemplateConfigs.version',
        '1.0.0',
    )
    # ---- Act ----
    result = textwrap.dedent(template.get_text())[1:]
    # ---- Assert ----
    assert result == expected_text


def test_hari_template_helpers_filename():
    # ---- Arrange ----
    template = HariTemplateHelpers(project_name)
    expected_filename = f'{project_name}/utils/helpers.py'
    # ---- Act ----
    result = template.get_filename()
    # ---- Assert ----
    assert result == expected_filename


def test_hari_template_helpers_get_text():
    # ---- Arrange ----
    template = HariTemplateHelpers(project_name)
    expected_text = textwrap.dedent(
        f"""
        # This is a helpers.py template for project {project_name}.
        # Used to create utility functions that are reused across different
        # modules in a project
        """
    )[1:]
    # ---- Act ----
    result = textwrap.dedent(template.get_text())[1:]
    # ---- Assert ----
    assert result == expected_text


def test_hari_template_job_filename():
    # ---- Arrange ----
    template = HariTemplateJob(project_name)
    expected_filename = f'{project_name}/job.py'
    # ---- Act ----
    result = template.get_filename()
    # ---- Assert ----
    assert result == expected_filename


def test_hari_template_job_get_text():
    # ---- Arrange ----
    template = HariTemplateJob(project_name)
    expected_text = textwrap.dedent(
        f'''
        # This is a job.py template for project {project_name}.
        # Used to define job configurations and execution logic
        # in data processing projects

        def main():
            """
            Main function to execute the job logic.
            This function should be implemented with the specific job requirements.
            """
            pass


        if __name__ == '__main__':
            main()
        '''
    )[1:]
    # ---- Act ----
    result = textwrap.dedent(template.get_text())[1:]
    # ---- Assert ----
    assert result == expected_text


def test_hari_template_lock_filename():
    # ---- Arrange ----
    template = HariTemplateLock(project_name)
    expected_filename = f'{project_name}/hari.lock'
    # ---- Act ----
    result = template.get_filename()
    # ---- Assert ----
    assert result == expected_filename


def test_hari_template_lock_get_text(monkeypatch):
    # ---- Arrange ----
    template = HariTemplateLock(project_name)
    expected_text = textwrap.dedent(
        f"""
        Hari project: {project_name}
        Created with Hari CLI version: 1.0.0
        """
    )[1:]
    # set the version
    monkeypatch.setattr(
        'hari_data.cli.templates.hari_template_lock.HariTemplateLock.version',
        '1.0.0',
    )
    # ---- Act ----
    result = textwrap.dedent(template.get_text())[1:]
    # ---- Assert ----
    assert result == expected_text


def test_hari_template_readme_filename():
    # ---- Arrange ----
    template = HariTemplateReadme(project_name)
    expected_filename = f'{project_name}/README.md'
    # ---- Act ----
    result = template.get_filename()
    # ---- Assert ----
    assert result == expected_filename


def test_hari_template_readme_get_text():
    # ---- Arrange ----
    template = HariTemplateReadme(project_name)
    expected_text = textwrap.dedent(
        f"""
        # Hari project: {project_name}
        """
    )[1:]
    # ---- Act ----
    result = textwrap.dedent(template.get_text())[1:]
    # ---- Assert ----
    assert result == expected_text


def test_hari_template_validators_filename():
    # ---- Arrange ----
    template = HariTemplateValidators(project_name)
    expected_filename = f'{project_name}/utils/validators.py'
    # ---- Act ----
    result = template.get_filename()
    # ---- Assert ----
    assert result == expected_filename


def test_hari_template_validators_get_text():
    # ---- Arrange ----
    template = HariTemplateValidators(project_name)
    expected_text = textwrap.dedent(
        f"""
        # This is a validators.py template for project {project_name}.
        # Used to create validation functions for data quality and integrity checks
        # in data projects
        """
    )[1:]
    # ---- Act ----
    result = textwrap.dedent(template.get_text())[1:]
    # ---- Assert ----
    assert result == expected_text


def test_hari_template_version_property(monkeypatch):
    from hari_data import __version__

    # ---- Arrange ----
    template = DummyTemplate(project_name)
    expected_version = __version__
    # ---- Act ----
    result = template.version
    # ---- Assert ----
    assert result == expected_version


def test_hari_template_get_filename():
    # ---- Arrange ----
    template = DummyTemplate(project_name)
    expected_filename = f'{project_name}/dummy.txt'
    # ---- Act ----
    result = template.get_filename()
    # ---- Assert ----
    assert result == expected_filename


def test_hari_template_get_text():
    # ---- Arrange ----
    template = DummyTemplate(project_name)
    expected_text = textwrap.dedent(
        """
        # Hello, Hari!
        # This is a dummy template for testing purposes.
        """
    )[1:]
    # ---- Act ----
    result = textwrap.dedent(template.get_text())[1:]
    # ---- Assert ----
    assert result == expected_text


def test_hari_template_create_directories(tmp_dir_shared):
    # ---- Arrange ----
    # change the workdir
    os.chdir(tmp_dir_shared)
    template = DummyTemplate(project_name)
    dirs_expected = [
        f'{project_name}/configs',
        f'{project_name}/utils',
    ]
    # ---- Act ----
    result = template.create_directories()

    # ---- Assert ----
    assert result == dirs_expected


def test_hari_template_create_directories_already_exists(tmp_dir_shared):
    # ---- Arrange ----
    # change the workdir
    os.chdir(tmp_dir_shared)
    template = DummyTemplate(project_name)
    # Create directories first time
    template.create_directories()
    # ---- Act ----
    result = template.create_directories()
    # ---- Assert ----
    assert result == []


def test_hari_template_create_directories_error(tmp_dir_shared, monkeypatch):
    # ---- Arrange ----
    # change the workdir
    os.chdir(tmp_dir_shared)
    template = DummyTemplate(project_name)
    # Mock os.makedirs to raise an exception
    monkeypatch.setattr('os.makedirs', raise_oserror)
    # ---- Act / Assert ----
    with pytest.raises(HariDirectoryCreationError) as exc_info:
        template.create_directories()
    assert 'Failed to create directory' in str(exc_info.value)


def test_hari_template_save_to_file(tmp_dir_shared):
    # ---- Arrange ----
    # change the workdir
    os.chdir(tmp_dir_shared)
    template = DummyTemplate(tmp_dir_shared)
    expected_filename = f'{tmp_dir_shared}/dummy.txt'
    # ---- Act ----
    result = template.save_to_file()
    # ---- Assert ----
    assert result == expected_filename
    assert os.path.exists(expected_filename)


def test_hari_template_save_to_file_already_exists(tmp_dir_shared):
    # ---- Arrange ----
    # change the workdir
    os.chdir(tmp_dir_shared)
    template = DummyTemplate(tmp_dir_shared)
    # Create file first time
    template.save_to_file()
    # ---- Act ----
    result = template.save_to_file()
    # ---- Assert ----
    assert not result
    assert os.path.exists(f'{tmp_dir_shared}/dummy.txt')


def test_hari_template_save_to_file_error(tmp_dir_shared, monkeypatch):
    # ---- Arrange ----
    # change the workdir
    os.chdir(tmp_dir_shared)
    template = DummyTemplate(tmp_dir_shared)
    # Mock open to raise an exception
    monkeypatch.setattr('builtins.open', raise_oserror)
    # ---- Act / Assert ----
    with pytest.raises(HariDirectoryCreationError) as exc_info:
        template.save_to_file()
    assert 'Failed to create directory' in str(exc_info.value)
