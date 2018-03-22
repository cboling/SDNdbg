#!/usr/bin/env python
"""
Copyright (c) 2015 - present.  Boling Consulting Solutions, BCSW.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
from setuptools import setup

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='SDNdbg',
    version='0.0.2',
    author='Boling Consulting Solutions, bcsw.net',
    author_email='info@bcsw.net',
    description=('SDN Debugging Suite'),
    license='Apache License 2.0',
    keywords='sdn nfv openstack onos',
    url='http://bcsw.net/SDNdbg',
    packages=['sdndbg', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Topic :: System :: Networking :: Monitoring',
        'Programming Language :: Python 2.7',
        'License :: OSI Approved :: Apache Software License',
    ],
)
