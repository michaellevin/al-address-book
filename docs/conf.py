# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Address App"
copyright = "2024, Michael Levin"
author = "Michael Levin"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".venv", ".vscode"]
autodoc_default_options = {
    "member-order": "bysource",  # "groupwise", "alphabetical", "bysource"
    # "special-members": "__init__", # "__init__", "__call__", "__getitem__", "__setitem__"
    "exclude-members": "__weakref__",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"  # "alabaster"
html_static_path = ["_static"]

import os
import sys

sys.path.insert(0, os.path.abspath("../"))
from address_app import __version__

version = __version__


def skip_internal_members(app, what, name, obj, skip, options):
    # print(name, obj, skip, options)
    return name.startswith("_")


def setup(app):
    app.connect("autodoc-skip-member", skip_internal_members)
