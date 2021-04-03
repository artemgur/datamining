from static_array import Array
from py_linq import Enumerable
from typing import Generic, TypeVar

T = TypeVar('T')


class Matrix(Generic[T]):
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.__rows_array = Array(rows)
        for x in range(len(self.__rows_array)):
            self.__rows_array[x] = Array(columns)

    def __getitem__(self, key: int) -> Array:
        return self.__rows_array[key]

    def __setitem__(self, key: int, value: Array):
        if len(value) != self.columns:
            raise ValueError("Length of row isn't equal to number of columns in matrix")
        self.__rows_array[key] = value

    def get(self, row: int, column: int):
        if row >= self.rows:
            raise IndexError('Row index is out of bounds of the matrix')
        if column >= self.columns:
            raise IndexError('Column index is out of bounds of the matrix')
        return self.__rows_array[row][column]

    def set(self, row: int, column: int, value):
        if row >= self.rows:
            raise IndexError('Row index is out of bounds of the matrix')
        if column >= self.columns:
            raise IndexError('Column index is out of bounds of the matrix')
        self.__rows_array[row][column] = value

    def __mul__(self, b: 'Matrix') -> 'Matrix':
        if self.columns != b.rows:
            raise ValueError("Matrixes are impossible to multiply. Column number of first matrix isn't equal to row number of second matrix")
        result = Matrix(self.rows, b.columns)
        for r in range(self.rows):
            for c in range(b.columns):
                cell_value = 0
                for i in range(self.columns):
                    cell_value += self.get(r, i) * b.get(i, c)
                result.set(r, c, cell_value)
        return result

    def __add__(self, b: 'Matrix') -> 'Matrix':
        if self.rows != b.rows or self.columns != b.columns:
            raise ValueError("Matrixes are impossible to sum. Dimensions of matrixes aren't equal")
        result = Matrix(self.rows, self.columns)
        for r in range(self.rows):
            for c in range(self.columns):
                result.set(r, c, self.get(r, c) + b.get(r, c))
        return result

    def __str__(self):
        return Enumerable(self.__rows_array).select(lambda x: str(x)).aggregate(lambda aggr, element: aggr + '\n' + element)