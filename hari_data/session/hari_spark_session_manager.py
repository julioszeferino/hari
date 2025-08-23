from threading import Lock
from typing import Dict, Optional

from pyspark.sql import SparkSession

from hari_data.session.hari.hari_spark_session import BaseHariSparkSession
from hari_data.session.hari.hari_spark_session_local import (
    HariSparkSessionLocal,
)
from hari_data.utils.helpers import read_yaml_to_dict
from hari_data.utils.logger import logger_manager
from hari_data.utils.validators import (
    validate_non_empty_string,
    validate_path_exists,
)


class HariSparkSessionManager:
    _instance: Optional[object] = None
    _spark_session: Optional[SparkSession] = None
    _logger = None
    _lock: Lock = Lock()

    __factories: Dict[str, BaseHariSparkSession] = {
        'local': HariSparkSessionLocal,
    }

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(
                        HariSparkSessionManager, cls
                    ).__new__(cls)
        return cls._instance

    @property
    def is_configured(self) -> bool:
        """
        Check if the Spark session is configured.

        Returns:
            bool: True if the Spark session is configured, False otherwise.

        Examples:
            >>> HariSparkSessionManager._instance = None; HariSparkSessionManager._spark_session = None
            >>> HariSparkSessionManager().is_configured
            False

            >>> HariSparkSessionManager._spark_session = 'spark_session_mock'
            >>> HariSparkSessionManager().is_configured
            True
        """
        if self._spark_session is None:
            return False
        return True

    def configure(
        self,
        env: str,
        configs_path: str = './configs/configs.yaml',
        app_name: Optional[str] = 'HARI_JOB_DEFAULT',
        log_level: Optional[str] = 'INFO',
        master_url: Optional[str] = 'local[*]',
        jars_path: Optional[str] = None,
        spark_extras: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Configure the Spark session based on the specified environment.

        Parameters:
            env (str): The environment to configure the Spark session for (e.g., 'local').
            configs_path (str): Path to a YAML configuration file that may contain
                                'app_name', 'log_level', 'master_url', and 'jars_path' settings.
                                Default is './configs/configs.yaml'.
            app_name (Optional[str]): The name of the Spark application. Default is 'HARI_JOB_DEFAULT'.
            log_level (Optional[str]): The logging level for Spark (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR',
                                        'CRITICAL'). Default is 'INFO'.
            master_url (Optional[str]): The master URL for the Spark session (e.g., 'local[*]'). Default is None.
            jars_path (Optional[str]): Path to the directory containing JAR files to include in the Spark session.
                                    Default is None.
            spark_extras: Additional Spark configuration options as keyword arguments.

        Raises:
            ValueError: If the specified environment is not supported or if configuration parameters are invalid.

        Examples:
            >>> HariSparkSessionManager._instance = None; HariSparkSessionManager._spark_session = None
            >>> HariSparkSessionManager().configure(env='local',configs_path=None,app_name='MyApp', master_url='local[*]', jars_path=None)
            Spark session configured for environment: local

            >>> HariSparkSessionManager().configure(env='local', configs_path=None)
            Spark session is already configured. Skipping reconfiguration.

            >>> HariSparkSessionManager._instance = None; HariSparkSessionManager._spark_session = None
            >>> HariSparkSessionManager().configure(env='123')
            Traceback (most recent call last):
                ...
            ValueError: Unsupported environment '123'. Supported environments: ['local'].

        """

        if self.is_configured:
            print(
                'Spark session is already configured. Skipping reconfiguration.'
            )
            return

        configs = {}

        if configs_path:
            try:
                configs_path = validate_path_exists(
                    configs_path, 'configs_path'
                )['value']
                configs = read_yaml_to_dict(configs_path)

            except Exception as e:
                print(
                    f'Error reading configs from {configs_path}: {e}. Using Provided Parameters.'
                )

        app_name = configs.get('app_name', app_name)
        log_level = configs.get('log_level', log_level)
        master_url = configs.get('master_url', master_url)
        jars_path = configs.get('jars_path', jars_path)

        if not logger_manager.is_configured:
            logger_manager.configure(
                app_name=app_name,
                log_level=log_level,
            )

        self._logger = logger_manager.get_logger()['logger']
        env: Dict[str, str] = validate_non_empty_string(env, 'env')[
            'value'
        ].lower()

        factory_class = self.__factories.get(
            validate_non_empty_string(env, 'env')['value'].lower()
        )

        if not factory_class:
            raise ValueError(
                f"Unsupported environment '{env}'. Supported environments: {list(self.__factories.keys())}."
            )

        factory: BaseHariSparkSession = factory_class(
            app_name=app_name,
            master_url=master_url,
            spark_log_level=log_level,
            jars_path=jars_path,
        )

        spark: Dict[str, SparkSession] = factory.create_spark_session(
            spark_extras=spark_extras
        )

        self._spark_session = spark.get('spark_session')
        print(f'Spark session configured for environment: {env}')

    def get_spark_session(self) -> Dict[str, SparkSession]:
        """
        Get the configured Spark session.

        Returns:
            Dict[str, SparkSession]: A dictionary containing the SparkSession instance.

        Raises:
            ValueError: If the Spark session has not been configured.

        Examples:
            >>> HariSparkSessionManager().configure(env='local',configs_path=None,app_name='MyApp', master_url='local[*]', jars_path=None)
            Spark session configured for environment: local
            >>> HariSparkSessionManager().get_spark_session()
            {'spark_session': <pyspark.sql.session.SparkSession object at 0x...>}

            >>> HariSparkSessionManager._instance = None; HariSparkSessionManager._spark_session = None
            >>> HariSparkSessionManager().get_spark_session()
            Traceback (most recent call last):
                ...
            ValueError: Spark session is not configured. Please call 'configure' first.
        """
        if not self.is_configured:
            raise ValueError(
                "Spark session is not configured. Please call 'configure' first."
            )
        return {'spark_session': self._spark_session}

    def stop_spark_session(self) -> None:
        """
        Stop the Spark session and reset the manager.

        Examples:
            >>> HariSparkSessionManager._instance = None; HariSparkSessionManager._spark_session = None
            >>> HariSparkSessionManager().configure(env='local',configs_path=None,app_name='MyApp', master_url='local[*]', jars_path=None)
            Spark session configured for environment: local
            >>> HariSparkSessionManager().stop_spark_session()
            Spark session stopped and manager reset.
            >>> HariSparkSessionManager().stop_spark_session()
        """
        if not self.is_configured:
            return
        self._spark_session.stop()
        self._spark_session = None
        self._instance = None
        print('Spark session stopped and manager reset.')


hari_spark_manager = HariSparkSessionManager()
