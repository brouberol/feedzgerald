import logging

import feedparser
import httpx
from feedgen.feed import FeedGenerator

from feedzgerald.config import FeedConfiguration

log = logging.getLogger(__name__)


class FeedProcessor:
    def __init__(self, feed_config: FeedConfiguration):
        self.feed_config = feed_config

    async def fetch(self) -> httpx.Response:
        async with httpx.AsyncClient() as http_client:
            return await http_client.get(self.feed_config.url)

    def parse(self, response: httpx.Response) -> feedparser.FeedParserDict:
        return feedparser.parse(response.text)

    def filter(
        self, feed: feedparser.FeedParserDict
    ) -> list[feedparser.FeedParserDict]:
        filtered_entries = []
        for feed_entry in feed.entries:
            keep = True
            if title_filter := self.feed_config.title_filter:
                if title_filter not in feed_entry.title:
                    keep = False
            if negative_title_filter := self.feed_config.negative_description_filter:
                if negative_title_filter in feed_entry.title:
                    keep = False
            if description_filter := self.feed_config.description_filter:
                if description_filter not in feed_entry.description:
                    keep = False
            if (
                negative_description_filter
                := self.feed_config.negative_description_filter
            ):
                if negative_description_filter in feed_entry.description:
                    keep = False
            if negative_url_filter := self.feed_config.negative_url_filter:
                if negative_url_filter in feed_entry.url:
                    keep = False
            if keep:
                log.info(f"[{self.feed_config.name}] Keeping feed {feed_entry.title}")
                filtered_entries.append(feed_entry)
        return filtered_entries

    def generate(self, entries: list[feedparser.FeedParserDict]):
        feed = FeedGenerator()
        feed.id(self.feed_config.url)
        feed.link(href=self.feed_config.url)
        feed.description(f"Filtered feed from {self.feed_config.url}")
        feed.title(self.feed_config.name)
        for entry in entries:
            feed_entry = feed.add_entry()
            feed_entry.id(entry.get("id"))
            feed_entry.title(entry.get("title"))
            feed_entry.link(href=entry.get("link"))
            feed_entry.description(entry.get("description"))
            feed_entry.pubDate(entry.get("published"))
        feed.rss_file(self.feed_config.output_folder / self.feed_config.filename)

    async def run(self):
        log.info(f"Processing feed {self.feed_config.name}")
        response = await self.fetch()
        feed = self.parse(response)
        entries = self.filter(feed)
        filtered_feed = self.generate(entries)
        return filtered_feed


async def process_feed(feed_config: FeedConfiguration):
    processor = FeedProcessor(feed_config=feed_config)
    await processor.run()
