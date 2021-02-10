# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='toutatis',
    version="1.22",
    packages=find_packages(),
    author="megadose",
    install_requires=["argparse","tabulate","httpx","tqdm","unicodecsv"],
    description="Toutatis is a tool that allows you to extract information from instagrams accounts such as e-mails, phone numbers and more",
    long_description="",
    include_package_data=True,
    url='http://github.com/megadose/toutatis',
    entry_points = {'console_scripts': ['toutatis = toutatis.core:main']},
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
