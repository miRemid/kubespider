# -*- coding: utf-8 -*-
import logging
from lxml import html
from api import types
from source_provider import provider

from utils import helper
from utils.config_reader import AbsConfigReader

class DoubanSourceProvider(provider.SourceProvider):
    """
    Description: general rss source provider
    """
    def __init__(self, name: str, config_reader: AbsConfigReader) -> None:
        """
        Description: init class of DoubanSourceProvider
                    provider_type: douban_source_provider
                    sub_link: the URL of the douban book(片单)
                    file_type: this type is resource type
                    provider_listen_type: disposable or period
                    jackett_endpoint: the endpoint of the jackett server

        Args:
            rss_config: config member of rss config, file is ./config/general_rss.json
        """
        super().__init__(config_reader)
        self.webhook_enable = False
        self.sub_link = "" # 片单地址
        self.jackett_endpoint = "" # jackett地址
        self.file_type = types.FILE_TYPE_COMMON
        self.link_type = types.LINK_TYPE_TORRENT
        self.provider_listen_type = types.SOURCE_PROVIDER_PERIOD_TYPE
        self.provider_type = "douban_source_provider"
        self.provider_name = name
        self.load_config()

    def get_provider_name(self) -> str:
        return self.provider_name

    def get_provider_type(self) -> str:
        return self.provider_type

    def get_link_type(self) -> str:
        return self.link_type

    def get_download_param(self) -> None:
        return self.config_reader.read().get('download_param')

    def get_download_provider_type(self) -> None:
        pass

    def get_prefer_download_provider(self):
        downloader_names = self.config_reader.read().get('downloader', None)
        if downloader_names is None:
            return None
        if isinstance(downloader_names, list):
            return downloader_names
        return [downloader_names]

    def get_provider_listen_type(self) -> str:
        return self.provider_listen_type

    def provider_enabled(self) -> bool:
        return self.config_reader.read().get('enable', True)

    def is_webhook_enable(self) -> bool:
        return self.webhook_enable

    def should_handle(self, data_source_url: str) -> None:
        pass

    def get_links(self, data_source_url: str) -> list:
        """
        Description: get rss resource link for download
        Args:
            dataSourceUrl:
        Returns:
        """
        links = []
        try:
            controller = helper.get_request_controller()
            resp = controller.open(self.sub_link, timeout=30).read()
        except Exception as err:
            logging.warning('DoubanSourceProvider get links error:%s', err)
            return links
        dom = html.fromstring(resp.decode('utf-8', 'ignore'))
        titles = dom.xpath("//*[@class='bd doulist-subject']/div[@class='title']")
        for title in titles:
            full_title = title.text_content().strip()
            chinese_title, other_title = full_title.split(' ')
        return links

    def load_config(self) -> None:
        cfg = self.config_reader.read()
        self.sub_link = cfg.get("sub_link", "")
        self.jackett_endpoint = cfg.get("jackett_endpoint", "")
