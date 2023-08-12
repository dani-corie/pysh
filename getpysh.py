#!/usr/bin/env python3
# coding: utf-8

# This script is a convenience installer to be used in the Pythonista3 iOS app

from functools import partial
import os
import requests
import shutil

URL = "https://github.com/dani-jozsef/pysh/archive/refs/heads/main.zip"
DOWNLOADTO = "Documents/pysh-main.zip"
TEMPDIR = "Documents/_tmp_pysh_main"
PACKAGEDIR = "pysh-main/pysh"
ADDITIONAL_FILES = [ "pysh-main/LICENSE" ]
INSTALLDIR = "Documents/site-packages/pysh"

##

def postinst(install_path):
  pass

##

def _httpget_internal(url, dst):
  with requests.get(url, stream=True) as r:
    r.raw.read = partial(r.raw.read, decode_content=True)
    with open(dst, 'wb') as f:
      shutil.copyfileobj(r.raw, f)

def _alreadyexists(path):
  return FileExistsError(f"File or directory already exists: '{path}")

def install(
    url = URL,
    downloadto = DOWNLOADTO,
    tempdir = TEMPDIR,
    packagedir = PACKAGEDIR,
    additional_files = ADDITIONAL_FILES,
    installdir = INSTALLDIR):
  
  homedir = os.environ['HOME']
  download_path = os.path.join(homedir, downloadto)
  expand_path = os.path.join(homedir, tempdir)
  package_path = os.path.join(expand_path, packagedir)
  install_path = os.path.join(homedir, installdir)

  if os.path.exists(download_path):
    raise _alreadyexists(download_path)

  if os.path.exists(expand_path):
    raise _alreadyexists(expand_path)

  if os.path.exists(install_path):
    raise _alreadyexists(download_path)

  print(f"Attempting to download '{url}' to '{download_path}'")
  _httpget_internal(url, download_path)
  print(" done..")
  
  print(f"Attempting to unpack to '{expand_path}'")
  shutil.unpack_archive(download_path, expand_path)
  print(" done..")

  print(f"Attempting to install to '{install_path}'")
  shutil.move(package_path, install_path)
  for file in additional_files:
    file_path = os.path.join(expand_path, file)
    shutil.move(file_path, install_path)
  print(" done!")

  print(f"Attempting to remove '{download_path}' and '{expand_path}'")
  os.remove(download_path)
  shutil.rmtree(expand_path)
  print(" done..")

  print("Running post-install script..")
  postinst(install_path)

  print("Bye! <3")


if __name__ == "__main__":
  install()
