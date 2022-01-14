
from logging import getLogger
from logging import Logger

import requests

from tests.TestBase import TestBase


class DistributedBlockChainTest(TestBase):

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()

    def setUp(self):
        """"""

        self.logger: Logger = getLogger(__name__)

    def testDistributed(self):

        server1: str = 'http://127.0.0.1:7575'
        server2: str = 'http://127.0.0.1:9000'

        self._register_node(server2, server1)  # server2 node will be register inside server1

        self._create_transaction(server2, {'sender': 'I', 'recipient': 'Gabby10Meows', 'amount': 3})

        self._mine_block(server2)  # Mined a new block on server2

        self._get_server_chain(server1)  # server1's chain
        self._get_server_chain(server2)  # server2's chain

        self._sync_chain(server1)  # updating server1's chain with neighbour node's chain

        self._get_server_chain(server1)  # server1's chain after syncing

    def _register_node(self, node_addr, parent_server):
        requests.post(parent_server + '/register-node', json={'address': node_addr})
        self.logger.info(f"On Server {parent_server}: Node-{node_addr} has been registered successfully!")

    def _create_transaction(self, server: str, data):
        requests.post(server + '/create-transaction', json=data).json()
        self.logger.info(f"On Server {server}: Transaction has been processed!")

    def _mine_block(self, server: str):
        requests.get(server + '/mine').json()
        self.logger.info(f"On Server {server}: Block has been mined successfully!")

    def _get_server_chain(self, server: str):
        resp = requests.get(server + '/chain').json()
        self.logger.info(f"On Server {server}: Chain is-{resp}")
        return resp

    def _sync_chain(self, server: str):
        self.logger.info(f"On Server {server}: Started Syncing Chain . . .")
        resp = requests.get(f"{server}/sync-chain")
        self.logger.info("On Server {server}: Chain synced!")
        self.logger.info(f"resp: {resp}")
