# -*- coding: utf-8 -*-
"""
This is a setup.py script to install ShakeNBreak
"""

from setuptools import setup, find_packages

setup(
    name="shakenbreak",
    version="0.2",
    description="Package to generate and analyse distorted defect structures, in order to "
    "identify ground-state and metastable defect configurations.",
    author="Irea Mosquera, Seán Kavanagh",
    author_email="irea.lois.20@ucl.ac.uk",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        "doped>=0.0.5",
        "numpy",
        "pymatgen",
        "matplotlib",
        "ase",
        "pandas",
        "seaborn",
        "hiphive",
        "monty",
    ],
    extras_require={"tests": ["pytest", "pytest-mpl"]},
    setup_requires=['setuptools_scm'],
    include_package_data=True
)
