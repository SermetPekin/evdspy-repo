from dataclasses import dataclass
from enum import Enum, auto
from evdspy.EVDSlocal.components.api_params import get_enum_with_value
from pathlib import Path
from evdspy.EVDSlocal.common.files import Read
from typing import Union


# class VersionType(Enum):
#     development = auto()
#     production = auto()


def increment(d: Union[str, int]):
    if isinstance(d, str):
        d = int(d)
    return str(d + 1)


@dataclass
class VersionParts:
    major: int
    minor: int
    patch: int
    patch2: int
    extra: int = 0
    next_status_pre_release: bool = True
    version = ""

    def __post_init__(self):
        self.combine()
        # print(self.version)

    def combine(self, status_pre=None):
        if status_pre is None:
            status_pre = self.next_status_pre_release
        if status_pre:
            pre = "rc"
            self.version = f"{self.major}.{self.minor}.{self.patch}.{self.patch2}{pre}{self.extra}"
            return
        self.version = f"{self.major}.{self.minor}.{self.patch}.{self.patch2}"



    def increment(self, next_status=True):
        major = self.major
        minor = self.minor
        patch = self.patch
        patch2 = self.patch2
        extra = self.extra

        if self.next_status_pre_release:
            if next_status:
                extra = self.extra + 1
            else:
                patch2 = self.patch2 + 1
                extra = 0

        else:
            if next_status:
                extra = self.extra + 1
            else:
                patch2 = self.patch2 + 1
        # self.combine(next_status)

        new_element = VersionParts(major, minor, patch, patch2, extra, next_status)
        return new_element

    def __str__(self):
        return self.version


def create_version_instance(version: str):
    version = version.replace("#", "").strip().replace("'", "")
    if "rc" in version:
        status_pre = True
        # 1.0.17.6rc2
        major, minor, patch, e = version.split(".")
        sp = e.split("rc")
        patch2 = int(e.split("rc")[0])
        extra = int(e.split("rc")[1])


    else:
        major, minor, patch, patch2, status_pre, extra, = version.split(".")
    return VersionParts(major, minor, patch, patch2, extra, status_pre)


def get_previous():
    p = Path() / "evdspy" / "__version__.py"
    # p = Path() / "__version__.py"
    if p.is_file():
        c = Read(p)
        c = c.replace("version", "")
        c = c.replace("=", "").strip()
    else:
        raise "Version not found"
    return c


def get_prev_version_instance():
    print(get_previous())
    return create_version_instance(get_previous())


def get_next_version(increment=True, next_status_pre_release=True):
    """ M A I N   F U N C """
    e = get_prev_version_instance()
    if not increment:
        return e
    return e.increment(next_status_pre_release)

# v2 = get_next_version()
# print(v2)
