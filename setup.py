#!/usr/bin/env python3

from setuptools import setup

from plover_build_utils.setup import BuildPy, BuildUi


BuildPy.build_dependencies.append('build_ui')
cmdclass = {
    'build_py': BuildPy,
    'build_ui': BuildUi,
}

setup(cmdclass=cmdclass)
