# -*- coding: utf-8 -*-
import setuptools
from eurekapy import version

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="eurekapy",
    version=version,
    author="hexer",
    author_email="hexu0614@gmail.com",
    description="A eureka client written in python. Support registering your python component to Eureka Server, as well as calling remote services by pulling the the Eureka registry. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["eurekapy"],
    install_requires=[
        "ifaddr",
        "dnspython"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
