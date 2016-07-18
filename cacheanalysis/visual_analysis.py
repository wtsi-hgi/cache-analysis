from abc import abstractmethod
from operator import itemgetter
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
        x = [self.statistical_analysis.total_block_misses(block_hash) for block_hash in self.block_hashes]
        y = [self.statistical_analysis.total_block_hits(block_hash) for block_hash in self.block_hashes]
        point_sizes = [[0 for y in range(max(y) + 1)] for x in range(max(x) + 1)]
        for block_hash in self.block_hashes:
            _x = self.statistical_analysis.total_block_misses(block_hash)
            _y = self.statistical_analysis.total_block_hits(block_hash)
            point_sizes[_x][_y] += 1
        area = [[0 for y in range(max(y) + 1)] for x in range(max(x) + 1)]
        for _x, v in enumerate(point_sizes):
            for _y, _ in enumerate(v):
                area[_x][_y] = pi * ceil(point_sizes[_x][_y] * 0.005)**2
        plt.scatter(x, y, s=area, c="black", marker="o")
        # Colour must be black to avoid artifacts when multiple points are drawn on top of each other
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
