#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys


def non_std_fd(fd: int):
    """
    Check if the file descriptor is a non-standard one.
    Standard file descriptors are 0 (stdin), 1 (stdout), and 2 (stderr).
    """
    fd = int(fd)

    if fd < 0:
        raise ValueError(f"File descriptor {fd} is negative.")

    if fd in (0, 1, 2):
        raise ValueError(f"File descriptor {fd} is standard (stdin, stdout, stderr).")

    return fd


def _syntax():
    parser = argparse.ArgumentParser(
        description=(
            "Compare two files line by line. Return 0 if they are the same; "
            "return 1 if they differ; return 2 if an error occurs. "
            "This program is only used to demonstrate the use of input "
            "redirection on non-stdin file descriptors. It does not mean to "
            "implement a full file comparison tool."
        )
    )

    parser.add_argument(
        "fd1",
        type=non_std_fd,
        help="File descriptor number (non-standard) for the first file to compare.",
    )

    parser.add_argument(
        "fd2",
        type=non_std_fd,
        help="File descriptor number (non-standard) for the second file to compare.",
    )

    return parser


def compare_files(fd1, fd2):
    """
    Compares two files based on their file descriptors.

    1. Checks if the file sizes are the same. If not, returns False.
    2. If sizes are the same, compares the files line by line.
    3. Returns True if the files are identical, False otherwise.
    """
    file_info1 = os.fstat(fd1)
    file_info2 = os.fstat(fd2)

    if file_info1.st_size != file_info2.st_size:
        return False

    with open(fd1, "r") as f1, open(fd2, "r") as f2:
        while True:
            line1 = f1.readline()
            line2 = f2.readline()

            if not line1 and not line2:
                return True  # Both files have reached the end

            if line1 != line2:
                return False


def main(fd1: int, fd2: int):
    try:
        return sys.exit(0) if compare_files(fd1, fd2) else sys.exit(1)
    except Exception as e:
        print(f"Error comparing files: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main(**vars(_syntax().parse_args()))
