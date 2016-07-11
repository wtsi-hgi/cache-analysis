from typing import Optional

from cacheanalysis.analysis import BlockAnalysis, BlockFileAnalysis
from cacheanalysis.models import CacheMissRecord


class StatisticalBlockAnalysis(BlockAnalysis):
    """
    Statistical analysis of blocks that are put into a cache.
    """
    def total_block_misses(self, block_hash: str) -> int:
        """
        Gets the total number of cache misses for the given block (times that a block has been
        loaded into the cache).
        :param block_hash: the block hash
        :return: the total number of times loaded
        """
        return len(self.record_collection.get_block_misses(block_hash))

    def mean_block_hits(self, block_hash: str) -> Optional[float]:
        """
        Gets the mean number of hits for the given block (accesses whilst it is in the cache). If
        the block has never been in the cache, `None` is returned.
        :param block_hash: the block hash
        :return: the mean number of accesses
        """
        misses = self.record_collection.get_block_misses(block_hash)
        hits = self.record_collection.get_block_hits(block_hash)
        deletes = self.record_collection.get_block_deletes(block_hash)
        if len(misses) == 0:
            return None
        # sort all records into chronological order
        records = sorted(
            [record for record in self.record_collection],
            key=lambda record: record.timestamp
        )
        block_in_cache = False
        block_hits = []
        for record in records:
            if record in misses:
                block_in_cache = True
                block_hits.append(0)
            elif record in deletes:
                block_in_cache = False
            elif record in hits and block_in_cache:
                block_hits[-1] += 1
        return sum(block_hits) / len(block_hits)

    def mean_other_block_misses_between_reload(self, block_hash: str) -> Optional[float]:
        """
        Gets the mean number of other block misses that took place between when the given block was
        deleted from the cache and then reloaded. If the given block has not been loaded into the
        cache, was not deleted once loaded or was not reloaded once deleted, `None` is returned.
        :param block_hash: the block hash
        :return: the mean number of other block loads between reloading
        """
        misses = self.record_collection.get_block_misses(block_hash)
        deletes = self.record_collection.get_block_deletes(block_hash)
        if len(misses) < 2 or len(deletes) == 0:
            return None
        # sort all records into chronological order
        records = sorted(
            [record for record in self.record_collection],
            key=lambda record: record.timestamp
        )
        block_in_cache = True  # don't include data before the block is added for the first time
        other_block_misses = []
        for record in records:
            if record in misses:
                block_in_cache = True
            elif record in deletes:
                block_in_cache = False
                other_block_misses.append(0)
            elif type(record) == CacheMissRecord and not block_in_cache:
                other_block_misses[-1] += 1
        return sum(other_block_misses) / len(other_block_misses)

    # TODO: Anything else that might be useful to know


class StatisticalBlockFileAnalysis(BlockFileAnalysis):
    """
    Statistical analysis of block files that are put into a cache.
    """
    # TODO: Anything interesting to know about block file access patterns
