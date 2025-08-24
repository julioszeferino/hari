import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from pyspark.sql import SparkSession

from hari_data.utils.logger import logger_manager
from hari_data.utils.validators import (
    validate_non_empty_string,
    validate_path_exists,
    validate_type,
)


class BaseHariSparkSession(ABC):
    def __init__(
        self,
        app_name: str,
        master_url: str = 'local[*]',
        spark_log_level: str = 'INFO',
        jars_path: Optional[str] = None,
    ):
        self._logger = logger_manager.get_logger()['logger']
        self._app_name: str = validate_non_empty_string(app_name, 'app_name')[
            'value'
        ]
        self._master_url: str = validate_type(master_url, str, 'master_url')[
            'value'
        ]
        if jars_path is not None:
            jars_path = validate_path_exists(jars_path, 'jars_path')['value']
        self._jars_path: Optional[str] = jars_path
        self._spark_log_level: str = spark_log_level

    @abstractmethod
    def configure_spark_session(self) -> None:  # pragma: no cover
        pass

    def get_jars_list(self) -> Optional[Dict[str, str]]:
        """
        Get a comma-separated string of all JAR files in the jars_path directory.

        Returns:
            Optional[Dict[str, str]]: A dictionary with the key 'jars_str' containing
            the comma-separated string of JAR file paths, or None if jars_path is not set.

        Examples:
            >>> BaseHariSparkSession.get_jars_list()  # doctest: +SKIP
            {'jars_str': '/path/to/jar1.jar,/path/to/jar2.jar'}
            >>> BaseHariSparkSession.get_jars_list()  # doctest: +SKIP
            None
        """
        if not self._jars_path:
            return

        jars = [
            os.path.join(self._jars_path, jar)
            for jar in os.listdir(self._jars_path)
            if jar.endswith('.jar')
        ]
        jars_str = ','.join(jars)
        return {'jars_str': jars_str}

    def get_spark_builder(
        self, spark_extras: Optional[Dict[str, Any]]
    ) -> Dict[str, SparkSession.Builder]:
        """
        Create and return a SparkSession.Builder configured with the provided parameters.

        Parameters:
            spark_extras: Additional Spark configuration options as keyword arguments.

        Returns:
            Dict[str, SparkSession.Builder]: A dictionary containing the SparkSession.Builder instance.

        Examples:
            >>> hari_spark_session = BaseHariSparkSession( # doctest: +SKIP
            ...     app_name='MyApp',
            ...     master_url='local[*]',
            ...     spark_log_level='INFO',
            ...     jars_path='/path/to/jars'
            ... )
            {'spark_builder': <pyspark.sql.session.SparkSession.Builder object at 0x...>}
        """
        builder: SparkSession = SparkSession.builder.appName(
            self._app_name
        ).master(self._master_url)

        if spark_extras:
            for key, value in spark_extras.items():
                builder = builder.config(key, value)

        return {'spark_builder': builder}

    def create_spark_session(
        self,
        spark_extras: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, SparkSession]:  # pragma: no cover
        """
        Create and return a SparkSession.

        Parameters:
            spark_extras: Keyword arguments to pass to the configure_spark_session method.

        Returns:
            Dict[str, SparkSession]: A dictionary containing the SparkSession instance.

        Examples:
            >> > BaseHariSparkSession.create_spark_session()  # doctest: +SKIP
            {'spark_session': < pyspark.sql.session.SparkSession object at 0x...>}
        """
        spark: SparkSession = self.configure_spark_session(
            spark_extras=spark_extras
        ).get('spark_session')

        spark.sparkContext.setLogLevel(self._spark_log_level)

        self._logger.info('Spark session configured successfully.')
        self._logger.info(f'Spark version: {spark.version}')
        self._logger.info(
            f'Spark UI available at: {spark.sparkContext.uiWebUrl}'
        )
        self._logger.info(
            f'Spark Config: {spark.sparkContext.getConf().getAll()}'
        )
        self._logger.info(
            f'Jars: {spark.sparkContext.getConf().get("spark.jars", None)}'
        )
        return {'spark_session': spark}
