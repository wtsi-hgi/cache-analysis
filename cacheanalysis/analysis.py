from abc import ABCMeta
from collections import defaultdict
from typing import Dict, Set

from cacheanalysis.collections import RecordCollection
from cacheanalysis.models import BlockFile


class Analysis(metaclass=ABCMeta):
    """
    Analysis of a collection of records that describe how blocks are put into a cache.
    """
    def __init__(self, record_collection: RecordCollection):
        """
        Constructor.
        :param record_collection: the records that are to be analysed
        """
        self.record_collection = record_collection

    @property
    def block_hashes(self) -> Set[str]:
        """
        Gets a set of hashes of all the blocks that are known about in this analysis.
        :return: hashes of all known blocks
        """
        return set(self.record_collection.records.keys())


class BlockAnalysis(Analysis, metaclass=ABCMeta):
    """
    Analysis of a collection of records that describe how blocks are put into a cache.
    """
    pass


class BlockFileAnalysis(Analysis, metaclass=ABCMeta):
    """
    Analysis of a collection of records that describe how blocks are put into a cache with added
    information about the origin and relationship of blocks.
    """
    def __init__(self, record_collection: RecordCollection):
        """
        Constructor.
        :param record_collection: see `Analysis.__init__`
        """
        super().__init__(record_collection)
        self._known_blocks = defaultdict(set)   # type: Dict[str, Set[BlockFile]]

    def register_file(self, file: BlockFile):
        """
        Registers a block file with this analysis so that information is added about the potential
        origin of blocks and their relationship to each other.
        :param file: the block file
        """
        for block_id in file.block_hashes:
            self._known_blocks[block_id].add(file)
