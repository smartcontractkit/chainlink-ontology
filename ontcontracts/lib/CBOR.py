############## COBR Library############
from ontcontracts.lib.ZeroCopySink import *

MAJOR_TYPE_INT = 0
MAJOR_TYPE_NEGATIVE_INT = 1
MAJOR_TYPE_BYTES = 2
MAJOR_TYPE_STRING = 3
MAJOR_TYPE_ARRAY = 4
MAJOR_TYPE_MAP = 5
MAJOR_TYPE_CONTENT_FREE = 7

def encodeType(buf, major, value):
    if value <= 23:
        buf = WriteUint8((major << 5) | value, buf)
    elif value <= 0xFF:
        buf = WriteUint8((major << 5) | 24, buf)
        buf = WriteUint8(value, buf)
    elif value <= 0xFFFF:
        buf = WriteUint8((major << 5) | 25, buf)
        buf = WriteUint16(value, buf)
    elif value <= 0xFFFFFFFF:
        buf = WriteUint8((major << 5) | 26, buf)
        buf = WriteUint32(value, buf)
    elif value <= 0xFFFFFFFFFFFFFFFF:
        buf = WriteUint8((major << 5) | 27, buf)
        buf = WriteUint64(value, buf)
    return buf


def encodeIndefiniteLengthType(buf, major):
    return WriteUint8((major << 5 | 31), buf)


def encodeUInt(buf, value):
    return encodeType(buf, 0, value)


def encodeInt(buf, value):
    if value >= 0:
        return encodeType(buf, 0, value)
    else:
        return encodeType(buf, 1, -1 - value)


def encodeBytes(buf, value):
    buf = encodeType(buf, 2, len(value))
    return WriteBytes(value, buf)


def encodeString(buf, value):
    buf = encodeType(buf, 3, len(value))
    return WriteString(value, buf)


def startArray(buf):
    return encodeIndefiniteLengthType(buf, 4)


def startMap(buf):
    return encodeIndefiniteLengthType(buf, 5)


def endSequence(buf):
    return encodeIndefiniteLengthType(buf, 7)
