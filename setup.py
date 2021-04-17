#!/usr/bin/env python3

__requires__ = '''
plover>=4.0.0.dev3
setuptools>=30.3.0
'''

from setuptools import setup

from plover_build_utils.setup import BuildPy, BuildUi


BuildPy.build_dependencies.append('build_ui')
cmdclass = {
    'build_py': BuildPy,
    'build_ui': BuildUi,
}

setup(cmdclass=cmdclass)
