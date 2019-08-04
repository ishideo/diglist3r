#!/usr/bin/env python
# -*- coding: utf-8 -*-
import concurrent.futures
import functools
import json
import logging
import subprocess
from argparse import ArgumentParser
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import IO, Dict, Iterator, List, Optional, Sequence, Tuple


def dig(config: List[str], domain: str) -> str:
    command: List[str] = config + [domain]
    process: Tuple[bytes, bytes] = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).communicate()
    results: List[str] = process[0].decode("utf-8").strip("\n").split("\n")
    jsonline: str = serialize_to_json(domain, results)
    logging_output(jsonline)
    return jsonline


def serialize_to_json(domain: str, results: List[str]) -> str:
    results_dict: OrderedDict[str, Sequence[str]] = OrderedDict(
        [("domain", domain), ("results", results)]
    )
    jsonline: str = json.dumps(results_dict)
    return jsonline


def logging_output(result: str) -> None:
    formatter: str = "%(levelname)s: %(asctime)s : %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    logging.info("%s", result)


def get_lines(path: str) -> Iterator[str]:
    iterator: Iterator[str] = (line.strip("\n") for line in open(path))
    return iterator

def read_config() -> Optional[Dict[str]]:
    parser = ArgumentParser(description="")
    parser.add_argument("--file", help="read configuration file")
    parser.add_argument("-f", "--file")
    args = parser.parse_args()
    config_file = args.file
    config: Dict[str] = json.load(config_file)
    return config


def main() -> None:
    pool: concurrent.futures.process.ProcessPoolExecutor = ProcessPoolExecutor(
        max_workers=32
    )
    #config = read_config()
    dig_config: functools.partial[str] = partial(dig, ["dig", "@8.8.8.8", "a", "+short"])
    #print(config["input"])
    lines: Iterator[str] = get_lines("./input.txt")
    jsonlines: List[str] = list(pool.map(dig_config, lines))
    text: str = "\n".join(jsonlines)
    file: IO[str] = open("./a.txt", "w")
    file.write(text)
    file.close()


if __name__ == "__main__":
    main()
