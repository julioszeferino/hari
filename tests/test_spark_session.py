from pyspark.sql import SparkSession

from hari_data.session.hari.hari_spark_session import BaseHariSparkSession
from hari_data.session.hari.hari_spark_session_generic import (
    HariSparkSessionGeneric,
)
from hari_data.utils.logger import Logger

# Configura o logger para todos os testes deste arquivo
Logger().configure(app_name='TestApp')


class DummyTemplate(BaseHariSparkSession):
    def configure_spark_session(self):
        print('Configured')


# ---------- Tests for BaseHariSparkSession ----------
def test_get_jars_list_no_path():
    # ---- Arrange ----
    template = DummyTemplate(
        app_name='TestApp',
        master_url='local[*]',
        spark_log_level='INFO',
        jars_path=None,
    )
    # ---- Act ----
    result = template.get_jars_list()
    # ---- Assert ----
    assert result is None


def test_get_jars_list_with_path(tmp_path):
    # ---- Arrange ----
    # Create dummy jar files in a temporary directory
    jar1 = tmp_path / 'dummy1.jar'
    jar1.write_text('This is a dummy jar file 1.')

    template = DummyTemplate(
        app_name='TestApp',
        master_url='local[*]',
        spark_log_level='INFO',
        jars_path=str(tmp_path),
    )
    # ---- Act ----
    result = template.get_jars_list()
    # ---- Assert ----
    expected_jars_str = f'{jar1}'
    assert result == {'jars_str': expected_jars_str}


def test_get_spark_builder():
    # ---- Arrange ----
    template = DummyTemplate(
        app_name='TestApp',
        master_url='local[*]',
        spark_log_level='INFO',
        jars_path=None,
    )
    # ---- Act ----
    result = template.get_spark_builder(
        spark_extras={'spark.executor.memory': '2g'}
    )
    # ---- Assert ----
    assert 'spark_builder' in result
    builder = result['spark_builder']
    assert isinstance(builder, SparkSession.Builder)
    assert builder._options['spark.app.name'] == 'TestApp'
    assert builder._options['spark.master'] == 'local[*]'
    assert builder._options['spark.executor.memory'] == '2g'


# ---------- Tests for HariSparkSessionGeneric ----------
def test_hari_spark_local_super_init(monkeypatch):
    # ---- Arrange ----
    called = {}

    # Simulate the super class __init__ method
    def fake_super_init(
        self, app_name, master_url, spark_log_level, jars_path
    ):
        called['args'] = (
            self,
            app_name,
            master_url,
            spark_log_level,
            jars_path,
        )

    # Patch the super class __init__ method
    monkeypatch.setattr(
        BaseHariSparkSession, '__init__', fake_super_init, raising=True
    )

    # ---- Act ----
    # Create an instance of HariSparkSessionGeneric but do not call __init__
    result = HariSparkSessionGeneric.__new__(HariSparkSessionGeneric)
    # Call the patched __init__ method
    result.__init__(
        app_name='TestApp',
        master_url='local[*]',
        spark_log_level='INFO',
        jars_path=None,
    )

    # ---- Assert ----
    assert 'args' in called
    assert called['args'][1] == 'TestApp'
    assert called['args'][2] == 'local[*]'
    assert called['args'][3] == 'INFO'


def test_hari_spark_local_get_spark_session(monkeypatch):
    # ---- Arrange ----
    app_name = 'TestApp'
    master_url = 'local[*]'
    spark_log_level = 'INFO'
    jars_path = None
    template = HariSparkSessionGeneric(
        app_name=app_name,
        master_url=master_url,
        spark_log_level=spark_log_level,
        jars_path=jars_path,
    )
    monkeypatch.setattr(
        template,
        'get_jars_list',
        lambda: {'jars_str': 'dummy.jar'},
        raising=True,
    )
    monkeypatch.setattr(template._logger, 'info', lambda *args, **kwargs: None)

    def fake_get_or_create(self):
        return 'fake_session'

    monkeypatch.setattr(
        SparkSession.Builder, 'getOrCreate', fake_get_or_create, raising=True
    )
    expected_result = {'spark_session': 'fake_session'}

    # ---- Act ----
    result = template.configure_spark_session(spark_extras=None)

    # ---- Assert ----
    assert result == expected_result


def test_hari_spark_local_get_spark_session_with_errors(monkeypatch):
    # ---- Arrange ----
    app_name = 'TestApp'
    master_url = 'local[*]'
    spark_log_level = 'INFO'
    jars_path = None
    template = HariSparkSessionGeneric(
        app_name=app_name,
        master_url=master_url,
        spark_log_level=spark_log_level,
        jars_path=jars_path,
    )
    monkeypatch.setattr(
        template,
        'get_jars_list',
        lambda: {'jars_str': 'dummy.jar'},
        raising=True,
    )
    monkeypatch.setattr(template._logger, 'info', lambda *args, **kwargs: None)

    def fake_get_or_create(self):
        return None  # Simulate failure to create session

    monkeypatch.setattr(
        SparkSession.Builder, 'getOrCreate', fake_get_or_create, raising=True
    )

    # ---- Act & Assert ----
    try:
        template.configure_spark_session(spark_extras=None)
        assert False, 'Expected RuntimeError was not raised'
    except RuntimeError as e:
        assert str(e) == 'Failed to create Spark session.'
