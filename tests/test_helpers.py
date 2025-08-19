import os

import pytest
import yaml

from hari_data.utils.helpers import create_yaml_from_dict, is_hari_project


def test_is_hari_project_true(tmp_path, monkeypatch):
    # Arrange: create a dummy 'hari.lock' file in the temp directory
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'hari.lock').touch()
    # Act & Assert
    assert is_hari_project() is True


def test_is_hari_project_false(tmp_path, monkeypatch):
    # Arrange: ensure 'hari.lock' does not exist
    monkeypatch.chdir(tmp_path)
    # Act & Assert
    assert is_hari_project() is False


def test_create_yaml_from_dict_creates_file(tmp_path):
    # Arrange
    data = {'a': 1, 'b': [2, 3]}
    dir_name = tmp_path / 'mydir'
    file_name = 'myfile'
    # Act
    create_yaml_from_dict(data, str(dir_name), file_name)
    # Assert
    yaml_path = dir_name / f'{file_name}.yaml'
    assert yaml_path.exists()
    with open(yaml_path, 'r') as f:
        loaded = yaml.safe_load(f)
    assert loaded == data


def test_create_yaml_from_dict_creates_dir(tmp_path):
    # Arrange
    data = {'foo': 'bar'}
    dir_name = tmp_path / 'newdir'
    file_name = 'testfile'
    # Act
    create_yaml_from_dict(data, str(dir_name), file_name)
    # Assert
    assert os.path.isdir(dir_name)
    assert os.path.isfile(dir_name / f'{file_name}.yaml')


def test_create_yaml_from_dict_raises_oserror(monkeypatch):
    # Simulate OSError when creating directory
    def raise_oserror(*args, **kwargs):
        raise OSError('Cannot create directory')

    monkeypatch.setattr(os, 'makedirs', raise_oserror)
    with pytest.raises(
        OSError, match='Error creating YAML file: Cannot create directory'
    ):
        from hari_data.utils.helpers import create_yaml_from_dict

        create_yaml_from_dict({}, '/nonexistent_dir', 'file')


def test_create_yaml_from_dict_raises_yamlerror(monkeypatch, tmp_path):
    # Simula erro do yaml.dump para garantir cobertura do except yaml.YAMLError
    dir_name = tmp_path / 'errordir'
    dir_name.mkdir()
    # Patch yaml.dump no namespace correto
    import hari_data.utils.helpers as helpers

    monkeypatch.setattr(
        helpers.yaml,
        'dump',
        lambda *a, **kw: (_ for _ in ()).throw(
            yaml.YAMLError('YAML dump error')
        ),
    )
    with pytest.raises(
        yaml.YAMLError, match='Error writing YAML file: YAML dump error'
    ):
        helpers.create_yaml_from_dict({}, str(dir_name), 'file')
