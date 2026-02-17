"""Sphinx configuration for METIS Simulations documentation."""

project = "METIS Simulations"
copyright = "2024, AstarVienna"
author = "Jennifer Karr, Hugo Buddelmeijer, Fabian Haberhauer"

extensions = []

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = []

html_theme_options = {
    "navigation_depth": 3,
}
