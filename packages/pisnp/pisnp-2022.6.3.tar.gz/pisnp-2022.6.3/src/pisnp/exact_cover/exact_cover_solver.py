# coding=utf-8
#
# exact_cover_solver.py in pisnp/exact_cover
#
# created by 谢方圆 (self.universeIE Fangyuan) on 2022-06-05
# Copyright © 2022 谢方圆 (self.universeIE Fangyuan). All rights reserved.
#
# Solver for exact cover problem.


from abc import ABCMeta
from typing import Any, Generator

from sty import fg

from pisnp.solver import Solver


class ExactCoverSolver(Solver, metaclass=ABCMeta):
    def __init__(self, universe: set, subsets: dict[Any, set]):
        """Solver for an exact cover problem.

        Args:
            universe: A universe.
            subsets: A collection of named subsets of the universe.
        """
        self.universe, self.subsets, self.solution = universe, subsets, set()

    def solve(self) -> Generator:
        return super(ExactCoverSolver, self).solve()

    def display(self, solution: set | None = None) -> None:
        print(f'   {" ".join(map(str, cols := sorted(self.universe)))}')
        for i, subset in self.subsets.items():
            print(
                f'''{fg.green if solution and i in solution else ''}{i}: {
                " ".join("@" if c in subset else "." for c in cols)}{
                fg.rs if solution and i in solution else ''}'''
            )


class XExactCoverSolver(ExactCoverSolver):
    def __init__(self, universe: set, subsets: dict[Any, set]):
        """Solver for an exact cover problem by algorithm X.

        Args:
            universe: A universe.
            subsets: A collection of named subsets of the universe.
        """
        super(XExactCoverSolver, self).__init__(
            universe=universe,
            subsets=subsets,
        )

        self.where_has: dict[Any, set] = {x: set() for x in self.universe}
        for name, subset in self.subsets.items():
            for value in subset:
                self.where_has[value].add(name)

    def solve(self) -> Generator:
        """Solve an exact cover problem by algorithm x.

        Returns:
            A list of disjoint subsets whose union is the universe.
        """
        if not self.where_has:
            # If no column, a solution is found.
            yield set(self.solution)
        else:
            # Choose the column with minimum length to search quicker.
            # If min len(self.universe[x]) == 0, there is no solution.
            col = min(self.where_has, key=lambda x: len(self.where_has[x]))
            for row in list(self.where_has[col]):
                # Select one row.
                self.solution.add(row)

                # Delete rows and columns.
                cols = []
                for c in list(self.subsets[row]):
                    for r in self.where_has[c]:
                        # Delete a row in universe.
                        for k in self.subsets[r]:
                            if k != c:
                                self.where_has[k].remove(r)
                    # Delete a column in universe and save it for restore.
                    cols.append(self.where_has.pop(c))

                # Backtrack to choose more rows.
                for s in self.solve():
                    yield s

                # Restore universe.
                for c in reversed(list(self.subsets[row])):
                    self.where_has[c] = cols.pop()
                    for r in self.where_has[c]:
                        for k in self.subsets[r]:
                            if k != c:
                                self.where_has[k].add(r)

                # Deselect one row.
                self.solution.remove(row)

    def display(self, solution: set | None = None) -> None:
        super(XExactCoverSolver, self).display(solution=solution)


class MyExactCoverSolver(ExactCoverSolver):
    def __init__(self, universe: set, subsets: dict[Any, set]):
        super(MyExactCoverSolver, self).__init__(
            universe=universe,
            subsets=subsets,
        )

        self.choosable_elements = set(universe)
        self.choosable_subsets = set(subsets)
        self.intersections: dict[Any, set] = {
            n1: {n2 for n2, s2 in self.subsets.items() if s1.intersection(s2)}
            for n1, s1 in self.subsets.items()
        }

    def solve(self) -> Generator:
        if len(self.choosable_elements) == 0:
            yield set(self.solution)
        else:
            e = min(self.choosable_elements, key=lambda x: sum(
                x in self.subsets[n] for n in self.choosable_subsets
            ))
            for name in filter(
                    lambda x: e in self.subsets[x],
                    list(self.choosable_subsets),
            ):
                self.solution.add(name)
                self.choosable_elements -= self.subsets[name]
                removed = self.intersections[name] & self.choosable_subsets
                self.choosable_subsets -= removed
                for s in self.solve():
                    yield s
                self.choosable_subsets |= removed
                self.choosable_elements |= self.subsets[name]
                self.solution.remove(name)

    def display(self, solution: set | None = None) -> None:
        super(MyExactCoverSolver, self).display(solution=solution)
