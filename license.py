#! /usr/bin/env python3
import argparse
import os


def remove_header(prefix, lines):
    """
    Remove license header from content. Assumes that all lines (at the start of a files) that start with '//' are part of the license header
    :param lines: content as array of strings (representing lines of the file)
    :return: lines without header
    """
    is_header = True
    reslines = []
    for line in lines:
        if is_header:
            if not (line.startswith(prefix) or line.strip() == ""):
                is_header = False
                reslines += [line]
                continue
        else:
            reslines += [line]
    return reslines


def traversedir(d, prefix, ext, license):
    """
    Traverses a directory recursively and adds the current license header to all Golang files
    :param d: the directory to traverse
    :param license: the content of the new license to write
    """
    for dir, subdirlist, filelist in os.walk(d):
        for file in filelist:
            path = os.path.join(dir, file)
            root, curext = os.path.splitext(path)
            if curext == ext:
                with open(path, "r") as f:
                    lines = f.readlines()
                lines_noheader = remove_header(prefix, lines)
                with open(path, "w") as f:
                    for line in license:
                        f.write(prefix + " " + line)
                    f.write("\n")
                    for line in lines_noheader:
                        f.write(line)

        for subdir in subdirlist:
            newdir = os.path.join(dir, subdir)
            traversedir(newdir, prefix, ext, license)


def main():
    parser = argparse.ArgumentParser(description="Add license to source code files")
    parser.add_argument('--header', type=str, default="./scripts/license/header.txt",
                        help="Path to license header file")
    parser.add_argument('--dir', type=str, default=".", help="Directory to traverse for files")
    parser.add_argument('--header_prefix', type=str, default="//",
                        help="Prefix to each line to comment out the license header")
    parser.add_argument('--ext', type=str, default=".go", help="The file extension on which to filter files")
    args = parser.parse_args()

    with open(args.header) as f:
        license = f.readlines()
        traversedir(args.dir, args.header_prefix, args.ext, license)


if __name__ == "__main__":
    main()
