from typing import Optional


class HariError(Exception):
    """Exception base for errors related to Hari."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class HariDirectoryCreationError(HariError):
    """Exception raised when a directory cannot be created."""

    def __init__(self, directory: str, tb: str, message: Optional[str] = None):
        self.directory = directory
        self.tb = tb
        if message is None:
            message = 'Failed to create directory'
        full_message = f'{message}: {directory}'
        super().__init__(full_message)

    def __str__(self):
        return f'{self.message}\nTraceback:\n{self.tb}'
