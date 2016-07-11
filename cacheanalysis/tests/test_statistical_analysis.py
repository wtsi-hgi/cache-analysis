import unittest
from datetime import datetime, timedelta

from cacheanalysis.collections import RecordCollection
from cacheanalysis.models import CacheMissRecord, CacheHitRecord, CacheDeleteRecord
from cacheanalysis.statistical_analysis import StatisticalBlockAnalysis

_BLOCK_HASH_1 = "123"
_BLOCK_HASH_2 = "456"
_BLOCK_HASH_3 = "789"
_TIMESTAMP = datetime(year=2000, month=1, day=1)
_SIZE = 10


class TestStatisticalBlockAnalysis(unittest.TestCase):
    """
    Unit tests for `StatisticalBlockAnalysis`.
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
            CacheMissRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=10), _SIZE)
        ]
        record_collection = RecordCollection()
        for record in self.records:
            record_collection.add_record(record)
        self.analysis = StatisticalBlockAnalysis(record_collection)

    def test_total_block_misses_when_not_loaded(self):
        self.assertEqual(0, self.analysis.total_block_misses("other"))

    def test_total_block_misses_when_loaded(self):
        expected_loads = len(
            [record for record in self.records
             if record.block_hash == _BLOCK_HASH_1 and type(record) == CacheMissRecord]
        )
        self.assertEqual(expected_loads, self.analysis.total_block_misses(_BLOCK_HASH_1))

    def test_mean_block_hits_when_not_loaded(self):
        self.assertIsNone(self.analysis.mean_block_hits("other"))

    def test_mean_block_hits_when_loaded(self):
        self.assertEqual(1, self.analysis.mean_block_hits(_BLOCK_HASH_1))

    def test_mean_other_block_misses_between_reload_when_not_reloaded(self):
        self.assertIsNone(self.analysis.mean_other_block_misses_between_reload(_BLOCK_HASH_2))

    def test_mean_other_block_misses_between_reload_when_reloaded(self):
        self.assertEqual(1, self.analysis.mean_other_block_misses_between_reload(_BLOCK_HASH_1))

    # TODO: Tests for other methods


if __name__ == "__main__":
    unittest.main()
