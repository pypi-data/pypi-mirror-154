# zsfile

zstandard compress and decompress tool.

## Install

```
pip3 install zsfile
```

## Command Usage

```
test@test Downloads % zsf --help
Usage: zsf [OPTIONS] INPUT

  Zstandard compress and decompress tool.

Options:
  -d, --decompress   force decompression. default to false.
  -o, --output TEXT  Output filename.
  --help             Show this message and exit.
```

## Examples

```
test@test test01 % ls    
mingw-w64-x86_64-file-5.39-2-any.pkg.tar.zst
test@test test01 % zsf -d mingw-w64-x86_64-file-5.39-2-any.pkg.tar.zst
decompressing file mingw-w64-x86_64-file-5.39-2-any.pkg.tar.zst to mingw-w64-x86_64-file-5.39-2-any.pkg.tar...
test@test test01 % ls
mingw-w64-x86_64-file-5.39-2-any.pkg.tar	mingw-w64-x86_64-file-5.39-2-any.pkg.tar.zst
test@test test01 % file mingw-w64-x86_64-file-5.39-2-any.pkg.tar.zst 
mingw-w64-x86_64-file-5.39-2-any.pkg.tar.zst: Zstandard compressed data (v0.8+), Dictionary ID: None
test@test test01 % file mingw-w64-x86_64-file-5.39-2-any.pkg.tar
mingw-w64-x86_64-file-5.39-2-any.pkg.tar: POSIX tar archive
test@test test01 %
```

## Releases

### v0.1.0

- First release.
