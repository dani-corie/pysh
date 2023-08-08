#!/usr/bin/env python3
# coding: utf-8

import os


class paths_iOS:

  local = os.path.join(os.environ['HOME'], 'Documents')

  icloud = '/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents'

  def register_paths():
    os.environ['LOCAL'] = paths_iOS.local
    os.environ['ICLOUD'] = paths_iOS.icloud


# Maybe not too clean to do this here, but convenient :P
paths_iOS.register_paths()
