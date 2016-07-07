from abc import ABCMeta
from datetime import datetime
from typing import List


class Record(metaclass=ABCMeta):
    """
    Record of an event involving a block.
    """
    def __init__(self, block_hash: str, timestamp: datetime):
        self.block_hash = block_hash
        self.timestamp = timestamp


class CacheAccessRecord(Record):
    """
    Record of an access of a block in a cache.
    """


class CachePutRecord(Record):
    """
    Record of the put of a block in a cache.
    """
    def __init__(self, block_hash: str, timestamp: datetime, block_size: int):
        super().__init__(block_hash, timestamp)
        self.block_size = block_size


class CacheDeleteRecord(Record):
    """
    Record of the deletion of a block from a cache.
    """


class BlockFile:
    """
    Model of a named file comprised of a list of blocks.
    """
    def __init__(self, name: str, block_hashes: List[str]):
        """
        Constructor.
        :param name: the name of the file
        :param block_hashes: the blocks that constitute the file
        """
        self.name = name
        self.block_hashes = block_hashes
