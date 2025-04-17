"""
Script d'installation pour EndoriumUtils
"""

from setuptools import setup, find_packages

# Lire la description longue depuis README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="EndoriumUtils",
    version="1.0.0",
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
    ],
    python_requires=">=3.6",
)
