import os
import textwrap
import traceback
from abc import ABCMeta, abstractmethod

from hari_data import __version__
from hari_data.exceptions import HariDirectoryCreationError


class HariTemplate(metaclass=ABCMeta):
    def __init__(self, project_name: str):
        self.__project_name = project_name
        self.__directories = {
            'root': f'{self.project_name}',
            'configs': f'{self.project_name}/configs',
            'utils': f'{self.project_name}/utils',
        }

    @property
    def project_name(self) -> str:
        return self.__project_name

    @property
    def version(self) -> str:
        return __version__

    @property
    def directories(self) -> dict:
        return self.__directories

    @abstractmethod
    def get_filename(self) -> str:  # pragma: no cover
        pass

    @abstractmethod
    def get_text(self) -> str:  # pragma: no cover
        pass

    def create_directories(self):
        dirs_created = []

        for directory in self.directories.values():
            if directory != self.directories['root']:
                if not os.path.exists(directory):
                    try:
                        os.makedirs(directory)
                        dirs_created.append(directory)
                    except Exception:
                        tb = traceback.format_exc()
                        raise HariDirectoryCreationError(directory, tb)
        return dirs_created

    def save_to_file(self):
        filename: str = self.get_filename()
        text: str = textwrap.dedent(self.get_text())[1:]
        try:
            if not os.path.exists(filename):
                with open(filename, 'w') as file:
                    file.write(text)
                return filename
        except Exception:
            tb = traceback.format_exc()
            raise HariDirectoryCreationError(filename, tb)

    def create_hari_structure(self):  # pragma: no cover
        self.create_directories()
        self.save_to_file()
