OntCversion = '2.0.0'

from ontology.interop.Ontology.Runtime import Base58ToAddress
from ontology.interop.System.App import RegisterAppCall, DynamicAppCall
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash, GetCallingScriptHash
from ontology.interop.System.Runtime import CheckWitness
from ontology.interop.System.Storage import GetContext, Put, Get
from ontology.libont import bytearray_reverse

from chainlink_ontology.ont_contracts.chainlink import *

CURRENT_PRICE = 'CurrentPrice'

OWNER = Base58ToAddress('AGcWFujmhcya3Zi31qdYsckyAUWpoRktUa')

ChainlinkClientCall = RegisterAppCall('b2bbdcb8e17ad9604ba46257ae0e798910c57f65', 'operation', 'args')

ContractAddress = GetExecutingScriptHash()


def Main(operation, args):
    if operation == 'requestEthereumPrice':
        assert (len(args) == 3)
        oracle = args[0]
        jobId = args[1]
        payment = args[2]
        return requestEthereumPrice(oracle, jobId, payment)

    if operation == 'fulfill':
        assert (len(args) == 2)
        requestId = args[0]
        price = args[1]
        return fulfill(requestId, price)

    if operation == 'getCurrentPrice':
        return getCurrentPrice()

    if operation == 'cancelRequest':
        assert (len(args) == 4)
        requestId = args[0]
        payment = args[1]
        callBackFunc = args[2]
        expiration = args[3]
        return cancelRequest(requestId, payment, callBackFunc, expiration)

    return False


def requestEthereumPrice(oracle, jobId, payment):
    assert (CheckWitness(OWNER))
    req = ChainlinkClientCall('buildChainlinkRequest', [jobId, ContractAddress, 'fulfill'])
    req = add(req, "get", "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD")
    req = add(req, "path", "USD")
    req = addInt(req, "times", 100)
    assert (ChainlinkClientCall('sendChainlinkRequestTo', [OWNER, oracle, req, payment]))
    return True


def fulfill(requestId, price):
    assert (ChainlinkClientCall('recordChainlinkFulfillment', [bytearray_reverse(GetCallingScriptHash()), requestId]))
    # Notify(['test'])
    Put(GetContext(), CURRENT_PRICE, price)
    return True


def getCurrentPrice():
    return Get(GetContext(), CURRENT_PRICE)


def cancelRequest(requestId, payment, callBackFunc, expiration):
    assert (CheckWitness(OWNER))
    assert (ChainlinkClientCall('cancelChainlinkRequest', [OWNER, requestId, payment, callBackFunc, expiration]))
    return True


def concatKey(str1, str2):
    return concat(concat(str1, '_'), str2)


def DynamicCallFunction(callAddress, callbackFunctionId, params):
    res = DynamicAppCall(callAddress, callbackFunctionId, params)
    if res and res == b'\x01':
        return True
    else:
        return False


def DynamicCallFunctionResult(callAddress, callbackFunctionId, params):
    return DynamicAppCall(callAddress, callbackFunctionId, params)


def _transferLinkFromContact(link, toAcct, amount):
    params = [ContractAddress, toAcct, amount]
    res = DynamicAppCall(link, 'transfer', params)
    if res and res == b'\x01':
        return True
    else:
        return False