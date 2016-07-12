from collections import abc, defaultdict
from itertools import chain
from typing import Dict, Set, Iterator

from cacheanalysis.models import Record, CacheHitRecord, CacheMissRecord, CacheDeleteRecord


class RecordCollection(abc.Iterable, abc.Container):
    """
    TODO
    """
    def __init__(self):
        """
        Constructor.
        """
        self._records = defaultdict(set)  # type: Dict[type, Set[Record]]

    def __contains__(self, item) -> bool:
        return item in set(chain.from_iterable(self._records.values()))

    def __iter__(self) -> Iterator:
        """
        Iterate over all records in the collection. Order will not be consistent.
        :return:
        """
        return iter(set(chain.from_iterable(self._records.values())))

    def add_record(self, record: Record):
        """
        Add a record to the collection.
        :param record:
        """
        self._records[type(record)].add(record)

    def get_block_hits(self, block_hash: str) -> Set[CacheHitRecord]:
        """
        Get all cache hits associated with the given block hash.
        :param block_hash:
        :return:
        """
        return set((record for record in self._records[CacheHitRecord]
                    if record.block_hash == block_hash))

    def get_block_misses(self, block_hash: str) -> Set[CacheMissRecord]:
        """
        Get all cache misses associated with the given block hash.
        :param block_hash:
        :return:
        """
        return set((record for record in self._records[CacheMissRecord]
                    if record.block_hash == block_hash))

    def get_block_deletes(self, block_hash: str) -> Set[CacheDeleteRecord]:
        """
        Get all block deletes associated with the given block hash.
        :param block_hash:
        :return:
        """
        return set((record for record in self._records[CacheDeleteRecord]
                    if record.block_hash == block_hash))
