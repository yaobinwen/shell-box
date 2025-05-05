# Redirection

## 0. Reference

POSIX standard location ([direct link](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html#tag_19_07)):
- POSIX main page
  - Volume: Shell & Utilities
    - 2. Shell Command Language
      - 2.7 Redirection

## 1. Overview

The overall format used for redirection can be defined by the following [ABNF](https://datatracker.ietf.org/doc/html/rfc5234):

```
Redirection    = [FileDescriptor] RedirectionOp Word

FileDescriptor = 1*DIGIT

RedirectionOp  = ">" / ">|" / ">>" / ">&" / "<" / "<<" / "<<-" / "<&" / "<>"

Word           = FileDescriptor / FILE / "-"

FILE           = <File name or file path>

DIGIT          =  %x30-39 ; 0-9
```

In a simpler form:

```
[n]redir-op word
```

When `FileDescriptor` is not specified:
- `0` (stdin) is assumed for input redirecting.
- `1` (stdout) is assumed for output redirecting.

## 2. The redirection operators

Here is a quick overview:

| Operator | Description |
|:--------:|:------------|
| `>`      | Redirect output to the specified file to overwrite it. Fail if `set -C` is enabled. |
| `>\|`    | Same as `>` but overrides `set -C`. |
| `>>`     | Redirect output to the specified file but append to it. |
| `M>&N`   | Make the file descriptor `M` the same as (i.e., an alias of) `N` for output. |
| `<`      | Redirect input from the keyboard to the specified file. |
| `<<`     | Here-document. |
| `<<-`    | Here-document. |
| `M<&N`   | Make the file descriptor `M` the same as (i.e., an alias of) `N` for input. |
| `<>`     | Open file for both reading and writing. |

Without any redirection, the input and output typically look as follows:

![Standard configuration](https://github.com/yaobinwen/shell-box/blob/main/Redirection/00-standard.png?raw=true)

### 2.1 `>`, `>|`, `>>`: Redirect output to the specified file

The three general formats for redirecting output are:

```
[n]>file
[n]>|file
[n]>>file
```

If `n` is not specified, it's `1` (stdout) by default.

For example, `command 1>stdout.txt 2>stderr.txt` (or `command >stdout.txt 2>stderr.txt`) can be illustrated as follows:

![command 1>stdout.txt 2>stderr.txt](https://github.com/yaobinwen/shell-box/blob/main/Redirection/01.png?raw=true)

`>>` appends the output to the specified file (and firstly creates it if the file doesn't exist).

There doesn't seem to be a `>>|` redirection operator.

### 2.2 `>&`: Duplicate an output file descriptor

The general form is:

```
[M]>&N
```

where `M` and `N` are file descriptors. This essentially means making `M` the same as `N` for output. As a result, writing data to the file descriptor `M` will also affect the file position pointer at the file descriptor `N`.

For example, if we want to redirect the command's output to `stderr` to `stdout`, we can run `command >stdout.txt 2>&1`. There are two ways to interpret this:
- What is output to the file descriptor `2` is now output to the file descriptor `1`.
- The file descriptor `2` becomes an alias of `1` so now `2` and `1` point to the same file.

This can be illustrated as follows:

![command >stdout.txt 2>&1](https://github.com/yaobinwen/shell-box/blob/main/Redirection/02.png?raw=true)

### 2.3 `<`: Redirect input from the specified file

The general form is:

```
[n]<word
```

where `n` is the file descriptor. If not specified, `0`(stdin) is assumed.

It means the file that's specified by `word` will be opened for reading on the designated file descriptor `n`. In other words:
- When `n=0` (stdin), that means the stdin does not get the input from the standard input device keyboard but from the file `word`.
- When `n≠0`, that means the file that's represented by the file descriptor `n` gets the input (i.e., reads) from the file `word`.

For example, `command 0<input.txt` (or `command <input.txt`) can be illustrated as follows:

![command 0<input.txt](https://github.com/yaobinwen/shell-box/blob/main/Redirection/03.png?raw=true)

In case if the command wants to read input from other file descriptors such as `3` or `4`, we can redirect the input like this: `command 3<input.txt`. See [`compare-files.sh`](./compare-files.sh) as an example.

### 2.4 `<&`: Duplicating an input file descriptor

The general form is:

```
[M]<&N
```

where `M` and `N` are file descriptors. This essentially means making `M` the same as `N` for input. As a result, reading data from the file descriptor `M` will also affect the file position pointer at the file descriptor `N`.

For example, if a program reads input using the file descriptor `4`, but in one particular execution, we want the program to read from `stdin`, then we can make `4` the same as `0` (stdin) so the program will actually read from `stdin`. See [`dup_input_fd.sh`](./dup-input-fd.sh) as an example.

### 2.5 Here-Document

The redirection operators "<<" and "<<-" both allow redirection of subsequent lines read by the shell to the input of a command. The redirected lines are known as a "here-document".

### 2.6 `<>`: Open file descriptors for reading and writing

The redirection operator:

```
[n]<>file
```

shall cause the file to be opened for both reading and writing on the file descriptor `n`, or standard input if `n` is not specified. If the file does not exist, it shall be created.
