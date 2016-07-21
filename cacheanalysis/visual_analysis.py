from abc import abstractmethod
from collections import Counter
from itertools import chain
from typing import Iterable, List, Sequence, Tuple

import matplotlib as mpl
from matplotlib import pyplot as plt
from tabulate import tabulate

from cacheanalysis.analysis import Analysis, BlockAnalysis, BlockFileAnalysis
from cacheanalysis.models import BlockFile
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

    def visualise(self, highlight_blocks: Sequence[str]=()):
        """
        Visualises what happens to the blocks in the collection of records.
        :param highlight_blocks: a list of block hashes to highlight.
        """
        fig = plt.figure()
        # Double the height of the figure so that subplots do not overlap.
        fig.set_figheight(fig.get_figheight() * 2, forward=True)

        ax1 = fig.add_subplot(2, 1, 1)  # rows, columns, subplot number (1-indexed)
        ax1.set_title("Cache misses against cache hits")
        x, y, size = self.get_misses_against_hits(self.block_hashes, self.statistical_analysis)
        self.plot_misses_against_hits(ax1, x, y, s=size)
        self.set_limits(ax1, x, y)
        if highlight_blocks:
            x, y, size = self.get_misses_against_hits(
                [h for h in self.block_hashes if h in highlight_blocks], self.statistical_analysis
            )
            self.plot_misses_against_hits(ax1, x, y, s=size, c="cyan")

        ax2 = fig.add_subplot(2, 1, 2)
        ax2.set_title("Cache accesses against mean cache hits per miss")
        x, y, size = self.get_accesses_against_mean_hits(self.block_hashes, self.statistical_analysis)
        self.plot_accesses_against_mean_hits(ax2, x, y, s=size)
        self.set_limits(ax2, x, y)
        if highlight_blocks:
            x, y, size = self.get_accesses_against_mean_hits(
                [h for h in self.block_hashes if h in highlight_blocks], self.statistical_analysis
            )
            self.plot_misses_against_hits(ax2, x, y, s=size, c="cyan")

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
    def get_misses_against_hits(block_hashes: Iterable[str], statistical_analysis: StatisticalBlockAnalysis) -> Tuple[List[int], List[int], List[int]]:
        count = Counter()
        for block_hash in block_hashes:
            x = statistical_analysis.total_block_misses(block_hash)
            y = statistical_analysis.total_block_hits(block_hash)
            count[(x, y)] += 1
        xysize = []
        for k, v in count.items():
            xysize.append((*k, v))
        x, y, size =  zip(*xysize)
        return x, y, size

    @staticmethod
    def plot_misses_against_hits(ax: mpl.axes.Axes, x: Sequence[int], y: Sequence[int], **kwargs) -> mpl.collections.PathCollection:
        ax.set_xlabel("Cache misses")
        ax.set_ylabel("Cache hits")
        return ax.scatter(x, y, edgecolors="none", **kwargs)

    @staticmethod
    def get_accesses_against_mean_hits(block_hashes: Iterable[str], statistical_analysis: StatisticalBlockAnalysis) -> Tuple[List[int], List[int], List[int]]:
        count = Counter()
        for block_hash in block_hashes:
            x = statistical_analysis.total_block_misses(block_hash) \
                + statistical_analysis.total_block_hits(block_hash)
            y = statistical_analysis.mean_block_hits(block_hash)
            count[(x, y)] += 1
        xysize = []
        for k, v in count.items():
            xysize.append((*k, v))
        x, y, size =  zip(*xysize)
        return x, y, size

    @staticmethod
    def plot_accesses_against_mean_hits(ax: mpl.axes.Axes, x: Sequence[int], y: Sequence[int], **kwargs) -> mpl.collections.PathCollection:
        ax.set_xlabel("Cache accesses")
        ax.set_ylabel("Mean cache hits")
        return ax.scatter(x, y, edgecolors="none", **kwargs)

    @staticmethod
    def set_limits(ax, x, y):
        ax.set_xlim(-.1*(max(x)-min(x)), max(x) + .1*(max(x)-min(x)))
        ax.set_ylim(-.1*(max(y)-min(y)), max(y) + .1*(max(y)-min(y)))


class VisualBlockFileAnalysis(VisualBlockAnalysis, BlockFileAnalysis):
    """
    Visualisation for the analysis of known blocks that are put in a cache.
    """
    def __init__(self, record_collection):
        super().__init__(record_collection)
        self.statistical_analysis = StatisticalBlockFileAnalysis(record_collection)

    def visualise(self, highlight_blocks: Sequence[str]=(), highlight_files: Sequence[BlockFile]=()):
        """
        Visualises what happens to the blocks in the collection of records, with
        information on what file each block belongs to.
        :param highlight_blocks: a list of block hashes to highlight. Combined with
        `highlight_files`.
        :param highlight_files: a list of files to highlight. Combined with `highlight_blocks`.
        """
        super().visualise(list(highlight_blocks) + list(chain.from_iterable([f.block_hashes for f in highlight_files])))
