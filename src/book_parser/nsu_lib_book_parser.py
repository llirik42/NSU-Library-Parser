from typing import Tuple, Optional, Union, List

import requests
import json

from .book_parser import BookParser
from src.book import Book


BASE_LINK_TO_PAGES: str = 'https://e-lib.nsu.ru/reader/service/SecureViewer/Page'
BASE_LINK_TO_BOOK_INFO: str = 'https://e-lib.nsu.ru/reader/service/SecureViewer/BookInfo'
BASE_LINK_TO_PAGES_PARAMETERS: str = 'https://e-lib.nsu.ru/reader/service/SecureViewer/PagesParameters'


class NSULibBookParser(BookParser):
    def parse(self, url: str) -> Optional[Book]:
        try:
            ids: Tuple[str, str] = self.__parse_ids(url=url)
            title: str = self.__parse_title(ids=ids)
            pages_count: int = self.__parse_pages_count(ids=ids)
            link_to_pages: str = self.__parse_link_to_pages(ids=ids)
            links_to_pages: List[str] = [f'{link_to_pages}/{page_index + 1}' for page_index in range(pages_count)]
            return Book(title=title, links_to_pages=links_to_pages)
        except RuntimeWarning:
            print(f'Invalid url: {url}\n')
            return None

    def __parse_title(self, ids: Tuple[str, str]) -> Optional[str]:
        return self.__parse_json_key(
            url=self.__get_url_with_ids(BASE_LINK_TO_BOOK_INFO, ids=ids),
            key='title'
        )

    def __parse_link_to_pages(self, ids: Tuple[str, str]) -> str:
        return self.__get_url_with_ids(url=BASE_LINK_TO_PAGES, ids=ids)

    def __parse_pages_count(self, ids: Tuple[str, str]) -> int:
        return self.__parse_json_key(
            url=self.__get_url_with_ids(url=BASE_LINK_TO_PAGES_PARAMETERS, ids=ids),
            key='pagesCount'
        )

    @staticmethod
    def __parse_ids(url: str) -> Tuple[str, str]:
        i: int = url.find('=') + 1
        j: int = url.find('/', i)
        return url[i:j], url[j + 1:]

    @staticmethod
    def __get_url_with_ids(url: str, ids: Tuple[str, str]) -> str:
        return f'{url}/{ids[0]}/{ids[1]}'

    @staticmethod
    def __parse_json_key(url: str, key: str) -> Optional[Union[str, int]]:
        response: requests.Response = requests.get(url=url)

        if response.status_code != 200:
            raise RuntimeWarning()

        content: str = response.content.decode()
        json_data = json.loads(content)
        return json_data[key]
