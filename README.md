
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

If you do not have an IDE like PyCharm to set up run configurations then you can 
manually run the distributed tests as follows:

Start the first server

```commandline
python3 -m org.hasii.flaskbc.flaskmain --port 7575
```

Start the second server

```commandline
python3 -m org.hasii.flaskbc.flaskmain --port 9000
```

Run the test program

```commandline
python3 -m unittest tests.DistributedBlockChainTest
```
