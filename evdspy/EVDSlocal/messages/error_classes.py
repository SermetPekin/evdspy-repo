from ..common.common_imports import *


###########################  Base Exception Class ###########################
class BaseException(Exception):
    def __init__(self, message="Something happpened"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f' -> {self.message}'


###########################  / Base Exception Class ###########################
class ApiKeyNotSetError(BaseException):
    def __init__(self, message="Api key not set yet."):
        self.message = message

class SeriesEmptyError(BaseException):
    def __init__(self, message="Series cannot be empty"):
        self.message = message

class OptionsFileNotLoadedError(BaseException):
    def __init__(self, message="Options file not loaded..."):
        self.message = message


class SeriesFileDoesNotExists(BaseException):
    def __init__(self, message="Series file does not exist..."):
        self.message = message


class BucketFromSeriesFolderCreateError(BaseException):
    def __init__(self, message="BucketFromSeriesFolderCreateError folder problem"):
        self.message = message


class ExceptionMixing(ABC):
    ...
