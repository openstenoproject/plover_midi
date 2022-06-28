#!/usr/bin/env python3

from setuptools import setup

from plover_build_utils.setup import BuildPy, BuildUi, Develop


BuildPy.build_dependencies.append('build_ui')
if 'plover_build_utils.pyqt:gettext' in BuildUi.hooks:
    BuildUi.hooks.remove('plover_build_utils.pyqt:gettext')
Develop.build_dependencies.append('build_py')
cmdclass = {
    'build_py': BuildPy,
    'build_ui': BuildUi,
    'develop': Develop,
}

setup(cmdclass=cmdclass)
