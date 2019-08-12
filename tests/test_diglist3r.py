import json
import pytest
from functools import partial
import diglist3r


def get_config_file(input):
    if input is None:
        input = "a.json"
    return input

@pytest.mark.parametrize(("input", "result"), [
    (None, "a.json"),
    ("a.json", "a.json"),
    ("ns.json", "ns.json"),
    ("x.json", "x.json")
])
def test_get_config_returns_filename(mocker, input, result):
    mock = mocker.MagicMock()
    mock.get_config_file = mocker.Mock()
    mock.get_config_file.return_value = get_config_file(input)
    mocker.patch.object(diglist3r, "get_config_file", mock.get_config_file)
    config_file = diglist3r.get_config_file()
    assert result == config_file

@pytest.mark.parametrize(("domain", "results"),[
    ("google.com", ["172.217.31.142"]),
    ("google.com", ["ns1.google.com.","ns2.google.com.", "ns3.google.com.", "ns4.google.com."]),
    ("172.217.31.142", ["nrt20s08-in-f14.1e100.net."]),
])
def test_serialize_to_json(domain, results):
    json_str = diglist3r.serialize_to_json(domain, results)
    json_dict = json.loads(json_str)
    assert domain == json_dict["domain"]
    assert results == json_dict["results"]

