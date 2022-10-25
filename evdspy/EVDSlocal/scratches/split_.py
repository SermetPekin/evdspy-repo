# --------------------------------------------------------------------------------------
root_version = "1.0.16rc2"
# python setup.py bdist_wheel --universal
test_environment = r""
cmd_file = "Run_Produced"
package_name = "evdspy"

# --------------------------------------------------------------------------------------
from dataclasses import dataclass
from enum import Enum, auto


class VersionType(Enum):
    development = auto()
    production = auto()


from evdspy.EVDSlocal.components.api_params import get_enum_with_value

from pathlib import Path

from evdspy.EVDSlocal.common.files import Read
from typing import Union


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
            status_pre = self.status_pre
        if status_pre:
            pre = "rc"
            self.version = f"{self.major}.{self.minor}.{self.patch}.{self.patch2}{pre}{self.extra}"
            return
        self.version = f"{self.major}.{self.minor}.{self.patch}.{self.patch2}"

    def next_version(self):
        ...

    def increment(self, next_status=True):
        major = self.major
        minor = self.minor
        patch = self.patch
        patch2 = self.patch2
        extra = self.extra

        if self.status_pre:
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
    version = version.replace("#", "").strip()
    if "rc" in version:
        status_pre = True
        major, minor, patch, e = version.split(".")

        patch2 = int(e.split("rc")[0])
        extra = int(e.split("rc")[1])


    else:
        major, minor, patch, patch2, status_pre, extra, = version.split(".")
    return VersionParts(major, minor, patch, patch2, extra, status_pre)


def get_previous():
    # p = Path() / package_name / "__version__.py"
    p = Path() / "__version__.py"
    if p.is_file():
        c = Read(p)
    else:
        raise "Version not found"
    return c


def get_prev_version_instance():
    return create_version_instance(get_previous())


def get_next_version(next_status_pre_release=True):
    e = get_prev_version_instance()
    # print(e)
    return e.increment(next_status_pre_release=next_status_pre_release)

# v2 = get_next_version()
# print(v2)
