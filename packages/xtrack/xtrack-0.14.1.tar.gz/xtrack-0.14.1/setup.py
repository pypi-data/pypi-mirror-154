# copyright ############################### #
# This file is part of the Xtrack Package.  #
# Copyright (c) CERN, 2021.                 #
# ######################################### #

from setuptools import setup, find_packages, Extension

#######################################
# Prepare list of compiled extensions #
#######################################

extensions = []

#########
# Setup #
#########

setup(
    name='xtrack',
    version='0.14.1',
    description='Tracking library for particle accelerators',
    url='https://github.com/xsuite/xtrack',
    author='Riccard De Maria, Giovanni Iadarola',
    packages=find_packages(),
    ext_modules = extensions,
    include_package_data=True,
    install_requires=[
        'numpy>=1.0',
        'scipy',
        'xobjects',
        'xpart',
        'xdeps'
        ]
    )
