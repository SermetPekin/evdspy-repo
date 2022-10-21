from setuptools import setup, find_packages
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
# from setup_config import root_version, test_environment, cmd_file, package_name
STABLE_FORCE = True
STABLE_VERSION = "1.0.17.6rc4"
USER = ""
if USER =="author" :
    # from setup_config import *
    ...
else :
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
    python setup.py bdist_wheel --universal --folder

"""

print(sys.argv)
args_dict = arg_acc()
folder = args_dict.get("folder", None)
stable_param = args_dict.get("stable", None)
stable = True if stable_param == "True" else False
if STABLE_FORCE  :
    stable = True

if folder:
    test_environment = folder
    sys.argv = sys.argv[0: 3]
print(test_environment)
print(sys.argv)

def create_env_folder(test_environment_):
    path =Path(test_environment)
    if not path.is_dir():
        import os
        os.makedirs(path)

if test_environment : 
    create_env_folder(test_environment)
    nick_name_for_env = Path(test_environment).parts[-1]
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
        if get_test_env() : 
            self.create_run_command()

    def get_stable_version(self):
        return STABLE_VERSION

    def get_develop_version(self):
        if stable or STABLE_FORCE :
            self.version = version = self.get_stable_version()
            return version
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
        file_name = Path() / parent / "evdspy" / "EVDSlocal" / "version__.py"
        file_name2 = Path() / parent / "evdspy" / "__version__.py"
        
        self.write(file_name, f"# {self.get_develop_version()}")
        self.write(file_name2, f"version= '{self.get_develop_version()}'")

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
setup(
        name='evdspy',
        version=setup_options.version,
        description='evdspy',
        long_description=setup_options.long_des,
        long_description_content_type="text/markdown",
        url='',
        author='Sermet Pekin',
        author_email='sermet.pekin@gmail.com',
        license='MIT',
        keywords='evds, evdspy evdspy-repo',
        # package_dir={"": "evdspy"},
        packages=find_packages(
                exclude=('scratches', 'logs', 'docs', 'env', 'index.py', 'options.py')
        ),
        include_package_data=True,
        install_requires=[
                "rich",
                "pandas",
                "requests",
                "numpy",
                "openpyxl",
                "psutil",
                "pytest",

        ],
        exclude_package_data={

        },

        extras_require={
                'dev': [],
                'docs': [],
                'testing': [],
        },
        classifiers=[],
)
# --------------------------------------------------------------------------------------
