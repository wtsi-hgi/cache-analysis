from collections import defaultdict
from typing import Dict

from typing import Set

from cacheanalysis.models import Record, CacheAccessRecord, CachePutRecord, CacheDeleteRecord


class RecordCollection:
    """
    TODO
    """
    def __init__(self):
        """
        Constructor.
        """
        self._records = defaultdict(set)  # type: Dict[type, Set[Record]]

    def add_record(self, record: Record):
        """
        Add a record to the collection.
        :param record:
        """
        self._records[type(record)].add(record)

    def get_block_accesses(self, block_hash: str) -> Set[CacheAccessRecord]:
        """
        Get all block accesses associated with the given block hash.
        :param block_hash:
        :return:
        """
        return set((record for record in self._records[CacheAccessRecord]
                    if record.block_hash == block_hash))

    def get_block_puts(self, block_hash: str) -> Set[CachePutRecord]:
        """
        Get all block puts associated with the given block hash.
        :param block_hash:
        :return:
        """
        return set((record for record in self._records[CachePutRecord]
                    if record.block_hash == block_hash))

    def get_block_deletes(self, block_hash: str) -> Set[CacheDeleteRecord]:
        """
        Get all block deletes associated with the given block hash.
        :param block_hash:
        :return:
        """
        return set((record for record in self._records[CacheDeleteRecord]
                    if record.block_hash == block_hash))
