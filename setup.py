#!/usr/bin/env python3
from setuptools import setup

setup(
    name = 'trrc',
    version = '0.1.3',
    description='a command-line program for creating anki card using AnkiConnect API.',
    author='Constantin Hong',
    author_email='hongconstantin@gmail.com',
    url='https://github.com/Constantin1489/trrc',
    maintainer='Constantin Hong',
    maintainer_email='hongconstantin@gmail.com',
    readme = "README.md",
    packages = ['trrc'],
    data_files = [
        ('share/man/man1', ['docs/trrc.1']),
        ('share/bash-completion/completions', ['scripts/bash/trrc']),
        ('share/zsh/site-functions', ['scripts/zsh/_trrc'])
        ],
    python_requires='>=3.9',
    install_requires=[
        "requests",
        "tomlkit",
        "tomli_w",
        ],
    project_urls = {
        'Documentation': 'https://github.com/Constantin1489/trrc#readme',
        'Source': 'https://github.com/Constantin1489/trrc',
        'Tracker': 'https://github.com/Constantin1489/trrc/issues',
        },
    classifiers=[
        'Intended Audience :: Education',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Topic :: Education',
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        ],
    entry_points = {
        'console_scripts' : [
            'trrc = trrc.__main__:main'
        ]
    })
