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
        TODO
        :param block_hash:
        :return:
        """
        # TODO

    def get_block_puts(self, block_hash: str) -> Set[CachePutRecord]:
        """
        TODO
        :param block_hash:
        :return:
        """
        # TODO

    def get_block_deletes(self, block_hash: str) -> Set[CacheDeleteRecord]:
        """
        TODO
        :param block_hash:
        :return:
        """
        # TODO
