import unittest
from datetime import datetime, timedelta

from cacheanalysis.collections import RecordCollection
from cacheanalysis.models import CacheMissRecord, CacheHitRecord, CacheDeleteRecord

_BLOCK_HASH_1 = "123"
_BLOCK_HASH_2 = "456"
_BLOCK_HASH_3 = "789"
_TIMESTAMP = datetime(year=2000, month=1, day=1)
_SIZE = 10


class TestRecordCollection(unittest.TestCase):
    """
    Unit tests for `RecordCollection`.
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
        self.record_collection = RecordCollection()
        for record in self.records:
            self.record_collection.add_record(record)

    def test_contains_without_records(self):
        self.assertCountEqual([], RecordCollection())

    def test_contains_with_records(self):
        self.assertCountEqual(self.records, self.record_collection)

    def test_iterate_without_records(self):
        self.assertCountEqual(set(), set(RecordCollection()))

    def test_iterate_with_records(self):
        self.assertCountEqual(set(self.records), set(self.record_collection))

    def test_get_block_hits(self):
        self.assertEqual(3, len(self.record_collection.get_block_hits(_BLOCK_HASH_1)))

    def test_get_block_misses(self):
        self.assertEqual(2, len(self.record_collection.get_block_misses(_BLOCK_HASH_1)))

    def test_get_block_deletes(self):
        self.assertEqual(1, len(self.record_collection.get_block_deletes(_BLOCK_HASH_1)))


if __name__ == "__main__":
    unittest.main()
