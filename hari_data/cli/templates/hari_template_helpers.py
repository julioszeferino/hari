import os

from hari_data.cli.templates.hari_template import HariTemplate


class HariTemplateHelpers(HariTemplate):
    def get_filename(self) -> str:
        return os.path.join(self.directories['utils'], 'helpers.py')

    def get_text(self) -> str:
        return f"""
        # This is a helpers.py template for project {self.project_name}.
        # Used to create utility functions that are reused across different
        # modules in a project
        """
