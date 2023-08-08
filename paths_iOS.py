import os


class paths_iOS:

  local = os.path.join(os.environ['HOME'], 'Documents')

  icloud = '/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents'

  def register_paths():
    os.environ['LOCAL'] = paths_iOS.local
    os.environ['ICLOUD'] = paths_iOS.icloud


# Maybe not too clean but nice
paths_iOS.register_paths()
