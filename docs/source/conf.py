# Configuration file for the Sphinx documentation builder.
# See: https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import os
import sys

# Projekt-Root-Verzeichnis (eine Ebene über "src" und "tests")
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
project = 'Helmholtz Resonator Calculator'
copyright = '2025, Rösch F, Schön J, van Dijk T, Verhoeven J'
author = 'Rösch F, Schön J, van Dijk T, Verhoeven J'
release = '0.1'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',   # Für Google-/NumPy-Style Docstrings
]

autosummary_generate = True
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']