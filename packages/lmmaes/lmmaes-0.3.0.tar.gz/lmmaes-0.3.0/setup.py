# Thanks `https://github.com/pypa/sampleproject`!!

from setuptools import setup, find_packages
from os import path
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'VERSION'), 'r', encoding='utf-8') as f:
    version = f.read().strip()
with open(path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(here, 'LICENSE.txt'), 'r', encoding='utf-8') as f:
    license = f.read()

setup(
    name              = 'lmmaes',
    version           = version,
    description       = 'Limited-Memory Matrix Adaptation Evolution Strategy',
    long_description  = long_description,
    long_description_content_type='text/markdown',
    url               = 'https://github.com/giuse/lmmaes',
    author            = 'Giuseppe Cuccu',
    author_email      = 'giuseppe.cuccu@gmail.com',
    license           = license,
    classifiers       = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords         = 'blackbox optimization evolution strategies large scale',
    packages         = find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires  = '>=3.6',
    install_requires = ['numpy'],
    project_urls={
        'Bug Reports' : 'https://github.com/giuse/lmmaes/issues',
        'Source'      : 'https://github.com/giuse/lmmaes/',
    },
    download_url      = f"https://github.com/giuse/lmmaes/archive/{version}.tar.gz",
)
