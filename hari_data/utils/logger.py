import logging
import sys
from typing import Optional

from hari_data.exceptions import HariLoggerNotConfigured
from hari_data.utils.helpers import read_yaml_to_dict


class Logger:
    """
    Singleton class to manage logging configuration and provide
    a logger instance.

    examples:
        >>> Logger()
        <logger.Logger object at 0x...>
    """

    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    @property
    def is_configured(self) -> bool:
        """
        Check if the logger is configured.

        Returns:
            bool: True if the logger is configured, False otherwise.

        Examples:
            >>> Logger._instance = None; Logger._logger = None
            >>> Logger().is_configured
            False
        """
        return self._logger is not None

    def configure(
        self,
        app_name: str = 'HARI_JOB_DEFAULT',
        log_level: str = 'INFO',
        configs_path: Optional[str] = None,
    ) -> None:
        """
        Configure the logger with the specified application name and log level.

        Parameters:
            app_name (str): The name of the application for logging purposes.
                            Default is "HARI_JOB_DEFAULT".
            log_level (str): The logging level (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
                             Default is "INFO".
            configs_path (Optional[str]): Path to a YAML configuration file that may contain
                                          'app_name' and 'log_level' settings.

        Examples:
            >>> Logger().configure()
            Logger configured with app name "HARI_JOB_DEFAULT" and log level "INFO".

            >>> Logger._instance = None; Logger._logger = None
            >>> Logger().configure(app_name='MyApp')
            Logger configured with app name "MyApp" and log level "INFO".

            >>> Logger._instance = None; Logger._logger = None
            >>> Logger().configure(app_name='AnotherMyApp', log_level='DEBUG')
            Logger configured with app name "AnotherMyApp" and log level "DEBUG".

            >>> Logger().configure(configs_path='./configs') # doctest: +SKIP
            Logger configured with app name "MyApp" and log level "ERROR".


        """
        if self._logger is not None:
            self._logger.warning(
                'Logger is already configured. Ignoring the new configuration.'
            )
            return

        if configs_path:
            configs = read_yaml_to_dict(configs_path)
            app_name = configs.get('app_name', app_name)
            log_level = configs.get('log_level', log_level)

        self._logger = logging.getLogger(app_name)
        self._logger.setLevel(
            getattr(logging, log_level.upper(), logging.INFO)
        )

        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

        print(
            f'Logger configured with app name "{app_name}" and log level "{log_level}".'
        )

    def get_logger(self) -> logging.Logger:
        """
        Get the configured logger instance.

        Returns:
            logging.Logger: The configured logger instance.

        Raises:
            HariLoggerNotConfigured: If the logger has not been configured yet.

        Examples:
            >>> Logger().get_logger()
            {'logger': <Logger ...>}

            >>> Logger._instance = None; Logger._logger = None
            >>> try:
            ...     Logger().get_logger()
            ... except HariLoggerNotConfigured as e:
            ...     print(f"{type(e).__name__}: {e}")
            HariLoggerNotConfigured: Logger has not been configured. Call the .configure() method first.
        """
        if self._logger is None:
            raise HariLoggerNotConfigured()
        return {'logger': self._logger}


logger_manager = Logger()
