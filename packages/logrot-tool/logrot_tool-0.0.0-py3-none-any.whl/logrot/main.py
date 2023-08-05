#!/usr/bin/env python3


"""
LogRot main executable module.

CRON example:
0  *  *  *  *  python3 ~/.local/share/cron/logrot ~/.cache/cron/*.log
""" """
This file is part of python-logrot.

python-logrot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

python-logrot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with python-logrot.  If not, see <https://www.gnu.org/licenses/>.

Copyright (c) 2019-2022, Maciej Barć <xgqt@riseup.net>
Licensed under the GNU GPL v3 License
"""


import argparse
import gzip
import os

from . import __version__


def next_arch_name(an_dir, an_name, an_num):
    """Return next available archive name of a file."""

    comb_name = os.path.join(an_dir, f"{an_name}-{an_num}.gz")

    if os.path.exists(comb_name):
        return next_arch_name(an_dir, an_name, an_num + 1)

    return comb_name


def main():
    """Main."""

    parser = argparse.ArgumentParser(
        description="%(prog)s - log rotate script (to be run using cron)",
        epilog="""Copyright (c) 2019-2022, Maciej Barć <xgqt@riseup.net>
        Licensed under the GNU GPL v3 License"""
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"logrot {__version__}"
    )
    parser.add_argument(
        "-o", "--out",
        type=str,
        help="the directory to rotate to"
    )
    parser.add_argument(
        "-s", "--size",
        type=float,
        default=1,
        help="minimal size to rotate (in MB)"
    )
    parser.add_argument(
        "-k", "--keep",
        action="store_true",
        help="don't remove the files"
    )
    parser.add_argument(
        "files",
        type=str,
        nargs="+"
    )
    args = parser.parse_args()

    for i in args.files:
        if not os.path.isfile(i):
            continue

        size_mb = os.path.getsize(i) / 1048576
        if not size_mb >= args.size:
            continue

        if args.out:
            arch_dir = args.out
        else:
            arch_dir = os.path.dirname(i)

        arch_name = next_arch_name(arch_dir, os.path.basename(i), 0)

        with open(i, "rb") as file_open:
            file_byte = bytearray(file_open.read())
            arch_path = os.path.join(arch_dir, arch_name)

            with gzip.open(arch_path, "wb") as file_arch:

                file_arch.write(file_byte)

                if not args.keep:
                    try:
                        os.remove(i)
                    except PermissionError:
                        pass


if __name__ == "__main__":
    main()
