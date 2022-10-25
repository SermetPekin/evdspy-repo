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
    pre_release: bool = True
    version = ""

    def make_int(self, item):
        if isinstance(item, str):
            return int(item)
        return item

    def __post_init__(self):
        items = ("major", "minor", "patch", "patch2", "extra")
        for item in items:
            setattr(self, item, self.make_int(getattr(self, item)))
            print("setting", item, self.make_int(getattr(self, item)))

        self.combine()
        # print(self.version)

    def combine(self ):

        if self.pre_release:
            pre = "rc"
            self.version = f"{self.major}.{self.minor}.{self.patch}.{self.patch2}{pre}{self.extra}"
            return
        self.version = f"{self.major}.{self.minor}.{self.patch}.{self.patch2}"

    def increment(self, next_status, prev_instance):
        major = self.major
        minor = self.minor
        patch = self.patch
        patch2 = self.patch2
        extra = self.extra

        if next_status and prev_instance.pre_release:
            # 1.3rc1=>#1.3rc2
            extra = self.extra + 1
        if next_status and not prev_instance.pre_release:
            patch2 = self.patch2 + 1
            extra = 1
        if not next_status and not prev_instance.pre_release:
            patch2 = self.patch2 + 1
            extra = 0
        if not next_status and prev_instance.pre_release:
            patch = self.patch
            extra = 0
        # self.combine(next_status)

        new_element = VersionParts(major, minor, patch, patch2, extra, next_status)
        print(new_element)
        # exit()
        return new_element

    def __str__(self):
        return self.version


def create_version_instance(version: str):
    # assert len(version.split(".")) > 3, "previous version has shape error."
    if not len(version.split(".")) > 3:
        version = "1.0.17.6rc1"
    version = version.lower().replace("#", "").strip().replace("'", "")
    if "rc" in version:
        status_pre = True
        # 1.0.17.6rc2
        major, minor, patch, e = version.split(".")

        sp = e.split("rc")
        patch2 = int(sp[0])
        extra = int(sp[1])
    else:
        # 1.0.17.6
        status_pre = False
        major, minor, patch, patch2 = version.split(".")
        extra = 0
    instance = VersionParts(major, minor, patch, patch2, extra=extra, pre_release=status_pre)
    print(instance)

    return instance


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


def get_next_version(increment=True, pre_release=True):
    """ M A I N   F U N C """
    e = get_prev_version_instance()
    if not increment:
        return e
    if e.pre_release:
        if pre_release:
            return e.increment(pre_release, prev_instance=e)
        else:
            return e.increment(pre_release, prev_instance=e)

# v2 = get_next_version()
# print(v2)
