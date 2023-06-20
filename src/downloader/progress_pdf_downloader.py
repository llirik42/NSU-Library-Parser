from typing import List

import fpdf

from .pdf_downloader import PDFDownloader
from src.book import Book


class ProgressPDFDownloader(PDFDownloader):
    def download(self, books: List[Book], books_directory: str = 'books/') -> None:
        super().download(books, books_directory)

    def _make_directory_with_books(self, path: str) -> None:
        print(f'Making directory for books - "{path}"\n')
        super()._make_directory_with_books(path)

    def _download_book(self, book: Book, books_directory: str) -> None:
        super()._download_book(book, books_directory)
        print(f'\rBook "{book}" is downloaded!\n')

    def _convert_to_pdf(self, book: Book) -> fpdf.FPDF:
        return super()._convert_to_pdf(book)

    def _download_and_add_page(self, pdf_book: fpdf.FPDF, book: Book, page_index: int) -> None:
        print(f'\rDownloading page {page_index + 1}/{book.pages_count} of book "{book}"', end='')
        super()._download_and_add_page(pdf_book, book, page_index)
