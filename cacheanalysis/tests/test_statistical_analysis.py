import unittest
from datetime import datetime, timedelta

from cacheanalysis.collections import RecordCollection
from cacheanalysis.models import CachePutRecord, CacheAccessRecord, CacheDeleteRecord
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
            CachePutRecord(_BLOCK_HASH_1, _TIMESTAMP, _SIZE),
            CachePutRecord(_BLOCK_HASH_2, _TIMESTAMP, _SIZE),
            CacheAccessRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=1)),
            CacheDeleteRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=2)),
            CachePutRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=3), _SIZE),
            CacheAccessRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=4)),
            CacheAccessRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=5)),
            CacheDeleteRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=6)),
            CachePutRecord(_BLOCK_HASH_3, _TIMESTAMP + timedelta(days=7), _SIZE),
            CacheDeleteRecord(_BLOCK_HASH_3, _TIMESTAMP + timedelta(days=8)),
            CachePutRecord(_BLOCK_HASH_3, _TIMESTAMP + timedelta(days=9), _SIZE),
            CachePutRecord(_BLOCK_HASH_1, _TIMESTAMP + timedelta(days=10), _SIZE)
        ]
        record_collection = RecordCollection()
        for record in self.records:
            record_collection.add_record(record)
        self.analysis = StatisticalBlockAnalysis(record_collection)

    def test_total_times_block_loaded_when_not_loaded(self):
        self.assertEqual(0, self.analysis.total_times_block_loaded("other"))

    def test_total_times_block_loaded_when_loaded(self):
        expected_loads = len([
            record for record in self.records
            if record.block_hash == _BLOCK_HASH_1 and type(record) == CachePutRecord
        ])
        self.assertEqual(expected_loads, self.analysis.total_times_block_loaded(_BLOCK_HASH_1))

    def test_mean_block_accesses_whilst_loaded_when_not_loaded(self):
        self.assertIsNone(self.analysis.mean_block_accesses_whilst_loaded("other"))

    def test_mean_block_accesses_whilst_loaded_when_loaded(self):
        self.assertEqual(1, self.analysis.mean_block_accesses_whilst_loaded(_BLOCK_HASH_1))

    def test_mean_other_block_loads_between_reload_when_not_reloaded(self):
        self.assertIsNone(self.analysis.mean_other_block_loads_between_reload(_BLOCK_HASH_2))

    def test_mean_other_block_loads_between_reload_when_reloaded(self):
        self.assertEqual(1, self.analysis.mean_other_block_loads_between_reload(_BLOCK_HASH_1))

    # TODO: Tests for other methods


if __name__ == "__main__":
    unittest.main()
