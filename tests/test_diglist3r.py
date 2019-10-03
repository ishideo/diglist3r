import json
import pytest

import diglist3r


@pytest.mark.parametrize(
    ("filename", "result"),
    [
        (None, "./a.json"),
        ("a.json", "./a.json"),
        ("ns.json", "./ns.json"),
        ("x.json", "./x.json"),
    ],
)
def test_get_config_path(filename, result):
    config_path = diglist3r.get_config_path(filename)
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
def test_serialize_to_json(domain, results):
    json_str = diglist3r.serialize_to_json(domain, results)
    json_dict = json.loads(json_str)
    assert domain == json_dict["domain"]
    assert results == json_dict["results"]


@pytest.mark.parametrize(
    ("config", "domain"),
    [
        (["dig", "@8.8.8.8", "a", "+short"], "apnic.net"),
        (["dig", "@8.8.8.8", "a", "+short"], "google.com"),
        (["dig", "@8.8.8.8", "ns", "+short"], "apnic.net"),
        (["dig", "@8.8.8.8", "x", "+short"], "google.com"),
    ],
)
def test_dig_when_domain_is_lookedup(config, domain):
    results = diglist3r.dig(config, domain)
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
def test_dig_when_domain_is_not_lookedup(config, domain):
    results = diglist3r.dig(config, domain)
    assert results[0] == ""
