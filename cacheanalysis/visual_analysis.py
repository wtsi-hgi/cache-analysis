from abc import abstractmethod
from operator import itemgetter

from tabulate import tabulate

from cacheanalysis.analysis import Analysis, BlockAnalysis
from cacheanalysis.statistical_analysis import StatisticalBlockAnalysis


class VisualAnalysis(Analysis):
    """
    Visualisation for the analysis of a collection of records.
    """
    @abstractmethod
    def visualise(self):
        """
        Visualises the collection of records.
        """


class BlockVisualAnalysis(VisualAnalysis, BlockAnalysis):
    """
    Visualisation for the analysis of blocks that are put in a cache.
    """
    @abstractmethod
    def visualise(self):
        """
        Visualises what happens to the blocks in the collection of records.
        """


class BlockFileVisualAnalysis(BlockVisualAnalysis):
    """
    Visualisation for the analysis of known blocks that are put in a cache.
    """
    @abstractmethod
    def visualise(self):
        """
        Visualises what happens to the blocks in the collection of records, with
        information on what file each block belongs to.
        """


class MyBlockVisualAnalysis(BlockVisualAnalysis, StatisticalBlockAnalysis):
    """
    TODO
    """
    def visualise(self):
        print("Blocks sorted by number of accesses (hits + misses)")
        print(tabulate(
            sorted(
                [[block_hash, self.total_block_misses(block_hash)
                  + self.total_block_hits(block_hash)]
                 for block_hash in self.block_hashes],
                key=itemgetter(1),  # Sort by the second column
                reverse=True  # Sort descending
            ),
            headers=("Block", "Accesses")
        ))
        print("Blocks sorted by number of cache misses (high is bad)")
        print(tabulate(
            sorted(
                [[block_hash, self.total_block_misses(block_hash)]
                 for block_hash in self.block_hashes],
                key=itemgetter(1),
                reverse=True
            ),
            headers=("Block", "Cache misses")
        ))
        print("Blocks sorted by cache hits over cache misses (low is bad)")
        print(tabulate(
            sorted(
                [[block_hash,
                  self.total_block_hits(block_hash) / self.total_block_misses(block_hash)]
                 for block_hash in self.block_hashes],
                key=itemgetter(1)
            ),
            headers=("Block", "Hits per miss")
        ))


class MyBlockFileVisualAnalysis(BlockFileVisualAnalysis):
    """
    TODO
    """
    # TODO
