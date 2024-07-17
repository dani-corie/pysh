#!/usr/bin/env python3
# coding: utf-8

# This module provides some path constants and environment variables useful
# in the Pythonista3 iOS app

import os

LOCAL = os.path.join(os.environ['HOME'], 'Documents')
ICLOUD = '/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents'
SITEPKG = os.path.join(os.environ['HOME'], 'Documents/site-packages')

os.environ['LOCAL'] = LOCAL
os.environ['ICLOUD'] = ICLOUD
os.environ['SITEPKG'] = SITEPKG
