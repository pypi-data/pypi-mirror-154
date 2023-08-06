#!/bin/env python
# -*- coding:utf8 -*-
import os
import setuptools

long_description="""
This is a tool, customize an ISO image containing only required RPM packages based on the the EulerOS CD-ROM image
"""

packages=[]

setuptools.setup(
    name="isocut",
    version="1.0",
    author="Chunyi Zhu",
    author_email="zhuchunyi@huawei.com",
    description="Image tailor custom tool",
    long_description=long_description,
    packages=setuptools.find_packages()
)

