from shutil import rmtree
from os.path import isdir
from os import mkdir
from typing import Optional, List
from time import perf_counter
from math import floor

from fpdf import FPDF

from config import BOOKS_PATH
from book import Book


PDFBook = FPDF
IMAGES_EXTENSION = 'PNG'
A4_WIDTH_IN_MM = 210


class ProgressDisplay:
    __total_pages_count: int
    __start_time: float
    __current_page_index: int

    def __init__(self, total_pages_count: int) -> None:
        self.__total_pages_count = total_pages_count
        self.__start_time = perf_counter()
        self.__current_page_index = 0

    def increase_and_display(self) -> None:
        self.__current_page_index += 1

        current_percentage = self.__current_page_index / self.__total_pages_count

        eta = (perf_counter() - self.__start_time) * (1 / current_percentage - 1)
        hh_mm_ss_eta = self.__get_hh_mm_ss(round(eta))

        print(f'Прогресс = {floor(100 * current_percentage)}%   Оставшееся время = {hh_mm_ss_eta}')

        # print(f'\rПрогресс = {round(100 * current_percentage)}%   Оставшееся время = {hh_mm_ss_eta}', end='')

    @staticmethod
    def __get_hh_mm_ss(seconds: int) -> str:
        result = f'{seconds // 3600}:' * int(seconds >= 3600)

        m = seconds % 3600 // 60
        result += f'{m // 10}{m % 10}:'

        s = seconds % 60
        result += f'{s // 10}{s % 10}'

        return result


class Downloader:
    __progress_display: Optional[ProgressDisplay]

    def __init__(self):
        self.__make_directory_with_books()

        self.__progress_display = None

    def download(self, urls: List[str]) -> None:
        books = self.__prepare_books(urls=urls)

        total_pages_count = self.__calculate_total_pages_count(books=books)

        self.__progress_display = ProgressDisplay(total_pages_count=total_pages_count)

        self.__download_books(books=books)

    @staticmethod
    def __make_directory_with_books() -> None:
        if isdir(BOOKS_PATH):
            rmtree(BOOKS_PATH)

        mkdir(BOOKS_PATH)

    @staticmethod
    def __prepare_books(urls: List[str]) -> List[Book]:
        print('\rПодготовка к скачиванию', end='')

        books = []

        for current_url in urls:
            current_book = Book(url=current_url)

            books.append(current_book)

        return books

    def __download_books(self, books: List[Book]) -> None:
        print('\rСкачивание')

        for current_book in books:
            current_pdf_book = self.__convert_to_pdf(book=current_book)

            current_pdf_book.output(f'{BOOKS_PATH}/{current_book.title}.pdf')

    def __convert_to_pdf(self, book: Book) -> PDFBook:
        pdf_book = PDFBook(format='a4', orientation='portrait', unit='mm')

        for page_index in range(book.pages_count):
            pdf_book.add_page()

            pdf_book.image(book.get_link_to_page(page_index=page_index), x=0, y=0, w=A4_WIDTH_IN_MM)

            self.__progress_display.increase_and_display()

        return pdf_book

    @staticmethod
    def __calculate_total_pages_count(books: List[Book]) -> int:
        return sum([book.pages_count for book in books])
