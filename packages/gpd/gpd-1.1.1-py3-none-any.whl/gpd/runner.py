"""
    gpd.py
    ------------------

    Runs the project.

    :copyright: 2019 MislavJaksic
    :license: MIT License
"""
import argparse
import pickle
import socket
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Set

from diskcache import Cache
from loguru import logger

from gpd.cache.dependent_cache import DependentCache
from gpd.dependent_downloader import DependentDownloader
from gpd.dependents_stats import DependentsStats
from gpd.models.dependent import Dependent
from gpd.settings import cache_path


def main() -> int:
    """main() will be run if you run this script directly"""
    args = get_cli_arguments()

    setup_loguru()

    dependents = get_dependents(args["owner"], args["name"], args["max_page"])
    stats = DependentsStats(dependents)
    print(stats.get_top_stars())

    return 0


def get_dependents(owner: str, project: str, max_page: int) -> Set[Dependent]:
    cache = Cache(Path(cache_path).__str__())
    with DependentCache(cache) as dependent_cache:
        key = dependent_cache.construct_key(owner, project, max_page)
        dependents = dependent_cache.get_dependents(key)
        if not dependents:
            downloader = DependentDownloader(owner, project, max_page, cache)
            dependents = downloader.get_dependents()
        if dependents:
            dependent_cache.set_dependents(key, dependents)

    return dependents


def get_cli_arguments() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(description="", epilog="")

    parser.add_argument(
        "-o",
        "--owner",
        required=True,
        help="Project owner. For example 'github' in 'https://github.com/github/advisory-database'.",
    )
    parser.add_argument(
        "-n",
        "--name",
        required=True,
        help="Project name. For example 'advisory-database' in 'https://github.com/github/advisory-database'.",
    )
    parser.add_argument(
        "-m",
        "--max_page",
        type=int,
        nargs="?",
        const=sys.maxsize,
        default=sys.maxsize,
        help="How many pages of dependents do you want to parse before finishing. Default is sys.maxsize, infinity.",
    )

    return vars(parser.parse_args())


def setup_loguru() -> None:
    host = socket.gethostname()
    ip = socket.gethostbyname(host)

    config = {
        "handlers": [
            {
                "sink": sys.stderr,
                "diagnose": False,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{extra[host]}</cyan>:<cyan>{extra[ip]}</cyan> | <cyan>{process}</cyan>:<cyan>{thread}</cyan> | <cyan>{module}</cyan>:<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
            },
            {"sink": "file.log", "retention": "7 days", "serialize": True},
        ],
        "extra": {"host": host, "ip": ip},
    }
    logger.configure(**config)  # type: ignore


def run() -> None:
    """Entry point for the runnable script."""
    sys.exit(main())


if __name__ == "__main__":
    """main calls run()."""
    run()
