from argparse import ArgumentParser
from re import fullmatch
from typing import List

parser = ArgumentParser()
parser.add_argument('urls', type=str, nargs='+')
args = parser.parse_args().urls


def is_valid_url(url: str) -> bool:
    pattern = r'(https://|http://)?e-lib.nsu.ru/reader/bookView.html\?params=\w{18}/\w{11,12}'

    return fullmatch(pattern=pattern, string=url) is not None


def check_args() -> int:
    for index, url in enumerate(args):
        if not is_valid_url(url=url):
            return index + 1

    return 0


def get_args() -> List[str]:
    return args
