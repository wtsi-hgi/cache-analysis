import json
from json import JSONDecoder

import dateutil.parser
from hgijson import JsonPropertyMapping, MappingJSONEncoderClassBuilder, MappingJSONDecoderClassBuilder
from typing import List

from cacheanalysis.models import BlockFile, CacheMissRecord, CacheHitRecord, \
    CacheDeleteRecord


_block_file_json_property_mappings = [
    JsonPropertyMapping("name", "name", object_constructor_parameter_name="name"),
    JsonPropertyMapping("block_hashes", "block_hashes", object_constructor_parameter_name="block_hashes")
]
BlockFileJSONEncoder = MappingJSONEncoderClassBuilder(BlockFile, _block_file_json_property_mappings).build()
BlockFileJSONDecoder = MappingJSONDecoderClassBuilder(BlockFile, _block_file_json_property_mappings).build()


class RecordJSONDecoder(JSONDecoder):
    _record_type_mapping = {
        "get": CacheHitRecord,
        "put": CacheMissRecord,
        "delete": CacheDeleteRecord
    }

    def decode(self, record_as_string, *kwargs):
        json_as_dict = json.loads(record_as_string)
        return self.decode_parsed(json_as_dict)

    def decode_parsed(self, json_as_dict):
        if isinstance(json_as_dict, List):
            return [self.decode_parsed(x) for x in json_as_dict]

        cls = RecordJSONDecoder._record_type_mapping[json_as_dict["type"]]
        block_hash = json_as_dict["hash"]
        block_timestamp = dateutil.parser.parse(json_as_dict["timestamp"])
        if cls == CacheMissRecord:
            size = json_as_dict["size"]
            return cls(block_hash, block_timestamp, size)
        else:
            return cls(block_hash, block_timestamp)
