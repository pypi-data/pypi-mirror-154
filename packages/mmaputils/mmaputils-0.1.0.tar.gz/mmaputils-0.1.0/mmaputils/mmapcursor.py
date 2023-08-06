import mmap
import os
import struct
from types import TracebackType
import typing as t

__all__ = (
    "MmapCursor",
)


class MmapCursor:
    """
    A generic utility class using mmap for fast reading and in-place editing of large files,
    at the expense of memory space. At the moment this class maps the whole file into memory, so using it
    with files that are too big would be unwise.

    Args:
        path: The file path to open.
        byteorder: The byte order of the file, either big or little endian.
    """
    def __init__(self, path: str, byteorder: t.Literal["big", "little"] = "big"):
        self.fdesc = os.open(path, os.O_RDWR)
        self.m = mmap.mmap(self.fdesc, length=0)

        self._position = 0
        self.stack: t.List[int] = []
        self.byteorder = byteorder

    def __enter__(self) -> 'MmapCursor':
        return self

    def __exit__(
        self,
        exc_type: t.Optional[t.Type[BaseException]],
        exc_val: t.Optional[BaseException],
        exc_tb: t.Optional[TracebackType]
    ) -> bool:
        self.close()
        return False

    @property
    def struct_endian_str(self) -> str:
        """
        Get the endianness specifier to be used for the stdlib `struct` module.
        """
        return "<" if self.byteorder == "little" else ">"

    def close(self) -> None:
        """
        Flushes and closes the file, saving any writes to disk. This object cannot be used once closed.
        """
        self.m.flush()
        self.m.close()
        os.close(self.fdesc)

    def push(self) -> None:
        """
        Push the current cursor position on the stack.
        """
        self.stack.append(self._position)

    def pop(self) -> None:
        """
        Pop the last cursor position pushed to the stack.
        """
        self._position = self.stack.pop()

    @property
    def position(self) -> int:
        """
        The position in the file, in bytes. Zero-indexed. To advance the cursor, you can use `+=`.

        Raises:
            `ValueError`: If the set position is negative.
        """
        return self._position

    @position.setter
    def position(self, p: int) -> None:
        if p < 0:
            raise ValueError(f"Position shifted to a negative value ({self._position})")

        self._position = p

    def find(self, b: bytes, find_size: t.Optional[int] = None) -> bool:
        """
        Find a sequence of bytes, and place the cursor immediately after the found sequence.

        Args:
            b: The byte sequence to locate.
            find_size: Optional. If provided, `find` will only search between the current position and `find_size` bytes out.
                Otherwise, the whole file will be searched.

        Returns:
            `True`: If the sequence was found. The cursor will have moved.
            `False`: If the sequence was not found. The cursor will not move in this case.
        """
        if not b:
            raise ValueError("len(b) == 0. Cannot search for nothing.")

        if find_size == 0:
            raise ValueError("find_size may not be 0, use None to specify whole file.")

        if find_size is None:
            loc = self.m.find(b, self._position)
        else:
            loc = self.m.find(b, self._position, self._position + find_size)
        
        if loc == -1:
            return False

        self._position = loc + len(b)
        return True

    def find_byte(self, b: int, find_size: t.Optional[int] = None) -> bool:
        """
        Find a byte, and place the cursor immediately after it.

        Related:
            `MmapCursor.find`
        """
        return self.find_int(b, 1, find_size)

    def find_int(self, i: int, i_size: int, find_size: t.Optional[int] = None) -> bool:
        """
        Find an arbitrary sized integer, and place the cursor immediately after the found integer.
        Size is in bytes.

        Related:
            `MmapCursor.find`
        """
        return self.find(i.to_bytes(i_size, byteorder=self.byteorder), find_size)

    def find_ascii(self, s: str, find_size: t.Optional[int] = None) -> bool:
        """
        Find an ascii string, and place the cursor immediately after the found sequence.

        Related:
            `MmapCursor.find`
        """
        return self.find(bytes(s, 'ascii'), find_size)

    def write(self, b: bytes) -> None:
        """
        Write a byte sequence to the current position. Does not shift the cursor.
        """
        self.m.seek(self._position)
        self.m.write(b)

    def write_byte(self, b: int) -> None:
        """
        Write a byte to the current position. Does not shift the cursor.

        Related:
            `MmapCursor.write`
        """
        if isinstance(b, int) and not 0 < b < 255:
            raise ValueError("Single byte must be between 0 and 255.")

        self.write(bytes([b]))

    def write_int(self, i: int, i_size: int, signed: bool = True) -> None:
        """
        Write an integer to the current position. Does not shift the cursor.

        Related:
            `MmapCursor.write`
        """
        self.write(i.to_bytes(i_size, byteorder=self.byteorder, signed=signed))

    def write_ascii(self, s: str) -> None:
        """
        Writes a string to the current position as ASCII. Does not write a null terminator. Does not shift the cursor.

        Related:
            `MmapCursor.write`
        """
        self.write(bytes(s, 'ascii'))

    def write_double(self, d: float) -> None:
        """
        Writes a float as a double at the current position. Does not shift the cursor.

        Related:
            `MmapCursor.write`
        """
        self.write(bytes(struct.pack(f"{self.struct_endian_str}d", d)))

    def read(self, size: int) -> bytes:
        """
        Reads at most `size` bytes from the stream, starting at the current cursor position. Does not advance the cursor.
        Note that this function may read less than `size` bytes if close to the end of the stream.

        Related:
            `MmapCursor.read`
        """
        self.m.seek(self._position)
        return self.m.read(size)

    def read_byte(self) -> int:
        """
        Reads one byte from the stream and returns it.

        Related:
            `MmapCursor.read`
        """
        return self.read(1)[0]

    def read_int(self, size: int, signed: bool = True) -> int:
        """
        Reads an integer of the specified size (in bytes) and returns it.

        Related:
            `MmapCursor.read`
        """
        b = self.read(size)
        return int.from_bytes(b, byteorder=self.byteorder, signed=signed)

    def read_ascii(self, size: int) -> str:
        """
        Reads at most `size` bytes from the stream and returns them as an ASCII string. Does not advance the cursor.

        Related:
            `MmapCursor.read`
        """
        return str(self.read(size), 'ascii')

    def next(self, size: int) -> bytes:
        """
        Reads at most `size` bytes from the stream and advances the cursor immediately after the read bytes.
        """
        data = self.read(size)
        self.position += size
        return data

    def next_byte(self) -> int:
        """
        Read one byte from the stream, and advance the cursor after it.

        Related:
            `MmapCursor.next`
        """
        b = self.read_byte()
        self.position += 1
        return b

    def next_int(self, size: int, signed: bool = True) -> int:
        """
        Read an integer of the specified size (in bytes) and advance the cursor after it.

        Related:
            `MmapCursor.next`
        """
        i = self.read_int(size, signed)
        self.position += size

        return i

    def next_ascii(self, size: int) -> str:
        """
        Read an ascii string of length `size`, and advance the cursor after it.

        Related:
            `MmapCursor.next`
        """
        s = self.read_ascii(size)

        # need to shift by real str length, in case we hit end
        self.position += len(s)
        return s
