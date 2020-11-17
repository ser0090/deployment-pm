#!/usr/bin/python3
from distutils.core import setup

setup(
    name='kafka',
    version='1.0',
    description='Deployment pm',
    # author_email='gward@python.net',
    # packages=['analytics'],
    install_requires=[
        'kafka-python',
        'jupyterlab',
    ]
)
