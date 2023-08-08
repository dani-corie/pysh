#!/usr/bin/env python3
# coding: utf-8

# This module provides some path constants and environment variables useful
# in the Pythonista3 iOS app

import os


class iOS_paths:

  local = os.path.join(os.environ['HOME'], 'Documents')
  icloud = '/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents'
  sitepkg = os.path.join(os.environ['HOME'], 'Documents/site-packages')

  def register_paths():
    os.environ['LOCAL'] = iOS_paths.local
    os.environ['ICLOUD'] = iOS_paths.icloud
    os.environ['SITEPKG'] = iOS_paths.sitepkg


# Maybe not too clean to do this here, but convenient :P
iOS_paths.register_paths()
