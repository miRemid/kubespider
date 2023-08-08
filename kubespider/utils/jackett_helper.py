from __future__ import annotations

import json

from typing import List, Optional
from urllib import request, parse
from dataclasses import dataclass
# from utils.helper import get_request_controller
from dacite import from_dict, config
import enum

SEARCH_API = 'http://{}/api/v2.0/indexers/{}/results?apikey={}&'

@dataclass
class JackettResutItem():
    FirstSeen: Optional[str] = None
    Tracker: Optional[str] = None
    TrackerId: Optional[str] = None
    TrackerType: Optional[str] = None
    CategoryDesc: Optional[str] = None
    BlackholeLink: Optional[str] = None
    Title: Optional[str] = None
    Guid: Optional[str] = None
    Link: Optional[str] = None
    Details: Optional[str] = None
    PublishDate: Optional[str] = None
    Category: Optional[List[int]] = None
    Size: Optional[int] = None
    Files: Optional[int] = None
    Grabs: Optional[int] = None
    Description: Optional[str] = None
    RageID: Optional[str] = None
    TVDBId: Optional[str] = None
    Imdb: Optional[str] = None
    TMDb: Optional[str] = None
    TVMazeId: Optional[str] = None
    TraktId: Optional[str] = None
    DoubanId: Optional[str] = None
    Genres: Optional[List[str]] = None
    Languages: Optional[List[str]] = None
    Subs: Optional[List[str]] = None
    Year: Optional[int] = None
    Author: Optional[str] = None
    BookTitle: Optional[str] = None
    Publisher: Optional[str] = None
    Artist: Optional[str] = None
    Album: Optional[str] = None
    Label: Optional[List[str]] = None
    Track: Optional[str] = None
    Seeders: Optional[int] = None
    Peers: Optional[int] = None
    Poster: Optional[str] = None
    InfoHash: Optional[str] = None
    MagnetUri: Optional[str] = None
    MinimumRatio: Optional[float] = None
    MinimumSeedTime: Optional[str] = None
    DownloadVolumeFactor: Optional[float] = None
    UploadVolumeFactor: Optional[float] = None
    Gain: Optional[float] = None

@dataclass
class JackettIndexerItem():
    ID: Optional[str] = None
    Name: Optional[str] = None
    Results: Optional[int] = None
    Status: Optional[int] = None
    Error: Optional[str] = None

@dataclass
class JackettSearchResults():

    Results: List[JackettResutItem]
    Indexers: List[JackettIndexerItem]

    def get_index_items(self, name: List[str]=[], id: List[str]=[]) -> JackettSearchResults:
        """
        name: Tracker name
        id: Tracker id 
        """
        byid = False
        if len(name) != 0 and len(id) != 0:
            byid = True
        elif len(name) != 0 and len(id) == 0:
            byid = False
        elif len(name) == 0 and len(id) != 0:
            byid = True
        else:
            raise ValueError('must provide indexer name or id')

        if byid:
            indexers = [x for x in self.Indexers if x.ID in id]
        else:
            indexers  = [x for x in self.Indexers if x.Name in name]

        results = []
        for item in self.Results:
            if byid and item.TrackerId in id:
                results.append(item)
            elif not byid and item.Tracker in name:
                results.append(item)
        return JackettSearchResults(Results=results, Indexers=indexers)
    
    def sort_by_size(self, reverse=True) -> JackettSearchResults:
        """
        sort result by file size, big to small
        """
        self.Results.sort(key=lambda x: x.Size, reverse=reverse)
        return self
    
    def keywords(self, keywords: List[str] = []) -> JackettSearchResults:
        """
        keywords: include some contents like 1080P or HD, BD ... 
        """
        pass

class JackettHelper():

    def __init__(self, endpoint: str = '', apikey: str = '') -> None:
        self.endpoint = endpoint
        self.apikey = apikey
        self.client = request.build_opener()
        agent_header = ("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE")
        self.client.addheaders.append(agent_header)
    
    def search(self, filter: str = '', query: str = '', category: list = [], tracker: list = [])->JackettSearchResults:
        query_uri = parse.urlencode({
            'query': query,
            'Category': category,
            'Tracker': tracker
        })
        filter = 'all' if filter == '' else filter
        full_url = SEARCH_API.format(self.endpoint, filter, self.apikey) + query_uri
        resp = self.client.open(full_url).read().decode('utf8')
        data = json.loads(resp)
        result = from_dict(data_class=JackettSearchResults, data=data, config=config.Config(strict=True))
        return result


if __name__ == '__main__':

    jackett = JackettHelper('127.0.0.1:9117', 'ej2ky6s33m2uhbzj5sktqyorl9cx4wl3')
    result = jackett.search(query='Hello World').sort_by_size(reverse=True)
    for r in result.get_index_items(name=result.Indexers[0].Name).Results:
        print(r.Title, r.Size)