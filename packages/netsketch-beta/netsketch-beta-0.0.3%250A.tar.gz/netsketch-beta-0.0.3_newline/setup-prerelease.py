#!/usr/bin/env python

from distutils.core import setup

long_desc = 'Licensed under the generic MIT License. \"netsketch\" can either be downloaded from the ' \
            'installed via \"pip\".'
prerelease_version = ''

with open("version.txt", "r", encoding="utf-8") as fh:
    prerelease_version = fh.read()
    fh.close()

setup(name='netsketch-beta',
      version=prerelease_version,
      py_modules=['netsketch'],
      description='NetSketch [Beta] | The Network Visualizer',
      long_description=long_desc,
      long_description_content_type='text/markdown',
      author='Tushar Iyer',
      author_email='',
      url='https://github.com/tushariyer/netsketch',
      project_urls={
              "Bug Tracker": "https://github.com/tushariyer/netsketch/issues",
          }
      )