import os

from hari_data.cli.templates.hari_template import HariTemplate


class HariTemplateLock(HariTemplate):
    def get_filename(self) -> str:
        return os.path.join(self.directories['root'], 'hari.lock')

    def get_text(self) -> str:
        return f"""
        Hari project: {self.project_name}
        Created with Hari CLI version: {self.version}
        """
