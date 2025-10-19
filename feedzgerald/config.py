import os
from dataclasses import dataclass
from pathlib import Path

import tomllib


@dataclass
class FeedConfiguration:
    name: str
    filename: str
    url: str
    title_filter: str | None
    negative_url_filter: str | None
    negative_title_filter: str | None
    description_filter: str | None
    negative_description_filter: str | None
    output_folder: Path


@dataclass
class Config:
    parallelism: int
    feeds: list[FeedConfiguration]


def read_config(filepath: Path) -> Config:
    config = tomllib.load(open(filepath, "rb"))
    core_config = config.get("core", {})
    if output_folder_str := core_config.get("output_folder"):
        output_folder = Path(output_folder_str)
    else:
        output_folder = Path(os.getcwd())
    feed_configs = [
        FeedConfiguration(
            name=conf["name"],
            filename=f"{feed_name}.rss",
            url=conf["url"],
            title_filter=conf.get("title_filter"),
            negative_title_filter=conf.get("negative_title_filter"),
            description_filter=conf.get("description_filter"),
            negative_description_filter=conf.get("negative_description_filter"),
            negative_url_filter=conf.get("negative_url_filter"),
            output_folder=output_folder,
        )
        for feed_name, conf in config["feeds"].items()
    ]
    parallelism = min(len(feed_configs), core_config.get("parallelism", 5))
    return Config(parallelism=parallelism, feeds=feed_configs)
