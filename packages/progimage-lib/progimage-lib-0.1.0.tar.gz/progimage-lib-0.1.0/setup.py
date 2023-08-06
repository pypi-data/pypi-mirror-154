import setuptools
from setuptools import setup

setup(
    name='progimage-lib',
    version='0.1.0',
    description='Python package for ProgImage',
    url='https://github.com/chitnguyen169/progimage-lib',
    author='Chi Nguyen',
    author_email='chi.nguyen.gmb@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=['requests==2.27.1'],

    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
