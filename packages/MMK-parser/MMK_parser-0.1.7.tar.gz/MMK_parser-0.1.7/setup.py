from setuptools import setup, find_packages


setup(
    name='MMK_parser',
    version='0.1.7',
    license='MIT',
    author="MMK_group",
    author_email='maciekgoncerzewicz@gmail.com',
    packages=['MMK_parser'],
    package_dir={'': './'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='example project',
    install_requires=[
        'bs4',
        'requests',
    ],
)