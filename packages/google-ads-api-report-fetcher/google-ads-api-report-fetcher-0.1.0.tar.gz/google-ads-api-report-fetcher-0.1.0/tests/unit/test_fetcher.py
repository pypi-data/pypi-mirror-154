import pytest
from dataclasses import dataclass
from typing import Sequence
from operator import attrgetter

import gaarf.fetcher as fetcher
import gaarf.api_clients as api_clients
from gaarf.parsers import GoogleAdsRowParser
import gaarf.io.writer as writer

class FakeWriter(writer.AbsWriter):
    def __init__(self):
        pass

    def write(self, results, destination, header):
        return [header] + results

    def _define_header(self, results, header):
        return None


class FakeClient(api_clients.BaseClient):

    def __init__(self):
        pass

    def get_response(self, entity_id, query_text):
        return [FakeResult({
                    "campaign": {"id": 1} }
                )]

    def get_client(self):
        return None


class FakeResponse:

    def __init__(self, values):
        self.counter = 0
        self.batch = [values]

    def __iter__(self):
        return self

    def __next__(self):
        self.counter += 1
        return FakeResult(self.batch)

class FakeResult(dict):
    def __init__(self, results, *args, **kwargs):
        super(FakeResult, self).__init__(*args, **kwargs)
        self["results"] = self._traverse(results)

    def __getattr__(self, attr):
        return self.get(attr)

    def _traverse(self, custom_dict):
        tmp_dict = {}
        for key, value in custom_dict.items():
            if isinstance(value, dict):
                value = self._traverse(value)
            tmp_dict[key]= value
        return tmp_dict



query = "SELECT campaign.id FROM campaign"
customer_ids = {"1": "sample_account"}
api_client = FakeClient()
parser = GoogleAdsRowParser()
fake_writer = FakeWriter()


def test_get_response():
    response = api_client.get_response("1", query)
    assert response == [{"results": {
                    "campaign": {"id": 1} }
                }]

def test_get_correct_results():
    response = api_client.get_response("1", query)
    batches = []
    results = []
    getter = attrgetter("campaign.id")
    for batch in response:
       #  print(batch.results)
       #  results = [
       #      api_handler.parse_ads_row(row, getter, parser, None)
       #      for row in batch.results
       #  ]
        results.append([row for row in batch.results])
        batches.append(batch.results)

    assert batches[0] ==  {"campaign": {"id": 1}}
    assert results[0] ==  ["campaign"]
# def test_process_query():
#     results = fetcher.process_query(query, customer_ids, api_client, parser, fake_writer)
#     assert results == []

def test_save_results():
    results = fake_writer.write([(1, 2, 3)], "fake", ("one", "two", "three"))
    assert results == [("one", "two", "three"), (1, 2, 3)]
