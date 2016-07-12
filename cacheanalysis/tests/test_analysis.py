import unittest
from datetime import datetime, timedelta

from cacheanalysis.analysis import BlockAnalysis
from cacheanalysis.collections import RecordCollection
from cacheanalysis.models import CacheMissRecord, CacheHitRecord, CacheDeleteRecord

_BLOCK_HASH_1 = "123"
_BLOCK_HASH_2 = "456"
_TIMESTAMP = datetime(year=2000, month=1, day=1)
_SIZE = 10


class TestAnalysis(unittest.TestCase):
    """
    Unit tests for `BlockAnalysis`.
    """
    def setUp(self):
        self.records = [
            CacheMissRecord(_BLOCK_HASH_1, _TIMESTAMP, _SIZE),
            CacheMissRecord(_BLOCK_HASH_2, _TIMESTAMP, _SIZE),
            CacheHitRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=1)),
            CacheDeleteRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=2)),
            CacheMissRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=3), _SIZE),
            CacheHitRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=4)),
            CacheHitRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=5))
        ]
        record_collection = RecordCollection()
        for record in self.records:
            record_collection.add_record(record)
        self.analysis = BlockAnalysis(record_collection)

    def test_block_hashes_when_empty(self):
        self.assertEqual(set(), BlockAnalysis(RecordCollection()).block_hashes)

    def test_block_hashes_when_not_empty(self):
        self.assertEqual({_BLOCK_HASH_1, _BLOCK_HASH_2}, self.analysis.block_hashes)


if __name__ == '__main__':
    unittest.main()
