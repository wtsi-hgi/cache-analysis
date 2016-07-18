from abc import abstractmethod
from operator import itemgetter

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
