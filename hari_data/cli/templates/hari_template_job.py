import os

from hari_data.cli.templates.hari_template import HariTemplate


class HariTemplateJob(HariTemplate):
    def get_filename(self) -> str:
        return os.path.join(self.directories['root'], 'job.py')

    def get_text(self) -> str:
        return f'''
        # This is a job.py template for project {self.project_name}.
        # Used to define job configurations and execution logic
        # in data processing projects

        def main():
            """
            Main function to execute the job logic.
            This function should be implemented with the specific job requirements.
            """
            pass


        if __name__ == '__main__':
            main()
        '''
