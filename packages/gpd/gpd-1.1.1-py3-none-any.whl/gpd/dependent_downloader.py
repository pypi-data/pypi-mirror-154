import time
from typing import List, Set

import requests
from diskcache import Cache
from loguru import logger
from tqdm import tqdm

from gpd.models.dependent import Dependent
from gpd.parsers.table_page_parser import TablePageParser


class DependentDownloader:
    owner: str
    project: str
    max_page: int
    max_attempts: int

    def __init__(
        self,
        owner: str,
        project: str,
        max_page: int,
        cache: Cache,
        max_attempts: int = 3,
    ):
        self.owner = owner
        self.project = project
        self.max_page = max_page
        self.cache = cache
        self.max_attempts = max_attempts

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_dependents(self) -> Set[Dependent]:
        dependents: List[Dependent] = []
        page_count: int = min(self.get_estimate_of_dependent_pages(), self.max_page)
        next_url: str = self.get_start_url()
        current_url: str = next_url
        for i in tqdm(range(page_count)):
            for attempt in range(self.max_attempts):
                try:
                    html = self.get_dependents_html_from_url(current_url)

                    parser = TablePageParser(html)
                    dependents += self.get_dependents_from_html(html)
                    next_url = parser.get_next_page_url()
                except:
                    self.cache.delete(current_url)
                    logger.exception(
                        "attempt={attempt}, start_url={start_url}, current_url={current_url}, next_url={next_url}, page_number={page_number}",
                        attempt=attempt,
                        start_url=self.get_start_url(),
                        current_url=current_url,
                        next_url=next_url,
                        page_number=i,
                    )
                    time.sleep(30)
                if next_url:
                    current_url = next_url
                    break
        return set(dependents)

    def get_dependents_from_html(self, html: str) -> List[Dependent]:
        try:
            parser = TablePageParser(html)
            return parser.get_dependents()
        except:
            pass
        return []

    def get_estimate_of_dependent_pages(self) -> int:
        start_url = self.get_start_url()
        html = self.get_dependents_html_from_url(start_url)
        parser = TablePageParser(html)
        dependents_estimate = parser.get_dependents_estimate()
        return max(int(dependents_estimate * 1.1 / 30), 1)

    def get_dependents_html_from_url(self, url: str) -> str:
        if url in self.cache:
            html = self.cache.get(url)
        else:
            response = requests.get(url)
            html = response.text
            self.cache.set(url, html)
            time.sleep(1.5)  # throttling new requests
        return html

    def get_start_url(self) -> str:
        return "https://github.com/{}/{}/network/dependents".format(
            self.owner, self.project
        )

    def clear_cache(self) -> None:
        self.cache.clear()

    def close(self) -> None:
        self.cache.close()
