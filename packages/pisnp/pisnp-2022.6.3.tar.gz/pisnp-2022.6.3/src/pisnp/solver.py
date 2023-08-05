# coding=utf-8
#
# solver.py in pisnp
#
# created by 谢方圆 (XIE Fangyuan) on 2022-06-05
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Abstract base problem solver.


from abc import ABCMeta, abstractmethod
from typing import Generator, final

from pisnp.utility import Timer


class Solver(metaclass=ABCMeta):
    @abstractmethod
    def solve(self) -> Generator:
        """Override this function to solve a specific problem.

        Returns:
            The solution.
        """
        pass

    @final
    @Timer.time
    def timed_solve(self) -> list:
        return list(self.solve())

    def display(self, *args, **kwargs) -> None:
        """Display the solution.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        print(f'Override Solver.display() to display the solution.')
