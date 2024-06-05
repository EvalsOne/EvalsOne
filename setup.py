from setuptools import setup, find_packages

setup(
    name='evalsone',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'pydantic'
    ],
    author='EvalsOne',
    author_email='contact@evalsone.com',
    description='A Tiny Python client of EvalsOne for adding samples into a dataset.',
)