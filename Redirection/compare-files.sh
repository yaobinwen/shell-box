#!/bin/sh

TMP_DIR=$(mktemp -d "compare-files.XXXXXX")
_cleanup() {
  rm -fr "$TMP_DIR" || echo "WARNING: cleanup() failed" >&2
}
trap _cleanup EXIT

_make_file_a() {
  cat <<__EOF__ > "$TMP_DIR/file_a.txt"
  Line 1
  Line 2 in file A
__EOF__
}

_make_file_b() {
  cat <<__EOF__ > "$TMP_DIR/file_b.txt"
  Line 1
  Line 2 in file B
__EOF__
}

_make_file_a
_make_file_b

(
  exec 3< "$TMP_DIR/file_a.txt"
  exec 4< "$TMP_DIR/file_b.txt"
  ./compare_files.py 3 4
  rc=$?
  echo "Return code: $rc"
)
