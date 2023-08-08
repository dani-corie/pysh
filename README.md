# PySh

PySh (pronounced *'psssh'*) is a library of (vaguely) Unix shell-like calls for file manipulation from the Python REPL.

It was developed first as meditative practice, and second because I wanted something like this to use in the Pythonista3 iOS app. The design philosophy is safety first, at the detriment of convenience, to avoid becoming a gigantic footcannon. The calls perform no overwrites or directory merges.

## Error management

To keep it sweet and simple, batch operations will raise an exception after the first error encountered. The progress of files and directories processed are kept in the `last_processed` module-scoped variable, which is reset with each new call other than `ls`.

## Path expansion

Paths provided are expanded for environment variables (eg. `${HOME}`) via `os.path.expandvars` and wildcards via `glob.glob`. The `paths_iOS.py` module adds two additional environment variables useful in iOS Pythonista3 (`${LOCAL}` is the local documents folder, while `${ICLOUD}` is the iCloud Pythonista folder.)

Where a single file is expected, and a path expands to multiple files, a `ValueError` is raised.

**Note: The tilde symbol `~` in paths is not expanded by any of the calls for the primary reason that iOS seems to routinely use it as a regular character in iCloud paths.. Use `${HOME}` instead for the same effect.**

## The commands

### cd

Changes the working directory, and returns the new working directory path.

### cp

Copies the source item(s).

* If the destination is an existing directory, source items are copied into it.
* If the destination does not point to an existing directory, a copy of the source is made with the new name and location. In this case, the source path must expand to a single file or directory.

Set `recursive=True` to allow directories to be processed. By default, an error is raised on encountering a directory.

### find

Lists all files matching a wildcard path.

Setting `recursive=True` passes the same to `glob.glob`, allowing the wildcard `**` to mean subdirectories in any depth, and finding files by a name pattern anywhere within a directory tree.

### ls

Lists the current working directory or a single directory specified by a path that is 
Returns a tuple of `(directory path, [ ..directory content ])`

### mkdir

It's a shortcut to `os.mkdir` with path expansion.

### mv

Moves or renames the source item(s).

* If the destination is an existing directory, source items are mpved into it.
* If the destination does not point to an existing directory, the source is renamed to this new name and location. In this case, the source path must expand to a single file or directory.

### rm

Deletes items specified by a wildcard path.

Set `recursive=True` to allow directories to be processed. By default, an error is raised on encountering a directory.

### rmdir

It's a shortcut to `os.rmdir` with path expansion.
