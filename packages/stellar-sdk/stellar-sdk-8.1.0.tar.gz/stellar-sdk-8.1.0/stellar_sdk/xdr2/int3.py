# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import UnsignedInteger

__all__ = ["Int3"]


class Int3:
    """
    XDR Source Code::

        typedef unsigned int    int3;
    """

    def __init__(self, int3: int) -> None:
        self.int3 = int3

    def pack(self, packer: Packer) -> None:
        UnsignedInteger(self.int3).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Int3":
        int3 = UnsignedInteger.unpack(unpacker)
        return cls(int3)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Int3":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Int3":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.int3 == other.int3

    def __str__(self):
        return f"<Int3 [int3={self.int3}]>"
