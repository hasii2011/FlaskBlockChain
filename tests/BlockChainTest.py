
from unittest import main as unitTestMain

from logging import getLogger
from logging import Logger

from hashlib import sha256

from org.hasii.flaskbc.BlockChain import BlockChain
from org.hasii.flaskbc.Block import Block
from tests.TestBase import TestBase


class BlockChainTest(TestBase):

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()

    def setUp(self):
        """"""

        self.logger: Logger = getLogger(__name__)

    def testBasic(self):

        blockchain: BlockChain = BlockChain()

        self.logger.info(">>>>> Before Mining...")
        self.logger.info(blockchain.chain)

        last_block: Block = blockchain.get_last_block
        last_proof: int    = last_block.proof
        proof:      int    = blockchain.create_proof_of_work(last_proof)

        self.logger.debug(f"proof: {proof}")
        #
        # Sender "0" means that this node has mined a new block
        # For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)
        #
        blockchain.create_new_transaction(sender="0", recipient="Gabby10Meows@gmail.com", amount=1)

        last_hash: sha256 = last_block.get_block_hash
        block = blockchain.create_new_block(proof, last_hash)
        self.logger.debug(f"new block:{block}")

        self.logger.info(">>>>> After Mining...")
        self.logger.info(blockchain.chain)

        self.logger.info("More mining")

        for x in range(7):
            minerAddress: str = f"humberto.a.sanchez.{x}@gmail.com"
            minedBlock = blockchain.mine_block(miner_address=minerAddress)
            self.logger.info(f"minedBlock: {minedBlock}")

        self.logger.info(">>>>> After More Mining...")
        self.logger.info(blockchain.chain)

    def testCreateProofOfWork(self):

        blockchain: BlockChain = BlockChain()
        x = 0
        currentProof: int = 0
        while x < 7:
            currentProof = blockchain.create_proof_of_work(currentProof)
            self.assertEqual(currentProof % 7, 0, "Proof is not mod 7")
            self.logger.debug(f"Current iteration: {x} currentProof: {currentProof}")
            x += 1


if __name__ == '__main__':
    unitTestMain()
