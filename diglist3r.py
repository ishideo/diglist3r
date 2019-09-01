#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import subprocess
from argparse import ArgumentParser, Namespace
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import IO, Dict, Iterator, List, Sequence, Tuple


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


def get_config_file() -> str:
    config_file: str = "a.json"
    parser: ArgumentParser = ArgumentParser(description="")
    parser.add_argument("-f", "--file", help="configuration filename")
    args: Namespace = parser.parse_args()
    if args.file is not None:
        config_file = args.file
    return config_file


def read_config() -> Dict[str, str]:
    config_file: str = get_config_file()
    file: IO[str] = open("./" + config_file, "r")
    config: Dict[str, str] = json.load(file)
    file.close()
    return config


def main() -> None:
    pool: ProcessPoolExecutor = ProcessPoolExecutor(
        max_workers=32
    )
    config: Dict[str, str] = read_config()
    input: str = config["input"]
    output: str = config["output"]
    command: str = config["command"]
    dig_partial: partial[str] = partial(dig, command)
    lines: Iterator[str] = get_lines(input)
    jsonlines: List[str] = list(pool.map(dig_partial, lines))
    text: str = "\n".join(jsonlines)
    file: IO[str] = open(output, "w")
    file.write(text)
    file.close()


if __name__ == "__main__":
    main()
