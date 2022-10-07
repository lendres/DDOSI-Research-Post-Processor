"""
Created on October 4, 2022
@author: Lance A. Endres
"""
import                                           cffi
import                                           pathlib
import                                           re


# NOTE: The directory location may need to change depending on how this library was install relative to the signal segment library.
# Get the current directory where this file is and then go up two levels (equivilent to CD.., CD..).
directory        = pathlib.Path().absolute().parent.parent.parent
# Location of header file in relation to the previous path.
directory        = directory / "Segment Signals" / "src" / "CPP Static Library"
libraryDirectory = directory / "bin" / "Release"


# Should not need to change these, but allow for the possibility.
headerFileName   = "SegmentSignalFunctions.h"
libraryName      = "SegmentSignal"


# Allow the user the opportunity to spot any errors.
headerFilePath   = directory / "SegmentSignalFunctions.h"
print("\n\nReading the signal segment header file from:")
print(headerFilePath)

ffi = cffi.FFI()
with open(headerFilePath) as file:
    # cffi does not like our preprocessor directives, so we remove them
    lines = file.read().splitlines()
    print("\n\nLines:\n", lines)
    flt = filter(lambda line : not re.match(r" *#", line), lines)
    flt = map(lambda line : line.replace("EXPORT_SYMBOL ", ""), flt)

    result = list(flt)
    print("\n\nMapping done:\n", result)
    joinedResult = str("\n").join(result)
    print("\n\nJoined\n", joinedResult)
    ffi.cdef(joinedResult)




    ffi.cdef(file.read())

ffi.set_source(
    # Base name for the source file that will be created on your file system. CFFI will generate a .c file, compile it to a
    # .o file, and link it to a .<system-description>.so or .<system-description>.dll file.
    "SegmentSignal",
    # Since you're calling a fully-built library directly, no custom source is necessary. You need to include the .h files, though,
    # because behind the scenes cffi generates a .c file that contains a Python-friendly wrapper around each of the functions.
    '#include "' + headerFileName + '"',
    # The important thing is to include the pre-built lib in the list of libraries you're linking against.
    libraries=[libraryName],
    library_dirs=[libraryDirectory.as_posix()],
    extra_link_args=["-Wl,-rpath,."],
)