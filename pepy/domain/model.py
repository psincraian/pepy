from datetime import date
import attr


@attr.s
class ProjectName:
    name: str = attr.ib()
    MIN_LENGTH = 1
    MAX_LENGTH = 512

    @name.validator
    def _check(self, attribute, value):
        if len(value) < self.MIN_LENGTH or len(value) > self.MAX_LENGTH:
            from pepy.domain.exception import ProjectNameLengthIsNotValidException

            raise ProjectNameLengthIsNotValidException(value, self.MIN_LENGTH, self.MAX_LENGTH)

    def __attrs_post_init__(self):
        self.name = self.name.lower().strip()


@attr.s
class HashedPassword:
    password: str = attr.ib()


@attr.s
class Password:
    password: str = attr.ib()


@attr.s
class Badge:
    project: ProjectName = attr.ib()
    image = attr.ib()


@attr.s
class Downloads:
    value: int = attr.ib()


class Project:
    def __init__(self, name: ProjectName, downloads: Downloads):
        self.name = name
        self.downloads = downloads


@attr.s
class ProjectDownloads:
    name: ProjectName = attr.ib()
    downloads: Downloads = attr.ib()
    day: date = attr.ib()
