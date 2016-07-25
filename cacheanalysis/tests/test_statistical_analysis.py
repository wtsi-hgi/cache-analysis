import unittest
from datetime import datetime, timedelta

from cacheanalysis.collections import RecordCollection
from cacheanalysis.models import CacheMissRecord, CacheHitRecord, CacheDeleteRecord, BlockFile
from cacheanalysis.statistical_analysis import StatisticalBlockAnalysis, StatisticalBlockFileAnalysis

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
        self.assertEqual(3, self.analysis.total_block_misses(_BLOCK_HASH_1))

    def test_total_block_hits_when_not_loaded(self):
        self.assertEqual(0, self.analysis.total_block_hits("other"))

    def test_total_block_hits_when_loaded(self):
        self.assertEqual(3, self.analysis.total_block_hits(_BLOCK_HASH_1))

    def test_mean_block_hits_when_not_loaded(self):
        self.assertIsNone(self.analysis.mean_block_hits("other"))

    def test_mean_block_hits_when_loaded(self):
        self.assertEqual(1, self.analysis.mean_block_hits(_BLOCK_HASH_1))

    def test_mean_other_block_misses_between_reload_when_not_reloaded(self):
        self.assertIsNone(self.analysis.mean_other_block_misses_between_reload(_BLOCK_HASH_2))

    def test_mean_other_block_misses_between_reload_when_reloaded(self):
        self.assertEqual(1, self.analysis.mean_other_block_misses_between_reload(_BLOCK_HASH_1))


class TestStatisticalBlockFileAnalysis(unittest.TestCase):
    """
    Unit tests for `StatisticalBlockFileAnalysis`.
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
        self.analysis = StatisticalBlockFileAnalysis(record_collection)
        block_file = BlockFile("blockfile", [_BLOCK_HASH_1, _BLOCK_HASH_2])
        self.analysis.register_file(block_file)

    def test_known_file_block_hit_to_miss_proportion(self):
        self.assertEqual(3/4, self.analysis.known_file_block_hit_to_miss_proportion())
        # If finding the mean proportion of hits to misses for each block, this will be 0.5
        # ((3/3 + 0/1)/2); if finding the total proportion of all hits to all misses, it will be
        # 0.75 (3 hits / 4 misses). Here, the total proportion is more useful.

    def test_not_known_file_block_hit_to_miss_proportion(self):
        self.assertEqual(0, self.analysis.not_known_file_block_hit_to_miss_proportion())


if __name__ == "__main__":
    unittest.main()
