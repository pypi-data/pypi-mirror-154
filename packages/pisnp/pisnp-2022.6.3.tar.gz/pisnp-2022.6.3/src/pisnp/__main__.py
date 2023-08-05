# coding=utf-8
#
# __main__.py in pisnp
#
# created by 谢方圆 (XIE Fangyuan) on 2022-06-04
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Entry point when running this package as a module from the terminal.


from typing import NoReturn

from pisnp import __version__


def main() -> NoReturn:
    print(f'pisnp {__version__}\nP is NP? (Polynomial is Non-polynomial?)')


if __name__ == '__main__':
    main()
