import setuptools
from setuptools import setup

setup(
    name='scad_pm',
    version='0.20',
    scripts=['src/scad_pm'],
    package_dir={"": "src"},
    install_requires=[
        'pyyaml',
        'dataclasses_json',
        'scopeton'
   ]
)