from setuptools import setup


setup(
    name='drf-httpsig',
    version='1.0-dev',
    url='https://github.com/ahknight/drf-httpsig',

    license='LICENSE.txt',
    description='HTTP Signature support for Django REST framework',
    long_description=open('README.rst').read(),

    install_requires=[
        'Django>=1.6,<1.7'
        'djangorestframework',
        'pycrypto',
        'httpsig'
    ],
    dependency_links=[
        'https://github.com/ahknight/httpsig.git#egg=httpsig',
    ],

    author='Adam Knight',
    author_email='adam@movq.us',
    packages=['drf_httpsig'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
    ]
)
