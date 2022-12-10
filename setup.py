from setuptools import setup, find_packages

from setup_helper import arg_acc, check_stable, create_env_folder, get_cmd_file, get_test_env, get_args_dict
from pathlib import Path
import sys

""" Parameters for build and cmd file creator """
from setup_config_pub import package_name

PRE_RELEASE = False
INCREMENT = True
STABLE_FORCE = True
default_vers = "1.0.18"

# ------------------- VERSER latest-------------------
from verser import *


def force_pkg_for_the_latest_version(package_name_to_check):
    import pkg_resources
    current_version = pkg_resources.get_distribution(package_name_to_check).version
    print(f"{package_name_to_check} : current_version : {current_version}")
    latest_version = next_version_pypi(package_name_to_check, increment_choice=False)
    print(f"{package_name_to_check} : latest_version : {latest_version}")
    return current_version == latest_version


check_ = force_pkg_for_the_latest_version("verser")

# assert check_ is True

project = Project(package_name=package_name,
                  default_version=default_vers,
                  version_file_path=Path() / package_name / "__version__.py")
part = 'patch'  # 'minor' '1.1.11rc1'
STABLE_VERSION =  next_version(project, pypi=True, write=True, part=part)
# ----------------------------------------------------

"""STABLE_VERSION for TEMP FORCE HERE"""
# STABLE_VERSION = "1.0.18"

# --------------------------------------------------------------------------------------
#   get command line args
# --------------------------------------------------------------------------------------
args_dict_GLOBAL = get_args_dict(sys.argv)
# args_temp = sys.argv
"""Chop extra args for standard build procedure"""
sys.argv = sys.argv[0: 3]


def get_args_dict_runtime():
    """functional approach as possible"""
    return args_dict_GLOBAL


# --------------------------------------------------------------------------------------
# ------------------------------------M A I N ------------------------------------------
# ------------------------------------M A I N ------------------------------------------
# ------------------------------------M A I N ------------------------------------------
from setup_options_class import SetupOptions

setup_options = SetupOptions(
    stable_version=STABLE_VERSION,
    stable_force=STABLE_FORCE,
    test_environment=get_test_env(get_args_dict_runtime),
    get_args_dict_runtime=get_args_dict_runtime
)
# ------------------------------------M A I N ------------------------------------------
# ------------------------------------M A I N ------------------------------------------
# ------------------------------------M A I N ------------------------------------------


#
# --------------------------------------------------------------------------------------
# the setup
project_urls = {
    'Homepage': f'https://github.com/SermetPekin/{package_name}-repo',
    'Documentation': f'https://github.com/SermetPekin/{package_name}-repo'
}

description_ = f"""
Python interface to make requests from EVDS API Server. Fast, efficient and user friendly solution. Caches results to avoid redundant requests. Creates excel files reading configuration text file that can be easily created from the menu or console. Provides visual menu to the user. It is extendable and importable for user's own python projects. 
"""

setup(
    name=package_name,
    version=setup_options.version,
    description=description_,
    long_description=setup_options.long_des,
    long_description_content_type="text/markdown",
    project_urls=project_urls,
    url=f'https://github.com/SermetPekin/{package_name}-repo',
    author='Sermet Pekin',
    author_email='sermet.pekin@gmail.com',
    license='MIT',
    keywords=f'{package_name}, {package_name} {package_name}-repo',
    # package_dir={"": "evdspy"},

    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],

    packages=find_packages(
        exclude=('scratches', 'APIKEY_FOLDER', 'tests', 'logs', 'docs', 'env', 'index.py', 'options.py')
    ),
    include_package_data=True,
    classifiers=[

        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Topic :: Office/Business :: Financial',
        'Programming Language :: Python :: Implementation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        "rich>=12.5.1",
        "pandas>=0.19.2",
        "requests>=2.28.1",
        "openpyxl>=3.0.10",
        "numpy>=1.5.0"
    ],
    exclude_package_data={

    },
    python_requires='>=3',

    entry_points={
        'console_scripts': [
            f'{package_name}={package_name}:console_main',
        ],
    },
    extras_require={
        'dev': ["verser"],
        'docs': [],
        'testing': [],
    },

)
# --------------------------------------------------------------------------------------
