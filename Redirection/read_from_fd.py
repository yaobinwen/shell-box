#!/usr/bin/env python3

import argparse


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
            "Print hello messages to the names read from a file descriptor. "
            "This program is only used to demonstrate the use of input "
            "redirection on non-stdin file descriptors. It does not mean to "
            "implement anything of practical use."
        )
    )

    parser.add_argument(
        "fd",
        type=non_std_fd,
        help="File descriptor number (non-standard) for input",
    )

    return parser


def main(fd):
    print("Enter names (one per line). Press Ctrl+D (EOF) to finish.")
    with open(fd, "r") as fh:
        for line in fh:
            print(f"Hello, {line.strip()}")


if __name__ == "__main__":
    main(**vars(_syntax().parse_args()))
