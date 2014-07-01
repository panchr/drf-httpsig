#!/usr/bin/env python2
from setuptools import setup, find_packages
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

# versioneer config
import versioneer
versioneer.versionfile_source = 'drf_httpsig/_version.py'
versioneer.versionfile_build = 'drf_httpsig/_version.py'
versioneer.tag_prefix = 'v'                     # tags are like v1.2.0
versioneer.parentdir_prefix = 'drf-httpsig-'    # dirname like 'myproject-1.2.0'

# create long description
with open('README.rst') as file:
    long_description = file.read()
with open('CHANGES.rst') as file:
    long_description += '\n\n' + file.read()

cmdclass = {'test': Tox}
cmdclass.update(versioneer.get_cmdclass())

setup(
    name='drf-httpsig',
    version=versioneer.get_version(),
    cmdclass=cmdclass,
    description='HTTP Signature support for Django REST framework',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
    ],
    author='Adam Knight',
    author_email='adam@movq.us',
    url='https://github.com/ahknight/drf-httpsig',
    license='MIT',
    packages=find_packages(),
    zip_safe=True,
    install_requires=[
        'djangorestframework>=2.3,<2.4',
        'httpsig'
    ],
    tests_require=['tox'],
)
