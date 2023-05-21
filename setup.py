#!/usr/bin/env python3
from setuptools import setup

setup(
    name = 'ankiadderall',
    version = '0.1.0',
    description='a command line program for creating anki card using AnkiConnect API.',
    author='Constantin Hong',
    author_email='hongconstantin@gmail.com',
    url='https://github.com/Constantin1489/ankistreamadd',
    maintainer='Constantin Hong',
    maintainer_email='hongconstantin@gmail.com',
    packages = ['ankiadderall'],
    data_files = [('share/man/man1', ['ankiadderall.1'])],
    python_requires='>=3.9',
    project_urls = {
        'Documentation': 'https://github.com/Constantin1489/ankistreamadd#readme',
        'Source': 'https://github.com/Constantin1489/ankistreamadd',
        'Tracker': 'https://github.com/Constantin1489/ankistreamadd/issues',
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
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        ],
    entry_points = {
        'console_scripts' : [
            'ankiadderall = ankiadderall.__main__:main'
        ]
    })
