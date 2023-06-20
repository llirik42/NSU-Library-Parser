from argparse import ArgumentParser
from typing import List

from book import Book
from book_parser import BookParser, NSULibBookParser
from downloader import Downloader, ProgressPDFDownloader

if __name__ == '__main__':
    args_parser: ArgumentParser = ArgumentParser(
        prog='NSU-Library-Parser',
        description='The program downloads all given books (page by page) from NSU e-library and converts them to pdf. '
                    'It stores downloaded books to directory "books. '
                    'Before downloading all books, program clears this directory (if the directory existed).',
    )

    args_parser.add_argument('urls', metavar='link', type=str, nargs='+', help='link to the book')

    urls: List[str] = args_parser.parse_args().urls
    parser: BookParser = NSULibBookParser()
    books: List[Book] = []

    print('Preparing books for downloading ...\n')
    for url in urls:
        book = parser.parse(url=url)
        if book is not None:
            print(f'Book "{book}" is prepared for downloading\n')
            books.append(book)

    downloader: Downloader = ProgressPDFDownloader()
    downloader.download(books=books)
