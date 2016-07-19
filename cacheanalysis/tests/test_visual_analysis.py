import unittest
from datetime import datetime
from itertools import chain

from cacheusagesimulator.usage_generator import UsageGenerator

from cacheanalysis.collections import RecordCollection
from cacheanalysis.visual_analysis import VisualBlockAnalysis, VisualBlockFileAnalysis


_BLOCK_HASH_1 = "123"
_BLOCK_HASH_2 = "456"
_BLOCK_HASH_3 = "789"
_TIMESTAMP = datetime(year=2000, month=1, day=1)
_SIZE = 10


class TestVisualBlockAnalysis(unittest.TestCase):
    """
    Unit tests for `VisualBlockAnalysis`.
    """
    def setUp(self):
        self.usage_generator = UsageGenerator()
        self.records = [self.usage_generator.generate() for _ in range(30000)]
        print("records:", len(self.records))
        print("average blocks read between reference reads:", self.usage_generator.average_block_reads_between_reference_read)
        record_collection = RecordCollection()
        for record in self.records:
            record_collection.add_record(record)
        self.analysis = VisualBlockAnalysis(record_collection)

    def test_visual_analysis(self):
        self.analysis.visualise()


class TestVisualBlockFileAnalysis(unittest.TestCase):
    """
    Unit tests for `VisualBlockFileAnalysis`.
    """
    def setUp(self):
        self.usage_generator = UsageGenerator()
        self.records = [self.usage_generator.generate() for _ in range(30000)]
        print("records:", len(self.records))
        print("average blocks read between reference reads:", self.usage_generator.average_block_reads_between_reference_read)
        record_collection = RecordCollection()
        for record in self.records:
            record_collection.add_record(record)
        self.analysis = VisualBlockFileAnalysis(record_collection)

    def test_visual_analysis(self):
        blocks_to_display = list(chain.from_iterable([f.block_hashes for f in self.usage_generator.known_reference_files]))
        self.analysis.visualise(blocks_to_display)


if __name__ == "__main__":
    unittest.main()
