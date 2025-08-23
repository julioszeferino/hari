import traceback
from typing import Any, Dict, Optional

from pyspark.sql import SparkSession

from hari_data.session.hari.hari_spark_session import BaseHariSparkSession


class HariSparkSessionLocal(BaseHariSparkSession):
    def __init__(
        self,
        app_name: str,
        master_url: str,
        spark_log_level: str,
        jars_path: Optional[str],
    ):
        super().__init__(app_name, master_url, spark_log_level, jars_path)

    def configure_spark_session(
        self, spark_extras: Optional[Dict[str, Any]]
    ) -> Dict[str, SparkSession]:
        """
        Configure and return a SparkSession for local mode.

        Parameters:
            spark_extras : Additional Spark configuration options as keyword arguments.

        Returns:
            Dict[str, SparkSession]: A dictionary containing the SparkSession instance.

        Examples:

            >>> hari_spark_session_local = HariSparkSessionLocal( # doctest: +SKIP
            ...     app_name='MyApp',
            ...     master_url='local[*]',
            ...     spark_log_level='INFO',
            ...     jars_path='/path/to/jars'
            ... )

            >>> hari_spark_session_local.configure_spark_session() # doctest: +SKIP
            {'spark_session': <pyspark.sql.session.SparkSession object at 0x...>}

            >>> hari_spark_session_local.configure_spark_session( # doctest: +SKIP
            ...     spark.executor.memory='2g',
            ...     spark.executor.cores='2'
            ... ) # doctest: +SKIP
            {'spark_session': <pyspark.sql.session.SparkSession object at 0x...>}
        """
        try:
            jars: Optional[Dict[str, str]] = self.get_jars_list()

            if jars:
                jars_str: Optional[str] = jars.get('jars_str', None)
                self._logger.info(f'Using JARs from: {jars_str}')
                spark_extras = {} if spark_extras is None else spark_extras
                spark_extras['spark.jars'] = jars_str

            self._logger.info('Configuring Spark session...')
            builder: SparkSession.Builder = self.get_spark_builder(
                spark_extras
            ).get('spark_builder')

            spark = builder.getOrCreate()

            if not spark:
                raise RuntimeError('Failed to create Spark session.')

            return {'spark_session': spark}

        except Exception as e:
            print('Error creating Spark session:', e)
            traceback.print_exc()
            raise
