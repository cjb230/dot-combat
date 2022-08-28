"""Sphinx configuration."""
project = "Dot Combat"
author = "James Barton"
copyright = "2022, James Barton"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
