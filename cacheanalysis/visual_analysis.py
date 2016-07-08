from abc import abstractmethod

from cacheanalysis.analysis import Analysis
from cacheanalysis.analysis import BlockAnalysis


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


class MyBlockVisualAnalysis(BlockVisualAnalysis):
    """
    TODO
    """
    # TODO


class MyBlockFileVisualAnalysis(BlockFileVisualAnalysis):
    """
    TODO
    """
    # TODO
