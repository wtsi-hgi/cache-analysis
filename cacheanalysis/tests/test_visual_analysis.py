import unittest
from datetime import datetime

from cacheusagesimulator.usage_generator import UsageGenerator

from cacheanalysis.collections import RecordCollection
from cacheanalysis.visual_analysis import VisualBlockAnalysis


_BLOCK_HASH_1 = "123"
_BLOCK_HASH_2 = "456"
_BLOCK_HASH_3 = "789"
_TIMESTAMP = datetime(year=2000, month=1, day=1)
_SIZE = 10


class TestMyBlockVisualAnalysis(unittest.TestCase):
    """
    Unit tests for `MyBlockVisualAnalysis`.
    """
    def setUp(self):
        self.usage_generator = UsageGenerator()
        self.records = [self.usage_generator.generate() for _ in range(30000)]
        print("records:", len(self.records))
        print("average blocks read between reference reads:", self.usage_generator.average_block_reads_between_reference_block_read)
        record_collection = RecordCollection()
        for record in self.records:
            record_collection.add_record(record)
        self.analysis = MyBlockVisualAnalysis(record_collection)

    def test_visual_analysis(self):
        self.analysis.visualise()


if __name__ == "__main__":
    unittest.main()
