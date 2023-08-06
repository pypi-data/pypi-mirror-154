#
#     Copyright (C) 2022  Nikolas Boling
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, version 3 of the License any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see
#     https://github.com/Nikolai558/CyberByte/blob/development/LICENSE.txt.
#

from json import loads, dumps
from time import time

from .transactionModel import Transaction
from .blockModel import Block

CHECK_CHAIN_LENGTH = 1024


class Blockchain:
    def __init__(self, difficulty: int = None, mem_pool: list[Transaction | str] = None,
                 chain: list[Block | str] = None):
        self.difficulty: int = 7 if difficulty is None else difficulty
        self.mem_pool: list[Transaction | str] = [] if mem_pool is None else mem_pool
        self.chain: list[Block | str] = [] if chain is None else chain

        if not self.chain:
            self.create_genesis_block()

    @property
    def last_block(self) -> Block:
        return self.chain[-1] if type(self.chain[-1]) == Block else Block(**loads(self.chain[-1].block_to_json_str))

    @property
    def chain_length(self) -> int:
        return len(self.chain)

    @property
    def is_valid_chain(self) -> bool:
        if self.chain_length > CHECK_CHAIN_LENGTH:
            check_chain = self.chain[-CHECK_CHAIN_LENGTH:]
        else:
            check_chain = self.chain
        prev_block: [Block | None] = None
        for current_block in check_chain:
            if type(current_block) == str:
                current_block = Block(**loads(current_block))
            if prev_block is None:
                prev_block = current_block
            else:
                if current_block.previous_hash != prev_block.current_hash:
                    return False
            if not current_block.is_block_verified:
                return False
        return True

    @property
    def chain_to_json_str(self) -> str:
        output = {**self.__dict__,
                  "mem_pool": [x.tx_to_json_str if type(x) is Transaction else x for x in self.mem_pool],
                  "chain": [x.block_to_json_str if type(x) is Block else x for x in self.chain]}
        return dumps(output)

    @property
    def miner_reward(self) -> float:
        amt = 250.0
        if (self.chain_length // 1024) > 0:
            for _ in range(1, (self.chain_length // 1000) + 1):
                amt = round(amt / 2, 9)
        return amt

    def create_genesis_block(self) -> None:
        genesis_block = Block(
            # Genesis Block - The very first block for CryptoByte! Wahoo!
            miner_address="051760882eeffe2e70df562a72e43437829c4b4d9573ed585d0b29327da7cf74",
            index=0,
            timestamp=int(time()),
            transactions=[],
            previous_hash="0"*64,
            nonce=0,
            _fee_total=0.0
        )
        self.chain.append(genesis_block)

    def check_difficulty(self) -> None:
        if self.difficulty <= 10:
            self.difficulty = 10
        if self.difficulty >= 256:
            self.difficulty = 256

    def is_valid_proof(self, block: Block) -> bool:
        self.check_difficulty()
        if block.previous_hash != self.last_block.current_hash:
            return False
        if int(block.current_hash, 16) > 2**(256-self.difficulty):
            return False
        return True

    def replace_chain_with_longest(self, chain: str) -> bool:
        other_chain = Blockchain(**loads(chain))
        if not other_chain.is_valid_chain:
            return False
        if other_chain.chain_length <= self.chain_length:
            return False
        self.difficulty: int = other_chain.difficulty
        self.mem_pool: list[Transaction | str] = other_chain.mem_pool
        self.chain: list[Block | str] = other_chain.chain
        return True
