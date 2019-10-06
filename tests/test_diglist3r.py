import json
from typing import Any, Dict, List, Tuple

import pytest

import diglist3r


@pytest.mark.parametrize(
    ("filename", "result"),
    [
        (None, "./config/a.json"),
        ("a.json", "./config/a.json"),
        ("ns.json", "./config/ns.json"),
        ("x.json", "./config/x.json"),
    ],
)
def test_get_config_path(filename: str, result: str) -> None:
    config_path: str = diglist3r.get_config_path(filename)
    assert result == config_path


@pytest.mark.parametrize(
    ("domain", "results"),
    [
        ("google.com", ["172.217.31.142"]),
        (
            "google.com",
            [
                "ns1.google.com.",
                "ns2.google.com.",
                "ns3.google.com.",
                "ns4.google.com.",
            ],
        ),
        ("172.217.31.142", ["nrt20s08-in-f14.1e100.net."]),
    ],
)
def test_serialize_to_json(domain: str, results: List[str]) -> None:
    json_str: str = diglist3r.serialize_to_json(domain, results)
    json_dict: Dict[str, str] = json.loads(json_str)
    assert json_dict["domain"] == domain
    assert json_dict["results"] == results
    assert len(json_dict.keys()) == 2


@pytest.mark.parametrize(
    ("config", "domain"),
    [
        (["dig", "@8.8.8.8", "a", "+short"], "apnic.net"),
        (["dig", "@8.8.8.8", "a", "+short"], "google.com"),
        (["dig", "@8.8.8.8", "ns", "+short"], "apnic.net"),
        (["dig", "@8.8.8.8", "x", "+short"], "google.com"),
    ],
)
def test_dig_when_domain_is_lookedup(config: List[str], domain: str) -> None:
    results: List[str] = diglist3r.dig(config, domain)
    assert isinstance(results, list)


@pytest.mark.parametrize(
    ("config", "domain"),
    [
        (["dig", "@8.8.8.8", "a", "+short"], "alkjdjf"),
        (["dig", "@8.8.8.8", "a", "+short"], "jlkajdlkfj.com"),
        (["dig", "@8.8.8.8", "ns", "+short"], "lkdffkj"),
        (["dig", "@8.8.8.8", "x", "+short"], "jlkajdlkfj.com"),
    ],
)
def test_dig_when_domain_is_not_lookedup(config: List[str], domain: str) -> None:
    results: List[str] = diglist3r.dig(config, domain)
    assert results[0] == ""


@pytest.mark.parametrize(
    ("config", "domain", "results"),
    [
        (["dig", "@8.8.8.8", "a", "+short"], "apnic.net", ["203.119.101.61"]),
        (["dig", "@8.8.8.8", "a", "+short"], "google.com", ["172.217.27.78"]),
        (["dig", "@8.8.8.8", "ns", "+short"], "apnic.net", ["203.119.101.61"]),
        (["dig", "@8.8.8.8", "x", "+short"], "google.com", ["172.217.27.78"]),
        (["dig", "@8.8.8.8", "a", "+short"], "alkjdjf", [""]),
        (["dig", "@8.8.8.8", "a", "+short"], "jlkajdlkfj.com", [""]),
        (["dig", "@8.8.8.8", "ns", "+short"], "lkdffkj", [""]),
        (["dig", "@8.8.8.8", "x", "+short"], "jlkajdlkfj.com", [""]),
    ],
)
def test_dig_wrapper_when_domain_is_lookedup(
    config: List[str], domain: str, results: List[str], mocker: Any
) -> None:
    mocker.patch.object(diglist3r, "dig", return_value=results)
    jsonline: str = diglist3r.dig_wrapper(config, domain)
    jsonline_dict: Dict[str, str] = json.loads(jsonline)
    assert jsonline_dict["domain"] == domain
    assert jsonline_dict["results"] == results
    assert len(jsonline_dict.keys()) == 2


@pytest.mark.parametrize(
    ("filename", "result"),
    [
        (
            "a.json",
            {
                "input": "input.txt",
                "output": "a.txt",
                "command": ["dig", "@8.8.8.8", "a", "+short"],
                "max_workers": 32,
            },
        ),
        (
            "ns.json",
            {
                "input": "input.txt",
                "output": "ns.txt",
                "command": ["dig", "@8.8.8.8", "ns", "+short"],
                "max_workers": 32,
            },
        ),
        (
            "x.json",
            {
                "input": "input.txt",
                "output": "x.txt",
                "command": ["dig", "@8.8.8.8", "+short", "-x"],
                "max_workers": 32,
            },
        ),
    ],
)
def test_read_config(filename: str, result: Dict[str, Any], mocker: Any) -> None:
    config_path: str = "./tests/config/" + filename
    mocker.patch.object(diglist3r, "get_config_path", return_value=config_path)
    config: Dict[str, Any] = diglist3r.read_config(filename)
    assert config == result
