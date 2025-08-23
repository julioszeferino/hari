from hari_data.session.hari_spark_session_manager import (
    HariSparkSessionManager,
)


def test_singleton_behavior():
    # ---- Arrange & Act ----
    instance1 = HariSparkSessionManager()
    instance2 = HariSparkSessionManager()
    # ---- Assert ----
    assert instance1 is instance2


def test_manager_configure_with_configs_path(tmp_path):
    # ---- Arrange ----
    configs = {
        'app_name': 'TestApp',
        'master_url': 'local[*]',
        'spark_log_level': 'INFO',
        'jars_path': None,
    }
    config_file = tmp_path / 'spark_config.yaml'
    with open(config_file, 'w') as f:
        import yaml

        yaml.dump(configs, f)

    manager = HariSparkSessionManager()
    # Resetting instance for test isolation
    manager._instance = None
    manager._spark_session = None
    manager._logger = None

    # ---- Act ----
    manager.configure(env='local', configs_path=str(config_file))

    # ---- Assert ----
    assert manager._spark_session is not None
    assert manager._logger is not None
