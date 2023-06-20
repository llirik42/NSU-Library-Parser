from abc import ABC, abstractmethod
from typing import List

from src.book import Book


class Downloader(ABC):
    @abstractmethod
    def download(self, books: List[Book], path='books/') -> None:
        pass
