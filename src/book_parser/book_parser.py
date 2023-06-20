from abc import ABC, abstractmethod
from typing import Optional

from src.book import Book


class BookParser(ABC):
    @abstractmethod
    def parse(self, url: str) -> Optional[Book]:
        pass
