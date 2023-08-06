import os

from setuptools import setup

PROJECT_ROOT, _ = os.path.split(__file__)

NAME = 'ferris-k8s-cli'
EMAILS = 'bal@ballab.com'
AUTHORS = 'Balaji Bal'
VERSION = '0.0.1'

URL = 'https://github.com/Ferris-Labs/ferris-k8s-cli'
LICENSE = 'Apache2.0'


SHORT_DESCRIPTION = 'Wrapper for Kubernetes API for usage within Ferris Platform.'



try:
    import pypandoc
    DESCRIPTION = pypandoc.convert(os.path.join(PROJECT_ROOT, 'README.md'),
                                   'rst')
except (IOError, ImportError):
    DESCRIPTION = SHORT_DESCRIPTION

INSTALL_REQUIRES = open(os.path.join(PROJECT_ROOT, 'requirements.txt')). \
        read().splitlines()


setup(
    name=NAME,
    version=VERSION,
    author=AUTHORS,
    author_email=EMAILS,
    packages=[
        'ferris_k8s',
        ],
    install_requires=INSTALL_REQUIRES,
    include_package_data = True,
    url=URL,
    download_url='https://github.com/Ferris-Labs/ferris-k8s-cli/archive/{0}.tar.gz'.format(VERSION),
    description=SHORT_DESCRIPTION,
    long_description=DESCRIPTION,
    license=LICENSE,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Logging',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)