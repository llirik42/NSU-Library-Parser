from typing import List


class Book:
    __title: str
    __pages_count: int
    __links_to_pages: List[str]

    def __init__(self, title: str, links_to_pages: List[str]):
        self.__title = title
        self.__pages_count = len(links_to_pages)
        self.__links_to_pages = links_to_pages

    @property
    def title(self) -> str:
        return self.__title

    @property
    def pages_count(self) -> int:
        return self.__pages_count

    def get_link_to_page(self, page_index: int) -> str:
        return self.__links_to_pages[page_index]

    def __str__(self) -> str:
        return f'{self.__title}'
