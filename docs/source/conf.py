# Configuration file for the Sphinx documentation builder.
# See: https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import os
import sys

# Stelle sicher, dass sowohl src als auch tests importierbar sind
sys.path.insert(0, os.path.abspath('../../src'))     # z.B. für calculation, app_control etc.
sys.path.insert(0, os.path.abspath('../../tests'))   # z.B. für test_geometry etc.

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
    'sphinx.ext.napoleon',  # Unterstützt Google- und NumPy-Style Docstrings
]

autosummary_generate = True  # Automatisch .rst-Dateien erzeugen bei 'make html'

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
