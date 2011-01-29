#!/usr/bin/env python
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

setup(
    name="gossipr",
    version="0.1",
    description="Jabber chatroom logger (logs XMPP MUC rooms and provides web interface) using Python Twisted",
    author="Brian Muller",
    author_email="bamuller@gmail.com",
    license="GPLv3",
    url="http://findingscience.com/gossipr",
    packages=["gossipr"],
    package_data={'gossipr': ["static/*/*"]},
    requires=["twisted.enterprise.adbapi", "twisted.words", "twistar"]
)
