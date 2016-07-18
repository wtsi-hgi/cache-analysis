from abc import abstractmethod
from collections import Counter
from math import ceil, pi

from matplotlib import pyplot as plt
from tabulate import tabulate

from cacheanalysis.analysis import Analysis
from cacheanalysis.statistical_analysis import StatisticalBlockAnalysis, StatisticalBlockFileAnalysis


class VisualAnalysis(Analysis):
    """
    Visualisation for the analysis of a collection of records.
    """
    @abstractmethod
    def visualise(self):
        """
        Visualises the collection of records.
        """


class VisualBlockAnalysis(VisualAnalysis):
    """
    Visualisation for the analysis of blocks that are put in a cache.
    """
    def __init__(self, record_collection):
        super().__init__(record_collection)
        self.statistical_analysis = StatisticalBlockAnalysis(record_collection)

    def visualise(self):
        """
        Visualises what happens to the blocks in the collection of records.
        """
        count = Counter()
        for block_hash in self.block_hashes:
            x = self.statistical_analysis.total_block_misses(block_hash)
            y = self.statistical_analysis.total_block_hits(block_hash)
            count[(x, y)] += 1
        xysize = []
        for k, v in count.items():
            xysize.append((*k, v))
        x, y, size = zip(*xysize)
        plt.scatter(x, y, s=size, c="blue", marker=".")
        plt.title("Cache misses against cache hits")
        plt.xlabel("Cache misses")
        plt.ylabel("Cache hits")
        plt.xlim(-0.5, max(10, max(x))+.5)
        plt.ylim(-0.5, max(10, max(y))+.5)
        plt.show()
        # print("Blocks sorted by number of accesses (hits + misses)")
        # # This shows basically how popular a block is
        # print(tabulate(
        #     sorted(
        #         [[block_hash, self.statistical_analysis.total_block_accesses(block_hash)]
        #          for block_hash in self.block_hashes],
        #         key=itemgetter(1),  # Sort by the second column
        #         reverse=True  # Sort descending
        #     )[:20],
        #     headers=("Block", "Accesses")
        # ))
        # print("Blocks sorted by mean number of cache hits (per miss) (higher is better)")
        # print(tabulate(
        #     sorted(
        #         [[block_hash, self.statistical_analysis.mean_block_hits(block_hash)]
        #          for block_hash in self.block_hashes],
        #         key=itemgetter(1),
        #         reverse=True
        #     )[:20],
        #     headers=("Block", "Mean cache hits")
        # ))


class VisualBlockFileAnalysis(VisualAnalysis):
    """
    Visualisation for the analysis of known blocks that are put in a cache.
    """
    def __init__(self, record_collection):
        super().__init__(record_collection)
        self.statistical_analysis = StatisticalBlockFileAnalysis(record_collection)

    def visualise(self):
        """
        Visualises what happens to the blocks in the collection of records, with
        information on what file each block belongs to.
        """
