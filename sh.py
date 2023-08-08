#!/usr/bin/env python3
# coding: utf-8

from functools import partial
from glob import glob
import os
import requests
import shutil


last_processed = []


class _errorhelper:
  
  def alreadyexists(path):
    return FileExistsError(f"File or directory already exists: '{path}")

  def ambiguous(path):
    return ValueError(f"Path does not expand unambiguously: '{path}'")
  
  def isadir(path):
    return IsADirectoryError(f"Is a directory (set 'recursive=True' to process): '{path}'")
  
  def nosuchfile(path):
    return FileNotFoundError(f"No such file or directory: '{path}'")

  def notadir(path):
    return NotADirectoryError(f"Is not a directory: '{path}")
  

def _expand(path):
  path = os.path.expandvars(path)
  path = os.path.abspath(path)
  return path

def find(path, recursive=False):
  path = _expand(path)
  result = glob(path, recursive=recursive)
  if len(result) == 0:
    raise _errorhelper.nosuchfile(path)
  return result

def _find_single(path):
  expanded_paths = find(path)
  if len(expanded_paths) > 1:
    raise _errorhelper.ambiguous(path)
  return expanded_paths[0]

def _expand_destination(dst):
  try:
    dst_expanded = _find_single(dst)
    return dst_expanded, True
  # I know this is an antipattern but can't be bothered to care here
  except FileNotFoundError:
    dst_loc, dst_name = os.path.split(dst)
    dst_loc = _find_single(dst_loc)
    if not os.path.isdir(dst_loc):
      raise _errorhelper.notadir(dst_loc)
    dst_expanded = os.path.join(dst_loc, dst_name)
    return dst_expanded, False

def _resolvedir(path):
  path = _find_single(path)
  if not os.path.isdir(path):
    raise _errorhelper.notadir(path)
  return path

def ls(path=None):
  if path is not None:
    path = _resolvedir(path)
  else:
    path = os.getcwd()
  return path, os.listdir(path)

def cd(path=None):
  if path is None:
    return os.getcwd()
  path = _resolvedir(path)
  os.chdir(path)
  return path

def _cpmv_internal(src, dst, recursive, fn):
  global last_processed
  last_processed = []
  dst, dst_exists = _expand_destination(dst)
  if dst_exists:
    if not os.path.isdir(dst):
      # Existing non-directory destination provided
      raise _errorhelper.notadir(dst)
    # Existing directory destination provided
    # All source files and directories are copied inside the destination
    src_files = find(src)
    for src_file in src_files:
      src_name = os.path.basename(src_file)
      dst_file = os.path.join(dst, src_name)
      fn(src_file, dst_file, recursive)
  else:
    # New name provided
    # Single source file or directory will be copied or moved
    src_file = _find_single(src)
    fn(src_file, dst, recursive)
  return last_processed

def _cp_file(src, dst):
  if os.path.exists(dst):
    raise _errorhelper.alreadyexists(dst)
  return shutil.copy2(src, dst, follow_symlinks=False)

def _cp_dir(src, dst):
  # if os.path.exists(dst):
  #   raise FileExistsError(f"Destination already exists: '{dst}")
  return shutil.copytree(src, dst, symlinks=True)

def _cp_single(src, dst, recursive):
  global last_processed
  if os.path.isdir(src):
    if recursive:
      last_processed.append(_cp_dir(src, dst))
    else:
      raise _errorhelper.isadir(src)
  else:
    last_processed.append(_cp_file(src, dst))

def cp(src, dst, recursive=False):
  return _cpmv_internal(src, dst, recursive, _cp_single)

def _mv_single(src, dst, _):
  global last_processed
  if os.path.exists(dst):
    raise _errorhelper.alreadyexists(dst)
  last_processed.append(shutil.move(src, dst))

def mv(src, dst):
  return _cpmv_internal(src, dst, None, _mv_single)

def _ln_single(target, link, _):
  global last_processed
  if os.path.exists(link):
    raise _errorhelper.alreadyexists(link)
  os.symlink(target, link)
  last_processed.append(link)

def ln(target, link):
  return _cpmv_internal(target, link, None, _ln_single)

def unzip(zipfile, dst):
  global last_processed
  last_processed = []
  zipfile = _find_single(zipfile)
  dst, exists = _expand_destination(dst)
  if exists:
    raise _errorhelper.alreadyexists(dst)
  shutil.unpack_archive(zipfile, dst)
  last_processed.append(dst)
  return last_processed  

def _rm_single(path, recursive):
  global last_processed
  if os.path.isdir(path):
    if recursive:
      shutil.rmtree(path)
    else:
      raise _errorhelper.isadir(path)
  else:
    os.remove(path)
  last_processed.append(path)

def rm(path, recursive=False):
  global last_processed
  last_processed = []
  files = find(path)
  for file in files:
    _rm_single(file, recursive)
  return last_processed

def mkdir(path):
  global last_processed
  last_processed = []
  dst, exists = _expand_destination(path)
  if exists:
    raise _errorhelper.alreadyexists(dst)
  os.mkdir(dst)
  last_processed.append(dst)
  return last_processed

def rmdir(path):
  global last_processed
  last_processed = []
  path = _find_single(path)
  os.rmdir(path)
  last_processed.append(path)
  return last_processed

def _get_internal(url, dst):
  with requests.get(url, stream=True) as r:
    r.raw.read = partial(r.raw.read, decode_content=True)
    with open(dst, 'wb') as f:
      shutil.copyfileobj(r.raw, f)

def get(url, dst):
  global last_processed
  last_processed = []
  dst, exists = _expand_destination(dst)
  if exists:
    if not os.path.isdir(dst):
      raise _errorhelper.alreadyexists(dst)
    local_filename = url.split('/')[-1]
    dst = os.path.join(dst, local_filename)
  _get_internal(url, dst)
  last_processed.append(dst)
  return last_processed
