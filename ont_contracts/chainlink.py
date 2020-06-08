############ Chainlink Library#########

from ont_contracts.lib.CBOR import *
from ont_contracts.lib.ZeroCopySink import *

def initialize(id, callbackAddress, callbackFunction):
    return [id, callbackAddress, callbackFunction, 0, None]


def setBuffer(request, data):
    request[4] = WriteBytes(data, request[4])
    return [request[0], request[1], request[2], request[3], request[4]]


def add(request, key, value):
    request[4] = encodeString(request[4], key)
    request[4] = encodeString(request[4], value)
    return [request[0], request[1], request[2], request[3], request[4]]


def addBytes(request, key, value):
    request[4] = encodeString(request[4], key)
    request[4] = encodeBytes(request[4], value)
    return [request[0], request[1], request[2], request[3], request[4]]


def addInt(request, key, value):
    request[4] = encodeString(request[4], key)
    request[4] = encodeInt(request[4], value)
    return [request[0], request[1], request[2], request[3], request[4]]


def addUInt(request, key, value):
    request[4] = encodeString(request[4], key)
    request[4] = encodeUInt(request[4], value)
    return [request[0], request[1], request[2], request[3], request[4]]


def addStringArray(request, key, values):
    request[4] = encodeString(request[4], key)
    request[4] = startArray(request[4])
    for i in range(len(values)):
        request[4] = encodeString(request[4], values[i])
    request[4] = endSequence(request[4])
    return [request[0], request[1], request[2], request[3], request[4]]
