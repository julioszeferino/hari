import os

from hari_data.cli.templates.hari_template import HariTemplate


class HariTemplateValidators(HariTemplate):
    def get_filename(self) -> str:
        return os.path.join(self.directories['utils'], 'validators.py')

    def get_text(self) -> str:
        return f"""
        # This is a validators.py template for project {self.project_name}.
        # Used to create validation functions for data quality and integrity checks
        # in data projects
        """
