from typing import Tuple, Union, Optional
from json import loads

from requests import get

from config import BASE_LINK_TO_BOOK_INFO, BASE_LINK_TO_PAGES, BASE_LINK_TO_PAGES_PARAMETERS, TIMEOUT_CONNECT


class Book:
    __pages_count: int
    __title: Optional[str]
    __link_to_pages: str

    def __init__(self, url: str):
        ids = self.__get_ids(url=url)

        self.__pages_count = self.__extract_pages_count(ids=ids)

        self.__title = self.__extract_title(ids=ids)

        self.__link_to_pages = self.__extract_link_to_pages(ids=ids)

    def get_link_to_page(self, page_index: int) -> str:
        return f'{self.__link_to_pages}/{page_index + 1}'

    @property
    def title(self) -> str:
        return self.__title

    @property
    def pages_count(self) -> int:
        return self.__pages_count

    def __extract_title(self, ids: Tuple[str, str]) -> Optional[str]:
        return self.__get_json_key(
            url=self.__get_url_with_ids(BASE_LINK_TO_BOOK_INFO, ids=ids),
            key='title'
        )

    def __extract_link_to_pages(self, ids: Tuple[str, str]) -> str:
        return self.__get_url_with_ids(url=BASE_LINK_TO_PAGES, ids=ids)

    def __extract_pages_count(self, ids: Tuple[str, str]) -> int:
        return self.__get_json_key(
            url=self.__get_url_with_ids(url=BASE_LINK_TO_PAGES_PARAMETERS, ids=ids),
            key='pagesCount'
        )

    @staticmethod
    def __get_ids(url: str) -> Tuple[str, str]:
        indexes = [-1, -1]

        indexes[0] = url.find('=') + 1
        indexes[1] = url.find('/', indexes[0])

        return url[indexes[0]:indexes[1]], url[indexes[1] + 1:]

    @staticmethod
    def __get_url_with_ids(url: str, ids: Tuple[str, str]) -> str:
        return f'{url}/{ids[0]}/{ids[1]}'

    @staticmethod
    def __get_json_key(url: str, key: str) -> Optional[Union[str, int]]:
        response = get(url=url, verify=False, timeout=(TIMEOUT_CONNECT, None))

        content = response.content.decode()

        json_data = loads(content)

        return json_data[key]


__all__ = ['Book']
