import aiohttp
import async_timeout
import feedparser

from typing import List, Optional
from .release import Release

class SubsPlease:
    """
    Represents a SubsPlease client.

    Parameters
    -------------
    timeout: Optional[:class:`int`]
        To terminate the request after a while if no response is received.
        The default timeout is ``20``.
    """
    def __init__(self, timeout: Optional[int] = 20) -> None:
        self.timeout = timeout 

        self._torrent_url = "https://subsplease.org/rss/?t"
        self._magnet_url = "https://subsplease.org/rss/"
    
    async def _get(self, rss_url: str):
        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(self.timeout):
                async with session.get(rss_url) as response:
                    return await response.text()
    
    async def get_latest_torrent(self) -> List[Release]:
        feed = await self._get(self._torrent_url)

        rss = feedparser.parse(feed)
        entries = rss["entries"]
        releases: List[Release] = []

        for entry in entries:
            releases.append(
                Release(
                    title=entry["title"],
                    link=entry["link"],
                    guid=entry["id"],
                    tags=entry["tags"],
                    size=entry["subsplease_size"],
                    release_date=entry["published"],
                    raw=entry,
                )
            )
        return releases

    async def get_latest_magnet(self) -> List[Release]:
        feed = await self._get(self._magnet_url)

        rss = feedparser.parse(feed)
        entries = rss["entries"]
        releases: List[Release] = []

        for entry in entries:
            releases.append(
                Release(
                    title=entry["title"],
                    link=entry["link"],
                    guid=entry["id"],
                    tags=entry["tags"],
                    size=entry["subsplease_size"],
                    release_date=entry["published"],
                    raw=entry,
                )
            )
        return releases