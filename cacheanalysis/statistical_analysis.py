from typing import Optional

from operator import attrgetter

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

    def total_block_hits(self, block_hash: str) -> int:
        """
        Gets the total number of cache hits for the given block (times that a block has been served
        from the cache).
        :param block_hash:
        :return:
        """
        return len(self.record_collection.get_block_hits(block_hash))

    def mean_block_hits(self, block_hash: str) -> Optional[float]:
        """
        Gets the mean number of hits for the given block (accesses whilst it is in the cache). If
        the block has never been in the cache, `None` is returned.
        :param block_hash: the block hash
        :return: the mean number of accesses
        """
        misses = self.record_collection.get_block_misses(block_hash)
        hits = self.record_collection.get_block_hits(block_hash)
        if len(misses) == 0:
            return None
        return len(hits)/len(misses)

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
            key=attrgetter("timestamp")
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


class StatisticalBlockFileAnalysis(StatisticalBlockAnalysis, BlockFileAnalysis):
    """
    Statistical analysis of block files that are put into a cache.
    """
    def known_file_block_hit_to_miss_proportion(self) -> float:
        """
        Gets the proportion of hits to misses for the blocks in all of the known
        files.
        :return: the ratio of hits to misses
        """
        # TODO

    def not_known_file_block_hit_to_miss_proportion(self) -> float:
        """
        Gets the proportion of hits to misses for the blocks not in the known
        files.
        :return: the ratio of hits to misses
        """
        # TODO

    # TODO: Anything else interesting to know about block file access patterns
