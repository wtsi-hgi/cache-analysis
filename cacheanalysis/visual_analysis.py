from abc import abstractmethod
from collections import Counter
from typing import List

from matplotlib import pyplot as plt
from tabulate import tabulate

from cacheanalysis.analysis import Analysis, BlockAnalysis, BlockFileAnalysis
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


class VisualBlockAnalysis(VisualAnalysis, BlockAnalysis):
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
        self.misses_vs_hits(plt, self.block_hashes, self.statistical_analysis)
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

    @staticmethod
    def misses_vs_hits(plot, block_hashes, statistical_analysis):
        count = Counter()
        for block_hash in block_hashes:
            x = statistical_analysis.total_block_misses(block_hash)
            y = statistical_analysis.total_block_hits(block_hash)
            count[(x, y)] += 1
        xysize = []
        for k, v in count.items():
            xysize.append((*k, v))
        x, y, size = zip(*xysize)
        plot.scatter(x, y, s=size, color="blue", marker="o", edgecolors="none")
        plot.title("Cache misses against cache hits")
        plot.xlabel("Cache misses")
        plot.ylabel("Cache hits")
        plot.xlim(-0.5, max(10, max(x)) + .5)
        plot.ylim(-0.5, max(10, max(y)) + .5)


class VisualBlockFileAnalysis(VisualBlockAnalysis, BlockFileAnalysis):
    """
    Visualisation for the analysis of known blocks that are put in a cache.
    """
    def __init__(self, record_collection):
        super().__init__(record_collection)
        self.statistical_analysis = StatisticalBlockFileAnalysis(record_collection)

    def visualise(self, display_hashes: List[str]=None):
        """
        Visualises what happens to the blocks in the collection of records, with
        information on what file each block belongs to.
        :param display_hashes: hashes of blocks to display. If None, will display all blocks.
        """
        plt.figure(figsize=(8, 12))

        plt.subplot(211)
        self.misses_vs_hits(plt, self.block_hashes, self.statistical_analysis)

        plt.subplot(212)
        self.misses_vs_hits(plt, filter(lambda x: not display_hashes or x in display_hashes,
                                        self.block_hashes), self.statistical_analysis)

        plt.show()
