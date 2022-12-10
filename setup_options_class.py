from setup_helper import *
from datetime import datetime
from setup_config_pub import root_version, package_name
import typing as t
from dataclasses import dataclass


@dataclass
class SetupOptions:
    stable_version: str
    stable_force: bool
    test_environment: t.Union[bool, str, Path]
    get_args_dict_runtime: t.Callable
    version: str = ''
    long_des: str = ''
    test_folder: Path = None

    def __post_init__(self):
        self.main()
        if get_test_env(self.get_args_dict_runtime):
            self.create_run_command()

    def get_stable_version(self):
        return self.stable_version

    def get_develop_version(self):
        stable = check_stable(self.stable_force, self.get_args_dict_runtime)
        if stable:
            self.version = self.get_stable_version()
            return self.version
        ## rest will be develop version
        version = datetime.now().strftime("%d.%b_%H.%M")
        version = f"{root_version}.bd.{version}"
        self.version = version
        return version

    def get_commands_content(self):
        self.root_folder = Path(__file__).parent

        build_content = f"""REM   Build file for {package_name}
echo on
cd {self.root_folder}
python setup.py bdist_wheel --universal

"""
        content = \
            rf"""REM   Run file for {package_name}
rem
echo on
rem cd {self.test_environment}

poetry shell
echo {self.test_cmd_file}

pip uninstall {package_name}

rem pip install {self.root_folder}\dist\{package_name}-{self.version}-py2.py3-none-any.whl --force-reinstall --no-deps
pip install {self.root_folder}\dist\{package_name}-{self.version}-py2.py3-none-any.whl
rem python
rem from {package_name} import *

"""

        return content

    def create_run_command(self):
        self.test_folder = Path(self.test_environment)
        cmd_file_local = get_cmd_file(self.get_args_dict_runtime)
        self.test_cmd_file = self.test_folder / cmd_file_local
        self.write(self.test_cmd_file, self.get_commands_content())

    def main(self):
        print(f"building ... version:{self.get_develop_version()}")
        parent = Path(__file__).parent
        self.read_me_file()
        file_name = Path() / parent / package_name / "__version__.py"

        self.write(file_name, f"#{self.get_develop_version()}")

    def write(self, file_name, content):
        with open(file_name, 'w') as f:
            f.write(content)

    def read_me_file(self):
        with open("README.md", "r") as file_:
            long_des = file_.read()
        self.long_des = long_des
        return long_des
