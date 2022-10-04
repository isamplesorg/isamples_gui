"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    # This is required in order to make the imports work -- otherwise it gets flattened
    "packages": ["isamples_frictionless"],
    "resources": ["isamples_frictionless/isamples_simple_schema.json"]
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
