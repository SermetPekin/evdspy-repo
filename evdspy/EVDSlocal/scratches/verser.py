import random

from dataclasses import dataclass
from pathlib import Path

test = True
mock_versions = {
    0: "1.0.17.2",
    1: "1.0.17.3rc2",
    2: "1.0.17.8rc6",
    3: "1.0.17.7",
    4: "1.0.17.9rc2",
    5: "1.0.17.9rc8",
}

import random


def mock_read(p: Path):
    x = random.choice(tuple(mock_versions.keys()))
    return mock_versions[x]


def increment(next_status, prev_instance):
    major = prev_instance.major
    minor = prev_instance.minor
    patch = prev_instance.patch
    patch2 = prev_instance.patch2
    extra = prev_instance.extra
    if next_status and prev_instance.pre_release:
        # 1.3rc3<=#1.3rc2
        extra = extra + 1
    if next_status and not prev_instance.pre_release:
        # 1.4rc1<=#1.3
        patch2 = patch2 + 1
        extra = 1
    if not next_status and not prev_instance.pre_release:
        # 1.4<=#1.3
        patch2 = patch2 + 1
        extra = 0
    if not next_status and prev_instance.pre_release:
        # 1.3<=#1.3rc2
        patch2 = patch2 + 0
        extra = 0
    # self.combine(next_status)

    new_element = VersionParts(major, minor, patch, patch2, extra, next_status)
    # exit()
    return new_element


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
            # print("setting", item, self.make_int(getattr(self, item)))

        self.combine()
        # print(self.version)

    def combine(self):

        if self.pre_release:
            pre = "rc"
            self.version = f"{self.major}.{self.minor}.{self.patch}.{self.patch2}{pre}{self.extra}"
            return
        self.version = f"{self.major}.{self.minor}.{self.patch}.{self.patch2}"

    def __str__(self):
        return self.version


def create_version_instance(version: str):
    # assert len(version.split(".")) > 3, "previous version has shape error."
    # if not len(version.split(".")) > 3:
    #     version = "1.0.17.6rc1"
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
    # print(instance)

    return instance


if test:
    Read = lambda x: mock_read(x)


def get_previous():
    p = Path() / "evdspy" / "__version__.py"
    # p = Path() / "__version__.py"
    if test:
        return Read(p)
    if p.is_file():
        c = Read(p)
        c = c.replace("version", "")
        c = c.replace("=", "").strip()
    else:
        raise "Version not found"
    return c


def get_prev_version_instance():
    # print(get_previous())
    return create_version_instance(get_previous())


def get_next_version(increment_=True, pre_release=True, verbose=True):
    """ M A I N   F U N C """
    prev_instance = get_prev_version_instance()

    if not increment_:
        next_instance = prev_instance
    else:
        next_instance = increment(pre_release, prev_instance)
    if verbose:
        print("-" * 15)
        print("CURRENT VERSION", prev_instance)
        print(f"increment : {increment_}")
        print(f"pre_release : {pre_release}")
        print("NEW VERSION", next_instance)

    return next_instance


def test_create_version_instance():
    assert create_version_instance("1.0.17.2rc2") == VersionParts(1, 0, 17, 2, 2, True)
    assert create_version_instance("1.0.17.2") == VersionParts(1, 0, 17, 2, 0, False)
    assert create_version_instance("1.0.17.3rc4") == VersionParts(1, 0, 17, 3, 4, True)


def test_get_next_version():
    for item in range(100):
        # inc = random.choice((True, False,))
        inc = True
        pre = random.choice((True, False,))



        n = get_next_version(increment_=inc, pre_release=pre)

        assert n is not None


test_create_version_instance()
test_get_next_version()

# pytest -v evdspy/EVDSlocal/scratches/verser.py
