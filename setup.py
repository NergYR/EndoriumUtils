"""
Script d'installation pour EndoriumUtils
"""

import os
from setuptools import setup, find_packages

# Lire la description longue depuis README.md
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    # Fallback si README.md n'est pas trouvé
    long_description = """
    EndoriumUtils - Bibliothèque d'utilitaires réutilisables pour les projets Endorium
    
    Ce module fournit des fonctionnalités communes pour la gestion des logs et des versions.
    """

# Lire la version depuis version.txt
with open("version.txt", "r") as f:
    version = f.read().strip()

setup(
    name="EndoriumUtils",
    version=version,
    author="Energetiq",
    author_email="energetiq@outlook.com",
    description="Utilitaires communs pour les projets Endorium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NergYR/EndoriumUtils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    keywords="logging, version management, utilities",
    project_urls={
        "Bug Reports": "https://github.com/NergYR/EndoriumUtils/issues",
        "Source": "https://github.com/NergYR/EndoriumUtils",
    },
)
