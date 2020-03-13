#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import subprocess
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path
from typing import IO, Dict, Iterator, List, Optional, Sequence, Tuple

import click


def dig(config: List[str], domain: str) -> List[str]:
    command: List[str] = config + [domain]
    process: Tuple[bytes, bytes] = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ).communicate()
    results: List[str] = process[0].decode("utf-8").strip("\n").split("\n")
    return results


def dig_wrapper(config: List[str], domain: str) -> str:
    results: List[str] = dig(config, domain)
    jsonline: str = serialize_to_json(domain, results)
    return jsonline


def serialize_to_json(domain: str, results: List[str]) -> str:
    results_dict: OrderedDict[str, Sequence[str]] = OrderedDict(
        [("domain", domain), ("results", results)]
    )
    jsonline: str = json.dumps(results_dict)
    logging_output(jsonline)
    return jsonline


def logging_output(result: str) -> None:
    formatter: str = "%(levelname)s: %(asctime)s : %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    logging.info("%s", result)


def get_lines(path: Path) -> Iterator[str]:
    iterator: Iterator[str] = (line.strip("\n") for line in open(path))
    return iterator


def get_config_path(config: Optional[str]) -> Path:
    config_path: Path = Path("./config/" + "a.json")
    if config is not None:
        config_path = Path("./config/" + config)
    return config_path


def read_config(config: Optional[str]) -> Dict[str, str]:
    config_path: Path = get_config_path(config)
    f: IO[str] = open(config_path, "r")
    settings: Dict[str, str] = json.load(f)
    f.close()
    return settings


@click.command()
@click.option("-c", "--config", type=str)
def cli(config: Optional[str]) -> None:
    settings: Dict[str, str] = read_config(config)
    max_workers_value: int = int(settings["max_workers"])
    pool: ProcessPoolExecutor = ProcessPoolExecutor(max_workers=max_workers_value)
    input: Path = Path(settings["input"])
    output: Path = Path(settings["output"])
    command: str = settings["command"]
    dig_partial: partial[str] = partial(dig_wrapper, command)
    lines: Iterator[str] = get_lines(input)
    jsonlines: List[str] = list(pool.map(dig_partial, lines))
    text: str = "\n".join(jsonlines)
    f: IO[str] = open(output, "w")
    f.write(text)
    f.close()
    click.echo("Done!")


if __name__ == "__main__":
    cli()
