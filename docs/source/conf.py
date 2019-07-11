# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))
from PyFlow.Core.version import currentVersion
# -- Project information -----------------------------------------------------

project = 'PyFlow'
copyright = '2019, Ilgar Lunin, Pedro Cabrera'
author = 'Ilgar Lunin, Pedro Cabrera'

# The full version, including alpha/beta/rc tags
release = currentVersion().__str__()

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx'
]

source_suffix = {
    '.rst': 'restructuredtext',
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'blinker': ('https://pythonhosted.org/blinker', None)
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_context = {
    'css_files': [
        '_static/theme_overrides.css'
    ]
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

autodoc_default_options = {
    'member-order': 'bysource',
    'special-members': '__init__',
    'exclude-members': '__weakref__'
}

master_doc = 'index'