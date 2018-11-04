from abc import abstractmethod, ABC

from pepy.domain.model import ProjectName, Password


class DomainException(ABC, Exception):
    @abstractmethod
    def message(self) -> str:
        pass


class ProjectNotFoundException(DomainException):
    def __init__(self, project_name: str):
        self.project_name = project_name

    def message(self) -> str:
        return "Project with name {} does not exist".format(self.project_name)


class ProjectNameLengthIsNotValidException(DomainException):
    def __init__(self, project_name: str, min_length: int, max_length: int):
        self.project_name = project_name
        self.min_length = min_length
        self.max_length = max_length

    def message(self) -> str:
        return 'Name "{}" is not valid, length should be between {} and {}'.format(
            self.project_name, self.min_length, self.max_length
        )


class InvalidAdminPassword(DomainException):
    def __init__(self, password: Password):
        self.password = password

    def message(self) -> str:
        return 'Password "{}" is not a valid admin password'.format(self.password.password)
