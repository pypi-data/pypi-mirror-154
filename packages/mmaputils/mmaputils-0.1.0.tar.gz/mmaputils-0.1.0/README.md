# mmaputils
Various utilities I use in other projects, wrapping the python stdlib mmap module. 
Currently contains only one utility.

## MmapCursor
A utility class wrapping an `mmap.mmap` object. Intended to simplify reading and in-place
editing of file headers.

Example:
```py
# Say we want to find a specific header field in a file.
# This header starts with a HEADER_MAGIC field to identify itself, and the desired
# field is a 32 bit unsigned integer 16 bytes after that header.
from mmaputils import MmapCursor
import sys

filename = "whatever.file"
magic = 0x12345678

# Note: byteorder is important, but defaults to big endian.
# Let's say that's fine for this file.
with MmapCursor(filename) as cursor:
    # Search for magic number. If found, found=True.
    found = cursor.find_int(magic, 4)
    if not found:
        # handle not found
        print(f"{filename}: could not find header")
        sys.exit(1)
    
    # If found, cursor is placed after field. Advance 16 bytes
    cursor.position += 16
    
    # Read our 32-bit (4 bytes) field.
    field = cursor.read_int(4, signed=False)
    
    print(f"found field: {field}")
    
    # The above read does *not* advance the cursor. This is so we can write something
    # if we want. This will write a new 32 bit unsigned value to the header field
    # we just read:
    cursor.write_int(21, 4, signed=False)
    
    # Note that if we wanted to automatically advance the cursor after reading a field, we
    # could use "next_int" instead.
    
    # Once block is over, file will close and all writes are flushed.
```

