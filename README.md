# pylicenseheader
Script to prepend a license header to all files in a repository. 

## Usage
Tested with Python 3.7.0

```bash
usage: license.py [-h] [--header HEADER] [--dir DIR]
                  [--header-prefix HEADER_PREFIX] [--ext EXT]

Add license to source code files

optional arguments:
  -h, --help            show this help message and exit
  --header HEADER       Path to license header file
  --dir DIR             Directory to traverse for files
  --header-prefix HEADER_PREFIX
                        Prefix to each line to comment out the license header
  --ext EXT             The file extension on which to filter files                                  
```