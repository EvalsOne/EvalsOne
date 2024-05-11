from setuptools import setup, find_packages

setup(
    name='evalsone',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'pydantic'
    ],
    author='EvalsOne',
    author_email='contact@evalsone.com',
    description='A Tiny Python client for EvalsOne API'
)