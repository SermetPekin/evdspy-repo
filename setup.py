from setuptools import setup, find_packages
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

# from setup_get_next_version import get_next_version

from verser import get_next_version, Project

PRE_RELEASE = True
INCREMENT = True

# from setup_config import root_version, test_environment, cmd_file, package_name
STABLE_FORCE = True
default_vers = "1.0.17.10"

STABLE_VERSION = get_next_version(
    Project(package_name="evdspy",
            default_version=default_vers,
            version_file_path=Path() / "evdspy" / "__version__.py"),
    increment_=INCREMENT,
    pre_release=PRE_RELEASE,

)

p = Path() / "evdspy" / "__version__.py"
print(p.is_file())

# exit()
print("Getting next version", STABLE_VERSION)

# STABLE_VERSION = "1.0.17.10"
USER = ""
if USER == "author":
    # from setup_config import *
    ...
else:
    from setup_config_pub import *
# --------------------------------------------------------------------------------------
#   get command line args
# --------------------------------------------------------------------------------------
import sys


def arg_acc(argv=None):
    if argv is None:
        argv = sys.argv
    obj = {}
    for index, key in enumerate(argv):
        key = str(key)
        if key.startswith("--"):
            value = None
            if len(argv) > index + 1:
                value = argv[index + 1]
            key = key[2:]
            obj.update({key: value})
    return obj


# --------------------------------------------------------------------------------------
# T E S T   E N V I R O N M E N T
# --------------------------------------------------------------------------------------
rf"""
 Usage 
    echo on 
    cd C:\Users\Username\PycharmProjects\evdspy
    python setup.py bdist_wheel --universal --folder C:\Username\SomeFolder\Env
    @params 
        --folder : Test Env folder \
        --stable : status (dev : False / prod : True )
"""

print(sys.argv)
args_dict = arg_acc()

""" Test Env folder """
folder = args_dict.get("folder", None)

"""Stable Version or Development with time and date"""
stable_param = args_dict.get("stable", None)
stable = True if stable_param == "True" or STABLE_FORCE else False
# assert stable == False
if folder:
    test_environment = folder
    sys.argv = sys.argv[0: 3]


def create_env_folder(test_environment_):
    path = Path(test_environment)
    if not path.is_dir():
        import os
        os.makedirs(path)


if test_environment:
    create_env_folder(test_environment)
    """ nick name for the env for simplicity"""
    nick_name_for_env = Path(test_environment).parts[-1]
    """ command file to install development/pord version in local area"""
    cmd_file = f"{cmd_file}-{nick_name_for_env}.cmd"


def get_test_env():
    return test_environment


@dataclass
class SetupOptions:
    version: str = root_version
    long_des: str = ""
    test_folder: Path = None

    def __post_init__(self):
        self.main()
        if get_test_env():
            self.create_run_command()

    def get_stable_version(self):
        return STABLE_VERSION

    def get_develop_version(self):
        if stable or STABLE_FORCE:
            self.version = self.get_stable_version()
            return self.version
        version = datetime.now().strftime("%d.%b_%H.%M")
        version = f"{root_version}.bd.{version}"
        self.version = version
        return version

    def get_commands_content(self):
        self.root_folder = Path(__file__).parent

        build_content = f"""REM   Build file for evdspy 
echo on 
cd {self.root_folder}
python setup.py bdist_wheel --universal

"""
        content = \
            rf"""REM   Run file for {package_name}
rem 
echo on 
rem cd {test_environment}

poetry shell
echo {self.test_cmd_file}

pip uninstall {package_name}

rem pip install {self.root_folder}\dist\evdspy-{self.version}-py2.py3-none-any.whl --force-reinstall --no-deps
pip install {self.root_folder}\dist\evdspy-{self.version}-py2.py3-none-any.whl
python
from {package_name} import *
version() 
check() 
menu()
"""

        return content

    def create_run_command(self):
        self.test_folder = Path(test_environment)
        self.test_cmd_file = self.test_folder / cmd_file
        self.write(self.test_cmd_file, self.get_commands_content())

    def main(self):
        print(f"building ... version:{self.get_develop_version()}")
        parent = Path(__file__).parent
        self.read_me_file()
        file_name = Path() / parent / "evdspy" / "__version__.py"

        self.write(file_name, f"#{self.get_develop_version()}")

    def write(self, file_name, content):
        with open(file_name, 'w') as f:
            f.write(content)

    def read_me_file(self):
        with open("README.md", "r") as file_:
            long_des = file_.read()
        self.long_des = long_des
        return long_des


# --------------------------------------------------------------------------------------
# ------------------------------------M A I N ------------------------------------------
# ------------------------------------M A I N ------------------------------------------
# ------------------------------------M A I N ------------------------------------------
setup_options = SetupOptions()
# ------------------------------------M A I N ------------------------------------------
# ------------------------------------M A I N ------------------------------------------
# ------------------------------------M A I N ------------------------------------------


#
# --------------------------------------------------------------------------------------
# the setup
project_urls = {
    'Homepage': 'https://github.com/SermetPekin/evdspy-repo',
    'Documentation': 'https://github.com/SermetPekin/evdspy-repo'
}

description_ = f"""
Python interface to make requests from EVDS API Server. Fast, efficient and user friendly solution. Caches results to avoid redundant requests. Creates excel files reading configuration text file that can be easily created from the menu or console. Provides visual menu to the user. It is extendable and importable for user's own python projects. 
"""

setup(
    name='evdspy',
    version=setup_options.version,
    description=description_,
    long_description=setup_options.long_des,
    long_description_content_type="text/markdown",
    project_urls=project_urls,
    url='https://github.com/SermetPekin/evdspy-repo',
    author='Sermet Pekin',
    author_email='sermet.pekin@gmail.com',
    license='MIT',
    keywords='evds, evdspy evdspy-repo',
    # package_dir={"": "evdspy"},

    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],

    packages=find_packages(
        exclude=('scratches', 'logs', 'docs', 'env', 'index.py', 'options.py')
    ),
    include_package_data=True,
    classifiers=[

        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Topic :: Office/Business :: Financial',
        'Programming Language :: Python :: Implementation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        "rich",
        "pandas",
        "requests",
        "numpy",
        "openpyxl",
        "psutil",

    ],
    exclude_package_data={

    },
    entry_points={
        'console_scripts': [
            'evdspy=evdspy:console_main',
        ],
    },
    extras_require={
        'dev': [],
        'docs': [],
        'testing': [],
    },

)
# --------------------------------------------------------------------------------------
