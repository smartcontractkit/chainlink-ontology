# chainlink-ontology
This repo is consist of some ontology smartcontracts, used for chainlink oracle to support ontology.

## How to build and deploy
1. First you should move ont_contract to your root of ontology-python-compiler path.
2. Then compile your contract by using the ontology python compiler. You should compile oracle.py, chainlink_client.py, erc677.py and chainlink_example.py into avm code. Please refer this [document](https://github.com/ontio/ontology-python-compiler) to learn how to use the ontology python compiler.
You can deploy contract by running 
``` shell
python3 ../run.py  -n erc677.py
python3 ../run.py  -n oracle.py
python3 ../run.py  -n chainlink_client.py
python3 ../../run.py  -n chainlink_example.py
```
3. Finally you can invoke [ontology sdk](https://github.com/ontio/ontology-java-sdk) function to deploy the avm code. 
