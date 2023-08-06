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
from hashlib import sha256
from json import dumps, loads
from dataclasses import dataclass
from time import time

from .transactionModel import Transaction


@dataclass
class Block:
    def __init__(self, miner_address, index=None, timestamp=None, transactions=None, previous_hash=None, nonce=None,
                 current_hash=None, _fee_total=None):
        self.index: int = 0 if index is None else index
        self.timestamp: int = int(time()) if timestamp is None else timestamp
        self.transactions: list[Transaction | str] = [] if transactions is None else transactions
        self.previous_hash: str = "None" if previous_hash is None else previous_hash
        self.nonce: int = 0 if nonce is None else nonce
        self.miner_address: str = miner_address
        self._fee_total: float = self.fee_total if _fee_total is None else _fee_total
        self.current_hash: str = self._get_hash() if current_hash is None else current_hash

    @property
    def fee_total(self):
        total = 0.0
        for t in self.transactions:
            if type(t) == str:
                t = Transaction(**loads(t))
            total += t.fee
        return round(total, 6)

    @property
    def block_to_json_str(self) -> str:
        output = {**self.__dict__, 'transactions': self._convert_all_tx_to_json()}
        return dumps(output)

    def _get_hash(self) -> str:
        output = {**self.__dict__, 'transactions': self._convert_all_tx_to_json()}
        for i in ['current_hash']:
            try:
                del output[i]
            except KeyError as e:
                if i not in str(e):
                    raise e
        _hash = sha256(str(output).encode('utf-8')).hexdigest()
        return _hash

    def _all_transactions_verified(self) -> bool:
        if self.transactions:
            for t in self.transactions:
                if type(t) == str:
                    t = Transaction(**loads(t))
                if not t.is_verified():
                    return False
        return True

    @property
    def is_block_verified(self):
        if not self._all_transactions_verified():
            return False
        if self.current_hash != self._get_hash():
            return False
        return True

    def _convert_all_tx_to_json(self) -> list[str]:
        output = []
        if self.transactions:
            for t in self.transactions:
                if type(t) == str:
                    output.append(t)
                elif type(t) == Transaction:
                    output.append(t.tx_to_json_str)
                else:
                    raise ValueError("Transaction in list is not of type str or Transaction: {}".format(type(t)))
        return output
