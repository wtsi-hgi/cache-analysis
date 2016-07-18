import json
import sys

from cacheanalysis.collections import RecordCollection
from cacheanalysis.json_converters import RecordJSONDecoder, \
    BlockFileJSONDecoder
from cacheanalysis.statistical_analysis import StatisticalBlockFileAnalysis


if __name__ == "__main__":
    with sys.stdin as input:
        json_as_string = input.read()

    json_as_dict = json.loads(json_as_string)
    records = RecordJSONDecoder().decode_parsed(json_as_dict["records"])
    reference_files = BlockFileJSONDecoder().decode_parsed(json_as_dict["references"])

    record_collection = RecordCollection(records)
    analysis = StatisticalBlockFileAnalysis(record_collection)
    for file in reference_files:
        analysis.register_file(file)

    print(analysis.total_block_hits(records[0].block_hash))
