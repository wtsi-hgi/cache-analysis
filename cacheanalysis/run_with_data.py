import json
import sys

from cacheanalysis.collections import RecordCollection
from cacheanalysis.json_converters import RecordJSONDecoder, \
    BlockFileJSONDecoder

# PYTHONPATH=cache-usage-simulator/ python3 cache-usage-simulator/cacheusagesimulator/run_as_service.py
# PYTHONPATH=keep-cache-testing/ python2 keep-cache-testing/keepcachetest/run.py | PYTHONPATH=cache-analysis/ python3 cache-analysis/cacheanalysis/run_with_data.py
from cacheanalysis.visual_analysis import VisualBlockFileAnalysis

if __name__ == "__main__":
    with sys.stdin as input:
        json_as_string = input.read()

    json_as_dict = json.loads(json_as_string)
    records = RecordJSONDecoder().decode_parsed(json_as_dict["records"])
    reference_files = BlockFileJSONDecoder().decode_parsed(json_as_dict["references"])

    record_collection = RecordCollection(records)
    analysis = VisualBlockFileAnalysis(record_collection)
    for file in reference_files:
        analysis.register_file(file)

    print(analysis.statistical_analysis.total_block_hits(records[0].block_hash))

    analysis.visualise()
