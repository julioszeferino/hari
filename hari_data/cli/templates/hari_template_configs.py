import os

from hari_data.cli.templates.hari_template import HariTemplate


class HariTemplateConfigs(HariTemplate):
    def get_filename(self) -> str:
        return os.path.join(self.directories['configs'], 'configs.yaml')

    def get_text(self) -> str:
        return f"""
        # This is a config file template for the Hari CLI project.
        project_name: "{self.project_name}"
        version: "{self.version}"
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
