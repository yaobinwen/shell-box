#!/bin/sh

# Without `4<&0` the program will error out with "Bad file descriptor."
./read_from_fd.py 4 4<&0
