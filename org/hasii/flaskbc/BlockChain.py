
from logging import getLogger
from logging import Logger

from typing import List

from hashlib import sha256

from org.hasii.flaskbc.Block import Block


class BlockChain(object):

    _mySelf: "BlockChain"

    def __init__(self):

        self.logger: Logger            = getLogger(__name__)
        self.chain:  List[Block]       = []
        self.current_node_transactions = []
        self.nodes                     = set()

        self.create_genesis_block()
        BlockChain._mySelf = self

    @property
    def get_serialized_chain(self):
        return [vars(block) for block in self.chain]

    @property
    def get_last_block(self) -> Block:
        return self.chain[-1]

    def create_genesis_block(self):
        self.create_new_block(proof=0, previous_hash=0)

    def create_new_block(self, proof, previous_hash):
        block = Block(
            index=len(self.chain),
            proof=proof,
            previous_hash=previous_hash,
            transactions=self.current_node_transactions
        )
        self.current_node_transactions = []  # Reset the transaction list

        self.chain.append(block)
        return block

    def create_new_transaction(self, sender, recipient, amount):
        self.current_node_transactions.append({
            'sender':    sender,
            'recipient': recipient,
            'amount':    amount
        })
        return True

    def is_valid_chain(self):
        """
        Check if given blockchain is valid
        """
        previous_block = self.chain[0]
        current_index = 1

        while current_index < len(self.chain):

            block = self.chain[current_index]

            if not self.is_valid_block(block, previous_block):
                return False

            previous_block = block
            current_index += 1

        return True

    def mine_block(self, miner_address):
        """
        Sender "0" means that this node has mined a new block
        For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)

        Args:
            miner_address:

        Returns:

        """
        self.create_new_transaction(sender="0", recipient=miner_address, amount=1)

        last_block: Block = self.get_last_block
        last_proof: int   = last_block.proof
        proof:      int   = self.create_proof_of_work(last_proof)

        last_hash: sha256 = last_block.get_block_hash
        block:     Block  = self.create_new_block(proof, last_hash)

        return vars(block)  # Return a native Dict type object

    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def is_valid_block(block, previous_block):
        if previous_block.index + 1 != block.index:
            return False

        elif previous_block.get_block_hash != block.previous_hash:
            return False

        elif not BlockChain.is_valid_proof(block.proof, previous_block.proof):
            return False

        elif block.timestamp <= previous_block.timestamp:
            return False

        return True

    @classmethod
    def create_proof_of_work(cls, previous_proof: int) -> int:
        """
        Generate "Proof Of Work"
        A very simple `Proof of Work` Algorithm -
            - Find a number such that, sum of the number and previous POW number is divisible by 7
        """
        proof = previous_proof + 1
        while not BlockChain.is_valid_proof(proof, previous_proof):
            proof += 1

        cls._mySelf.logger.info(f"proof: {proof}")
        return proof

    @staticmethod
    def is_valid_transaction():
        # Not Implemented
        pass

    @staticmethod
    def is_valid_proof(proof, previous_proof):
        return (proof + previous_proof) % 7 == 0

    @staticmethod
    def get_block_object_from_block_data(block_data):
        return Block(
            block_data['index'],
            block_data['proof'],
            block_data['previous_hash'],
            block_data['transactions'],
            timestamp=block_data['timestamp']
        )
