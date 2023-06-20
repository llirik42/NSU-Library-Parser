from typing import List
from os import mkdir
from os.path import isdir
from shutil import rmtree

import fpdf

from .downloader import Downloader
from src.book import Book

A4_WIDTH_IN_MM = 210


class PDFDownloader(Downloader):
    def download(self, books: List[Book], books_directory: str = 'books/') -> None:
        if len(books) == 0:
            return

        self._make_directory_with_books(books_directory)

        for book in books:
            self._download_book(book, books_directory)

    def _make_directory_with_books(self, path: str) -> None:
        if isdir(path):
            rmtree(path)

        mkdir(path)

    def _download_book(self, book: Book, books_directory: str) -> None:
        pfd_book: fpdf.FPDF = PDFDownloader._convert_to_pdf(self, book)
        pfd_book.output(f'{books_directory}/{book.title}.pdf')

    def _convert_to_pdf(self, book: Book) -> fpdf.FPDF:
        pdf_book: fpdf.FPDF = fpdf.FPDF(format='a4', orientation='portrait', unit='mm')

        for page_index in range(book.pages_count):
            self._download_and_add_page(pdf_book, book, page_index)

        return pdf_book

    def _download_and_add_page(self, pdf_book: fpdf.FPDF, book: Book, page_index: int) -> None:
        pdf_book.add_page()

        pdf_book.image(
            name=book.get_link_to_page(page_index=page_index),
            x=0,
            y=0,
            w=A4_WIDTH_IN_MM,
        )
