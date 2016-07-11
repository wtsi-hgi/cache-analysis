from typing import Optional

from cacheanalysis.analysis import BlockAnalysis, BlockFileAnalysis
from cacheanalysis.models import CachePutRecord


class StatisticalBlockAnalysis(BlockAnalysis):
    """
    Statistical analysis of blocks that are put into a cache.
    """
    def total_times_block_loaded(self, block_hash: str) -> int:
        """
        Gets the total number of times that a block has been loaded into the cache.
        :param block_hash: the block hash
        :return: the total number of times loaded
        """
        return len(self.record_collection.get_block_puts(block_hash))

    def mean_block_accesses_whilst_loaded(self, block_hash: str) -> Optional[float]:
        """
        Gets the mean number of accesses for the given block whilst it is in the cache. If the
        block has never been in the cache, `None` is returned.
        :param block_hash: the block hash
        :return: the mean number of accesses
        """
        # TODO

    def mean_other_block_loads_between_reload(self, block_hash: str) -> Optional[float]:
        """
        Gets the mean number of other block loads that took place between when the given block was
        deleted from the cache and then reloaded. If the given block has not been loaded into the
        cache or was not deleted once loaded, `None` is returned.
        :param block_hash: the block hash
        :return: the mean number of other block loads between reloading
        """
        puts = self.record_collection.get_block_puts(block_hash)
        deletes = self.record_collection.get_block_deletes(block_hash)
        if len(puts) < 2 or len(deletes) == 0:
            return None
        # sort all records into chronological order
        records = sorted(
            [record for record in self.record_collection],
            key=lambda record: record.timestamp
        )
        block_in_cache = True  # don't include data before the block is added for the first time
        other_block_loads = []
        for record in records:
            if record in puts:
                block_in_cache = True
            elif record in deletes:
                block_in_cache = False
                other_block_loads.append(0)
            elif type(record) == CachePutRecord and not block_in_cache:
                other_block_loads[-1] += 1
        return sum(other_block_loads) / len(other_block_loads)

    # TODO: Anything else that might be useful to know


class StatisticalBlockFileAnalysis(BlockFileAnalysis):
    """
    Statistical analysis of block files that are put into a cache.
    """
    # TODO: Anything interesting to know about block file access patterns
