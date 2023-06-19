from urllib3 import disable_warnings
from args_parsing import check_args, get_args
from downloader import Downloader


def print_error(arg_index: int) -> None:
    digit = arg_index % 10

    s = 'ый'

    if digit in [2, 6, 7, 8]:
        s = 'ой'
    if digit == 3:
        s = 'ий'

    print(f'Некорректный {arg_index}-{s} аргумент')


if __name__ == '__main__':
    disable_warnings()

    incorrect_arg_index = check_args()

    if incorrect_arg_index:
        print_error(arg_index=incorrect_arg_index)
        exit(0)

    downloader = Downloader()

    downloader.download(urls=get_args())
