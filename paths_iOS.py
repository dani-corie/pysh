import os

class paths_iOS:
  local = os.path.join(os.environ['HOME'], 'Documents')
  icloud = '/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents'

os.environ['LOCAL'] = paths_iOS.local
os.environ['ICLOUD'] = paths_iOS.icloud
