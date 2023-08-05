# coding=utf-8
#
# sudoku_solver.py in pisnp/sudoku
#
# created by 谢方圆 (XIE Fangyuan) on 2022-06-08
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Solver for sudoku problem.


import re
from abc import ABCMeta
from string import ascii_lowercase, ascii_uppercase, digits
from typing import Generator, Sequence

from sty import fg

from pisnp.exact_cover import MyExactCoverSolver, XExactCoverSolver
from pisnp.solver import Solver


class SudokuSolver(Solver, metaclass=ABCMeta):
    def __init__(self, board: Sequence[Sequence[int]]):
        self.n = len(board)
        assert self.n == len(board[0]), f'board must be a square.'
        self.m = int(self.n ** 0.5)
        assert self.m ** 2 == self.n, f'board length must be a square number.'
        self.board = board

    def solve(self) -> Generator:
        return super(SudokuSolver, self).solve()

    def transform_to_exact_cover(self):
        # Initialize the universe and subsets for sudo.
        universe = set(
            [f'cell[{r},{c}]' for r in range(self.n) for c in range(self.n)] +
            [f'row[{r}]has{v}' for r in range(self.n)
             for v in range(1, self.n + 1)] +
            [f'col[{c}]has{v}' for c in range(self.n)
             for v in range(1, self.n + 1)] +
            [f'grid[{r},{c}]has{v}' for r in range(self.m)
             for c in range(self.m) for v in range(1, self.n + 1)]
        )
        subsets: dict[str, set[str]] = {
            f'cell[{r},{c}]={v}': {
                f'cell[{r},{c}]', f'row[{r}]has{v}', f'col[{c}]has{v}',
                f'grid[{r // self.m},{c // self.m}]has{v}'
            } for r in range(self.n) for c in range(self.n)
            for v in range(1, self.n + 1)
        }
        return universe, subsets

    def display(self, solution: Sequence | None = None) -> None:
        # Copy the original board.
        board = [list(row) for row in self.board]

        # Fill the board with solution.
        for i in solution:
            r, c, v = list(map(int, re.findall(pattern=r'\d+', string=i)))
            board[r][c] = v

        # Print the board.
        def expand_line(line):
            return line[0] + line[5:9].join(
                [line[1:5] * (self.m - 1)] * self.m) + line[9:13]

        line0 = expand_line('╔═══╤═══╦═══╗')
        line1 = expand_line('║ . │ . ║ . ║')
        line2 = expand_line('╟───┼───╫───╢')
        line3 = expand_line('╠═══╪═══╬═══╣')
        line4 = expand_line('╚═══╧═══╩═══╝')
        symbol = ' ' + digits + ascii_lowercase + ascii_uppercase
        nums = [[''] + [
            symbol[v] if self.board[r][
                c] else f'{fg.green}{symbol[v]}{fg.rs}'
            for c, v in enumerate(row)] for r, row in enumerate(board)]
        print(line0)
        for r in range(1, self.n + 1):
            print(''.join(
                n + s for n, s in zip(nums[r - 1], line1.split('.'))
            ))
            print([line2, line3, line4][(r % self.n == 0) + (r % self.m == 0)])


class XSudokuSolver(SudokuSolver):
    def __init__(self, board: Sequence[Sequence[int]]):
        super(XSudokuSolver, self).__init__(board=board)

        universe, subsets = self.transform_to_exact_cover()
        self.exact_cover_solver = XExactCoverSolver(
            universe=universe,
            subsets=subsets,
        )

        # Remove rows and columns according to the given board.
        for r, row in enumerate(self.board):
            for c, v in enumerate(row):
                if v == 0: continue
                for cc in [
                    f'cell[{r},{c}]', f'row[{r}]has{v}', f'col[{c}]has{v}',
                    f'grid[{r // self.m},{c // self.m}]has{v}'
                ]:
                    for rr in self.exact_cover_solver.where_has[cc]:
                        for k in self.exact_cover_solver.subsets[rr]:
                            if k != cc:
                                self.exact_cover_solver.where_has[k].remove(rr)
                    self.exact_cover_solver.where_has.pop(cc)

    def solve(self) -> Generator:
        return self.exact_cover_solver.solve()

    def display(self, solution: Sequence | None = None) -> None:
        super(XSudokuSolver, self).display(solution=solution)


class MySudokuSolver(SudokuSolver):
    def __init__(self, board: Sequence[Sequence[int]]):
        super(MySudokuSolver, self).__init__(board=board)

        universe, subsets = self.transform_to_exact_cover()
        self.exact_cover_solver = MyExactCoverSolver(
            universe=universe,
            subsets=subsets,
        )

        # Remove choosable elements and subsets according to the given board.
        for r, row in enumerate(self.board):
            for c, v in enumerate(row):
                if v == 0: continue
                n = f'cell[{r},{c}]={v}'
                self.exact_cover_solver.choosable_elements -= \
                    self.exact_cover_solver.subsets[n]
                self.exact_cover_solver.choosable_subsets -= \
                    self.exact_cover_solver.intersections[n]

    def solve(self) -> Generator:
        return self.exact_cover_solver.solve()

    def display(self, solution: Sequence | None = None) -> None:
        super(MySudokuSolver, self).display(solution=solution)
