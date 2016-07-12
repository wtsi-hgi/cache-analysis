import unittest
from datetime import datetime, timedelta

from cacheanalysis.collections import RecordCollection
from cacheanalysis.models import CacheMissRecord, CacheHitRecord, CacheDeleteRecord
from cacheanalysis.visual_analysis import MyBlockVisualAnalysis

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
        self.records = [
            CacheMissRecord(_BLOCK_HASH_1, _TIMESTAMP, _SIZE),
            CacheMissRecord(_BLOCK_HASH_2, _TIMESTAMP, _SIZE),
            CacheHitRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=1)),
            CacheDeleteRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=2)),
            CacheMissRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=3), _SIZE),
            CacheHitRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=4)),
            CacheHitRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=5)),
            CacheDeleteRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=6)),
            CacheMissRecord(_BLOCK_HASH_3, _TIMESTAMP + timedelta(days=7), _SIZE),
            CacheDeleteRecord(_BLOCK_HASH_3, _TIMESTAMP + timedelta(days=8)),
            CacheMissRecord(_BLOCK_HASH_3, _TIMESTAMP + timedelta(days=9), _SIZE),
            CacheMissRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=10), _SIZE),
            CacheHitRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=11)),
            CacheHitRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=12)),
            CacheHitRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=13)),
            CacheHitRecord(_BLOCK_HASH_2, _TIMESTAMP + timedelta(days=15)),
            CacheDeleteRecord(_BLOCK_HASH_2, _TIMESTAMP + timedelta(days=16))
        ]
        record_collection = RecordCollection()
        for record in self.records:
            record_collection.add_record(record)
        self.analysis = MyBlockVisualAnalysis(record_collection)

    def test_visual_analysis(self):
        self.analysis.visualise()


if __name__ == "__main__":
    unittest.main()
