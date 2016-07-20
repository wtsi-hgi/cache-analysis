from abc import abstractmethod
from collections import Counter
from typing import Iterable, List, Sequence, Tuple

import matplotlib
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
        # self.plot_misses_hits(plt, self.block_hashes, self.statistical_analysis)
        # plt.show()

        fig = plt.figure()

        ax = fig.add_subplot(1, 1, 1)  # 1 row, 1 column, 1st subplot
        ax.set_title("Cache misses against cache hits")
        x, y, size = self.get_misses_hits(self.block_hashes, self.statistical_analysis)
        self.plot_misses_hits(ax, x, y, s=size)

        plt.show()

        plt.close(fig)  # pyplot keeps a reference to fig unless close() is called.

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
    def get_misses_hits(block_hashes: Iterable[str], statistical_analysis: StatisticalBlockAnalysis) -> Tuple[List[int], List[int], List[int]]:
        count = Counter()
        for block_hash in block_hashes:
            x = statistical_analysis.total_block_misses(block_hash)
            y = statistical_analysis.total_block_hits(block_hash)
            count[(x, y)] += 1
        xysize = []
        for k, v in count.items():
            xysize.append((*k, v))
        return zip(*xysize)

    @staticmethod
    def plot_misses_hits(ax: matplotlib.axes.Axes, x: Sequence[int], y: Sequence[int], **kwargs) -> matplotlib.collections.PathCollection:
        ax.set_xlabel("Cache misses")
        ax.set_ylabel("Cache hits")
        ax.set_xlim(-0.5, max(10, max(x)) + .5)
        ax.set_ylim(-0.5, max(10, max(y)) + .5)
        return ax.scatter(x, y, edgecolors="none", **kwargs)


class VisualBlockFileAnalysis(VisualBlockAnalysis, BlockFileAnalysis):
    """
    Visualisation for the analysis of known blocks that are put in a cache.
    """
    def __init__(self, record_collection):
        super().__init__(record_collection)
        self.statistical_analysis = StatisticalBlockFileAnalysis(record_collection)

    def visualise(self, display_hashes: Sequence[str]=()):
        """
        Visualises what happens to the blocks in the collection of records, with
        information on what file each block belongs to.
        :param display_hashes: hashes of blocks to display. If empty, will display all blocks.
        """
        fig = plt.figure()

        ax1 = fig.add_subplot(2 if display_hashes else 1, 1, 1)
        ax1.set_title("Cache misses against cache hits")
        x, y, size = self.get_misses_hits(self.block_hashes, self.statistical_analysis)
        self.plot_misses_hits(ax1, x, y, s=size)

        if display_hashes:
            # Double the height of the figure so that subplots do not overlap.
            fig.set_figheight(fig.get_figheight() * 2, forward=True)
            ax2 = fig.add_subplot(2, 1, 2)
            ax2.set_title("Cache misses against cache hits, filtered")
            x, y, size = self.get_misses_hits(
                [h for h in self.block_hashes if h in display_hashes], self.statistical_analysis
            )
            self.plot_misses_hits(ax2, x, y, s=size)

        plt.show()

        plt.close(fig)
