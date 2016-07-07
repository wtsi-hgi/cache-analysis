from abc import ABCMeta

from cacheanalysis.analysis import Analysis, BlockFileAnalysis
from cacheanalysis.analysis import BlockAnalysis


class VisualAnalysis(Analysis, metaclass=ABCMeta):
    """
    Visualisation for the analysis of a collection of records.
    """
    def visualise(self):
        """
        Visualises the collection of records.
        """


class BlockVisualAnalysis(VisualAnalysis, BlockAnalysis, metaclass=ABCMeta):
    """
    Visualisation for the analysis of blocks that are put in a cache.
    """
    def visualise(self):
        """
        Visualises what happens to the blocks in the collection of records.
        """


class BlockFileVisualAnalysis(VisualAnalysis, BlockFileAnalysis, metaclass=ABCMeta):
    """
    Visualisation for the analysis of known blocks that are put in a cache.
    """
    def visualise(self):
        """
        Visualises what happens to the blocks in the collection of records, with
        information on what file each block belongs to.
        """


class MyBlockVisualAnalysis(BlockVisualAnalysis):
    """
    TODO
    """
    # TODO


class MyBlockFileVisualAnalysis(BlockVisualAnalysis):
    """
    TODO
    """
    # TODO
