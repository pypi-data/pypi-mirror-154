
from setuptools import setup, find_packages

setup(
    name='scad_pm',
    version='0.18',
    scripts=['src/scad_pm'],
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'dataclasses_json',
        'scopeton'
   ]
)