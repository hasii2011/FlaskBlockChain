
It is best to install the support libraries in a virtual environment

***
e.g.

```commandline
python3 -m venv venv-flask-3.9.7
pip3 install flask
pip3 install requests
```

There are two unit test programs in `tests` package

* `BlockChainTest.py` - test the basic classes
* `DistributedBlockChainTest.py` - Depends on having 2 servers running on ports 9000 and 7575 

