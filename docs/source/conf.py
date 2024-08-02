# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from sphinx.util import logging
import os

html_build_dir = '../docs'  # Directory for HTML build output

project = 'evdspy'
copyright = '2024, Sermet Pekin'
author = 'Sermet Pekin'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''

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
    # 'myst_parser'  # Uncomment if you use MyST markdown
]

templates_path = ['_templates']
exclude_patterns = []

doctest_global_setup = """
# Any global setup code for doctests
"""

# Disable execution of doctest blocks
doctest_test_doctest_blocks = 'false'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

<<<<<<< HEAD
html_theme = 'sphinx_book_theme'  # Theme for HTML output
html_static_path = ['_static']  # Static files path

=======
html_static_path = ['static']
os.makedirs(html_static_path[0])
>>>>>>> f106125c794f7eeb8348e421c7d0ba4b3edee5e1
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

<<<<<<< HEAD
from sphinx.util import logging
=======

>>>>>>> f106125c794f7eeb8348e421c7d0ba4b3edee5e1
logger = logging.getLogger(__name__)

def linkcode_resolve(domain, info):
    """
    Resolve the link to the source code for documentation.
    """
    print(domain, info, "Domain info ")
    if domain != 'py':
        return None
    if not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    return f"https://github.com/SermetPekin/evdspy-repo/{filename}.py"
