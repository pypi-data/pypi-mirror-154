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

from uuid import uuid4
from hashlib import sha256
from json import dumps
from time import time
from dataclasses import dataclass
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import PKCS1_v1_5

# To import this module Class
# from cyberByte.blockChains.transactionModel import Transaction


@dataclass
class Transaction:
    """
    Transaction data class for the CyberByte cryptocurrency blockchain practice by Nikolai558.
    """

    def __init__(self, tx_to_address: str, tx_from_address: str, amount: float, from_public_key: str,
                 timestamp: int = None, transaction_hash: str = None, tx_id: str = None, _signature: str = None):
        """
        Transaction data class for the CyberByte cryptocurrency blockchain practice by Nikolai558. Only enter kwargs
        if recreating and verifying a transaction, otherwise leave as None.

        :param tx_to_address: [str] CyberByte Wallet Address for the user this transaction is TO.
        :param tx_from_address: [str] CyberByte Wallet Address for the user this transaction is FROM.
        :param amount: [float] Amount this transaction is in charge of.
        :param from_public_key: [str[hex]] Public key for the Address this transaction originated FROM in Hex value.
        :param timestamp: [int] Timestamp this transaction was generated in epoch time.
        :param transaction_hash: [str] Hash for this transaction.
        :param tx_id: [str[uuid]] Unique identifier for this transaction.
        :param _signature: [str] Signature that matches and is verifiable for the 'from_public_key' field.
        """
        self.tx_id: str = str(uuid4()) if tx_id is None else tx_id
        self.timestamp: int = int(time()) if timestamp is None else timestamp
        self.tx_to_address: str = tx_to_address
        self.tx_from_address: str = tx_from_address
        self.amount: float = amount
        self.from_public_key: str = bytes.fromhex(from_public_key).decode('utf-8')
        self.transaction_hash: str = self._get_hash() if transaction_hash is None else transaction_hash
        self._signature: str = _signature

    @property
    def tx_to_json_str(self) -> str:
        """
        Convert this Transaction object to a string that can be used to recreate this transaction.

        :return: This Transaction object as a Json String.
        """
        output = {**self.__dict__}
        output['from_public_key'] = RSA.importKey(output['from_public_key']).export_key().hex()
        return dumps(output)

    def _get_hash(self) -> str:
        """
        Get the hash for this Transaction Object. Note: The _signature attribute is NOT included in the hash.

        :return: string of the object hash.
        """
        output = {**self.__dict__}
        try:
            del output['_signature']
        except KeyError as e:
            if '_signature' not in str(e):
                raise e
        return sha256(str(output).encode('utf-8')).hexdigest()

    def sign(self, private_key: RsaKey):
        """
        Sign and add a signature to this Transaction Object.

        :param private_key: Private RsaKey for the CyberByte user
        :return: dictionary of all attributes for this Transaction
        """
        digest = SHA256.new()
        digest.update(self._get_hash().encode('utf-8'))
        signer = PKCS1_v1_5.new(private_key)
        self._signature = signer.sign(digest).hex()
        return {**self.__dict__}

    def is_verified(self) -> bool:
        """
        Checks the signature against all the data of this object to make sure that everything matches.

        :return: True if everything checks out, False if it is unverifiable.
        """
        if self._signature:
            digest = SHA256.new()
            digest.update(self._get_hash().encode('utf-8'))
            verifier = PKCS1_v1_5.new(RSA.importKey(self.from_public_key))
            verified = verifier.verify(digest, bytes.fromhex(self._signature))
            if verified:
                return True
            else:
                return False
        else:
            return False
