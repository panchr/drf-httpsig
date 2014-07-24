#!/usr/bin/env python
from setuptools import setup, find_packages

# versioneer config
import versioneer
versioneer.versionfile_source = 'drf_httpsig/_version.py'
versioneer.versionfile_build = 'drf_httpsig/_version.py'
versioneer.tag_prefix = 'v'                     # tags are like v1.2.0
versioneer.parentdir_prefix = 'drf-httpsig-'    # dirname like 'myproject-1.2.0'

# create long description
with open('README.rst') as file:
    long_description = file.read()
with open('CHANGELOG.rst') as file:
    long_description += '\n\n' + file.read()

# Tox testing command
from setuptools.command.test import test as TestCommand
import sys

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)

cmdclass = {'test': Tox}
cmdclass.update(versioneer.get_cmdclass())

setup(
    name='drf-httpsig',
    version=versioneer.get_version(),
    cmdclass=cmdclass,
    description='HTTP Signature support for Django REST framework',
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        'Framework :: Django',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    author='Adam Knight',
    author_email='adam@movq.us',
    url='https://github.com/ahknight/drf-httpsig',
    license='MIT',
    packages=find_packages(),
    zip_safe=True,
    install_requires=[
        'django>=1.6,<1.7',
        'djangorestframework>=2.3,<2.4',
        'httpsig>=1.1,<1.2'
    ],
    tests_require=['tox'],
)
