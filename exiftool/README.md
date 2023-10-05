# exiftool

## Description

This package provides a fairly clumsy Python interface to Phil Harvey's
most excellent exiftool command. At the moment, it supports only the
ability to read EXIF tags from a given file. When I need to do more with
EXIF (maybe adding or updating location data), I'll add that capability
then.

Go to [https://exiftool.org](https://exiftool.org) to download the
exiftool command.

NOTE: Consider using [PyExifTool](http://smarnach.github.io/pyexiftool)
instead of this package.

## Usage

The readfile() function returns a complex structure that requires some
exploration. You can run this module directly against one or more files as in
the following example:

```
python exiftool.py IMG_9071.CR2
```

Think of ComplexNamespace as a dictionary that you address with
object.attribute syntax rather than with dictionary[key] syntax. So rather than
a compound dictionary that makes you write code like

```
exif_data['Composite']['ImageSize']
```

you can write

```
exif_data.Composite.ImageSize
```

instead. Isn't that nicer!?
