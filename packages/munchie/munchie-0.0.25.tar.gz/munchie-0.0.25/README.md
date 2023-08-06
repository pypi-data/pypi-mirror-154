# Munchie

Munchie is a simple file object manager to describe, manipulate and store directories and files.  

---

## Compatibility
* Munchie works with Linux, OSX, and Windows.  
* Requires Python 3.8 or later.  

---

## Installing
Install with `pip3` or your favorite PyPi package manager.  
```
pip install munchie
```

---

## Using FileMuncher

Import munchie and instantiate a file_muncher object:  
```
from munchie import FileMuncher

file_muncher = FileMuncher()
```

### Default attributes

By default FileMuncher loads the current working directory as well as the user home directory into respective attributes.  
The attributes can be accessed by calling them from the constructed FileMuncher object.  
```
file_muncher.base_dir  # current working directory
file_muncher.home_dir  # user home directory
```

### Create a new directory

Create a new directory at the given path: 
```
# create 'new_directory' in the user home folder
file_muncher.create_new_directory(f'{file_muncher.home_dir}/new_directory')
```

### Create a new file

Create a new file at the given path:  
```
# create 'new_file.test' in the user home folder
file_muncher.create_new_file(f'{file_muncher.home_dir}/new_file.test')
```

### Get directory contents

List the sub-directories and files of a given path:
```
# list the immediate contents of a path
file_muncher.get_directory_contents(file_muncher.home_dir)

# recursively list the contents of a path
file_muncher.get_directory_contents(file_muncher.home_dir, recursive=True)
```
Sub-directories will be listed under a "directories" key and sub-files will be listed under a "files" key

### Get filesystem details

To get filesystem details about a directory or file:
```
# get filesystem details about a path
file_muncher.get_path_stats(f'{file_muncher.home_dir}/new_file.test')
```

<table>
<thead>
  <tr>
    <th>Attribute</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>type</td>
    <td>file or directory</td>
  </tr>
  <tr>
    <td>st_mode</td>
    <td>read | write | execute permissions</td>
  </tr>
  <tr>
    <td>st_uid</td>
    <td>user owner of the path. returns raw uid on Windows</td>
  </tr>
  <tr>
    <td>st_gid</td>
    <td>group owner of the path. returns raw gid on Windows</td>
  </tr>
  <tr>
    <td>st_size</td>
    <td>size in bytes</td>
  </tr>
  <tr>
    <td>st_atime</td>
    <td>time of most recent access in seconds</td>
  </tr>
  <tr>
    <td>st_mtime</td>
    <td>time of most recent content modification in seconds</td>
  </tr>
  <tr>
    <td>st_ctime</td>
    <td>time of most recent metadata change on Unix and creation time on Windows in seconds</td>
  </tr>
</tbody>
</table>

### Read file

FileMuncher is able to read in various file types and return the contents in a format that can be manipulated.  
Supported extensions include:

<table>
<thead>
  <tr>
    <th>Type</th>
    <th>Extensions</th>
    <th>Return Type</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>csv</td>
    <td>.csv</td>
    <td>list of dicts</td>
  </tr>
  <tr>
    <td>config</td>
    <td>.cfg, .conf, .ini</td>
    <td>dict</td>
  </tr>
  <tr>
    <td>json</td>
    <td>.json</td>
    <td>dict</td>
  </tr>
  <tr>
    <td>text</td>
    <td>.nfo, .text, .txt</td>
    <td>list</td>
  </tr>
  <tr>
    <td>yaml</td>
    <td>.yaml, .yml</td>
    <td>dict</td>
  </tr>
</tbody>
</table>

Read in the contents of a supported file type. FileMuncher will determine the file extension and use the appropriate function to return the contents.  
```
# read in 'new_file.json' and return the contents as dict
contents = file_muncher.read_file(f'{file_muncher.home_dir}/new_file.json')
```

### Remove a directory

Delete a directory and all of the contents of the directory from the filesystem. This is not a permanent delete. Contents will be moved to Trash or Recycle Bin respective of the local operating system.
```
# prompt to remove directory 'new_dir'
file_muncher.remove_directory(f'{file_muncher.home_dir}/new_dir')
```
By default this command will require confirmation input from the user to verify prior to deletion. The confirmation requirement can be toggled off by setting the `force` flag.  
```
# remove directory 'new_dir' without confirmation check
file_muncher.remove_directory(f'{file_muncher.home_dir}/new_dir', force=True)
```

### Remove a file

Delete a file. This is not a permanent delete. The file will be moved to Trash or Recycle Bin respective of the local operating system.
```
# prompt to remove file 'new_file.test'
file_muncher.remove_file(f'{file_muncher.home_dir}/new_file.test')
```
By default this command will require confirmation input from the user to verify prior to deletion. The confirmation requirement can be toggled off by setting the force flag.  
```
# remove file 'new_file.test' without confirmation check
file_muncher.remove_file(f'{file_muncher.home_dir}/new_file.test', force=True)
```

### Rotate files

Cleanup old files within a given path. This functionality is great for log rotation.
```
# prompt to rotate files in directory 'old_logs'
file_muncher.rotate_files(f'{file_muncher.home_dir}/old_logs')
```

Specify how many days old files to rotate should be by setting the `days_old` parameter. Default is 14 days old.
```
# prompt to remove files in directory 'old_logs' older than 30 days
file_muncher.rotate_files(f'{file_muncher.home_dir}/old_logs', days_old=30)
```

By default this action will prompt for confirmation and display a list of all paths that will be removed. This can be toggled off with a `force` flag.  
```
# remove files in directory 'old_logs' older than 30 days without confirmation check
file_muncher.rotate_files(f'{file_muncher.home_dir}/old_logs', days_old=30, force=True)
```


### Update Path

New directory and file paths can be added to the FileMuncher object. Existing paths can also be updated.  
Whether creating a new path or updating an existing the only requirements are the `attribute_name` and the `attribute_path`.
A new path created by update_path will be added to a dictionary under the custom_path attribute.
```
# create a new attribute called 'new_file' that points to 'new_file.test' located in the user home directory
file_muncher.update_path(attribute_name='new_file', attribute_path=f'{file_muncher.home_dir}/new_file.test')

# reference a new path created by update_path
file_muncher.custom_path['new_file']

# update an existing path to point somewhere new
file_muncher.update_path(attribute_name='base_dir', attribute_path='/Users/username/Documents/testing')
```
When creating or updating a path you have the option to create a blank directory or empty file at the same time by specifying the `is_dir` or `is_file` flags. Only one flag may be chosen as a path cannot be both a directory and a file.
```
# create a new directory attribute and create the directory on the filesystem
file_muncher.update_path(attribute_name='new_dir', attribute_path=f'{file_muncher.home_dir}/new_dir', is_dir=True)

# create a new file attribute and create the file on the filesystem
file_muncher.update_path(attribute_name='new_file', attribute_path=f'{file_muncher.home_dir}/new_file.test', is_file=True)
```

### Write file

Update or create a new file with contents. Supports the following file types:
* .csv
* .cfg, .conf, .ini
* .json
* .nfo, .text, .txt
* .yaml, .yml

Write contents to a supported file type:  
```
# prepare dict contents
contents = {
    "file": "muncher"
}
# write the contents to a json file
file_muncher.write_file(contents, f'{file_muncher.home_dir}/new_file.json')
```

---
