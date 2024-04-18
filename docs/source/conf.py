
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
html_build_dir = '../docs'
project = 'evdspy'
copyright = '2024, Sermet Pekin'
author = 'Sermet Pekin'
release = 'v1.1.19'
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.autosummary',
    # 'myst_parser'
]
templates_path = ['_templates']
exclude_patterns = []
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['static']
# extensions = ['myst_parser']
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}
import os
import inspect
from sphinx.util import logging
logger = logging.getLogger(__name__)
import time
def linkcode_resolve(domain, info):
    print(domain, info, "Domain info ")
    time.sleep(2)
    if domain != 'py':
        return None
    if not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    return "https://github.com/SermetPekin/evdspy-repo/%s.py" % filename
def linkcode_resolveOLD(domain, info):
    if domain != 'py' or not info['module']:
        return None
    try:
        mod = __import__(info['module'])
        for part in info['module'].split('.')[1:]:
            mod = getattr(mod, part)
        obj = mod
        if 'fullname' in info:
            obj = getattr(obj, info['fullname'])
        filename = inspect.getsourcefile(obj)
        filename = os.path.relpath(filename, start=os.path.dirname(mod.__file__))
        lines, _ = inspect.getsourcelines(obj)
    except Exception as e:
        logger.warning(f"Could not get source link for module {info['module']} due to {e}")
        return None
    tag_or_branch = 'main'  # or 'master' or the specific tag if versioned
    path_to_file = os.path.join('path_to_repository', filename)
    return f"https://github.com/SermetPekin/evdspy-repo/blob/{tag_or_branch}/{path_to_file}#L{lines[0]}"