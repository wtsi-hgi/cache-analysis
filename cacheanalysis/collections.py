from collections import abc, defaultdict, Iterator
from itertools import chain
from typing import Dict, Set, Iterable

from cacheanalysis.models import Record, CacheHitRecord, CacheMissRecord, CacheDeleteRecord


class RecordCollection(abc.Iterable, abc.Container):
    """
    TODO
    """
    def __init__(self, records: Iterable[Record]=None):
        """
        Constructor.
        """
        self._records = defaultdict(lambda: defaultdict(set))  # type: Dict[str, Dict[type, Set[Record]]]
        if records is not None:
            for record in records:
                self.add_record(record)

    def __contains__(self, item) -> bool:
        return item in set(self)

    def __iter__(self) -> Iterator:
        """
        Iterate over all records in the collection. Order will not be consistent.
        :return:
        """
        return chain.from_iterable(chain.from_iterable(
            [d.values() for d in self._records.values()]
        ))

    @property
    def records(self):
        return self._records

    def add_record(self, record: Record):
        """
        Add a record to the collection.
        :param record:
        """
        self._records[record.block_hash][type(record)].add(record)

    def get_block_hits(self, block_hash: str) -> Set[CacheHitRecord]:
        """
        Get all cache hits associated with the given block hash.
        :param block_hash:
        :return:
        """
        return self._records[block_hash][CacheHitRecord]

    def get_block_misses(self, block_hash: str) -> Set[CacheMissRecord]:
        """
        Get all cache misses associated with the given block hash.
        :param block_hash:
        :return:
        """
        return self._records[block_hash][CacheMissRecord]

    def get_block_deletes(self, block_hash: str) -> Set[CacheDeleteRecord]:
        """
        Get all block deletes associated with the given block hash.
        :param block_hash:
        :return:
        """
        return self._records[block_hash][CacheDeleteRecord]
