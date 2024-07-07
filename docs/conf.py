# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import datetime

import HinetPy

# -- Project information -----------------------------------------------------
year = datetime.date.today().year
project = "HinetPy"
author = "Dongdong Tian"
copyright = f"2014-{year}, {author}"  # noqa: A001

# The full version, including alpha/beta/rc tags
version = HinetPy.__version__
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

html_context = {
    "menu_links": [
        (
            '<i class="fa fa-github fa-fw"></i> Source Code',
            "https://github.com/seisman/HinetPy",
        ),
        (
            '<i class="fa fa-globe fa-fw"></i> NIED Hi-net',
            "https://www.hinet.bosai.go.jp/",
        ),
        (
            '<i class="fa fa-book fa-fw"></i> Documentation',
            "https://seisman.github.io/HinetPy/",
        ),
        (
            '<i class="fa fa-book fa-fw"></i> 中文文档',
            "https://seisman.github.io/HinetPy/zh_CN/",
        ),
    ]
}

# autodoc options
autodoc_member_order = "bysource"
autoclass_content = "both"
napoleon_numpy_docstring = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_references = True

# intersphinx configurations
intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}

# Chinese translation
locale_dirs = ["locale/"]  # path is example but recommended.
gettext_compact = False  # optional.
