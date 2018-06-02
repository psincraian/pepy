from datetime import date


class ProjectName:
    MIN_LENGTH = 1
    MAX_LENGTH = 512

    def __init__(self, name: str):
        if len(name) < self.MIN_LENGTH or len(name) > self.MAX_LENGTH:
            from pepy.domain.exception import ProjectNameLengthIsNotValidException
            raise ProjectNameLengthIsNotValidException(name, self.MIN_LENGTH, self.MAX_LENGTH)
        self.name = name.lower().strip()


class HashedPassword:
    def __init__(self, password: str):
        self.password = password


class Password:
    def __init__(self, password: str):
        self.password = password


class Badge:
    def __init__(self, project: ProjectName, image):
        self.project = project
        self.image = image


class Downloads:
    def __init__(self, value: int):
        self.value = value


class Project:
    def __init__(self, name: ProjectName, downloads: Downloads):
        self.name = name
        self.downloads = downloads


class ProjectDownloads:
    def __init__(self, name: ProjectName, downloads: Downloads, day: date):
        self.name = name
        self.downloads = downloads
        self.day = day
