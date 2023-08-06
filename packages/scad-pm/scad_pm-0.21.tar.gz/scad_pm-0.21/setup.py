import setuptools
from setuptools import setup

setup(
    name='scad_pm',
    version='0.21',
    scripts=['src/scad_pm'],
    package_dir={"scad_pm": "/src"},
    packages=setuptools.find_packages(),
    install_requires=[
        'pyyaml',
        'dataclasses_json',
        'scopeton'
   ]
)