import argparse
import asyncio
import logging
from pathlib import Path

from asyncio_taskpool.pool import TaskPool

from feedzgerald.config import read_config
from feedzgerald.feed import process_feed

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logging.getLogger("asyncio_taskpool").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate rss feed files by filtering remote rss feeds"
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        help="The path to the feedzgerald configuration file",
        required=True,
    )
    return parser.parse_args()


async def main(args: argparse.Namespace):
    config = read_config(filepath=args.config)
    pool = TaskPool()
    pool.map(process_feed, arg_iter=config.feeds, num_concurrent=config.parallelism)
    await pool.gather_and_close()


def run_main():
    args = parse_args()
    asyncio.run(main(args))


if __name__ == "__main__":
    run_main()
