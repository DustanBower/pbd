#!/usr/bin/env python2

from distutils.core import setup

setup(name='pbd',
      version='0.1.1',
      description='Scripts for daemonizing pianobar.',
      author='Dustan Bower',
      author_email='dustan.bower@gmail.com',
      scripts=['pbd', 'pbevent', 'pb.py'],
      data_files=[('share/pbd', ['BUGS', 'COPYING', 'README', 'TODO'])])
