# Currently doesn't work properly
from matrix import Matrix
import pathos.multiprocessing as multiprocessing
from py_linq import Enumerable


def __concat_matrixes(a: Matrix, b: Matrix) -> Matrix:
    if a.columns != b.columns:
        raise ValueError("Can't concat matrixes, because they have different number of columns")
    for x in range(b.rows):
        a._Matrix__rows_array._Array__list.append(b._Matrix__rows_array[x])
    a._Matrix__rows_array._Array__length += b.rows
    return a


def __multiply_partial(a: Matrix, b: Matrix, first_row: int, last_row: int) -> Matrix:
    print(f'Started multiplying from row {first_row} to row {last_row}')
    result = Matrix(last_row - first_row + 1, b.columns)
    for r in range(first_row, last_row):
        for c in range(b.columns):
            cell_value = 0
            for i in range(a.columns):
                cell_value += a.get(r, i) * b.get(i, c)
            result.set(r - first_row, c, cell_value)
    print(f'Finished multiplying from row {first_row} to row {last_row}')
    return result


# Multiprocessing code is here
def multiply_multiprocessed(a: Matrix, b: Matrix) -> Matrix:
    print('Multiplication started!')
    step = a.rows // 8
    tuples = Enumerable(range(a.rows)).select(lambda x: (step * x, step * (x + 1))).to_list()
    last_tuple = tuples[len(tuples) - 1]
    tuples[len(tuples) - 1] = (last_tuple[0], a.rows - 1)
    with multiprocessing.Pool(8) as pool:
        pool_result = pool.map(lambda x: __multiply_partial(a, b, x[0], x[1]), tuples)
    print('Multiplication finished!')
    return Enumerable(pool_result).aggregate(lambda aggr, new: __concat_matrixes(aggr, new))
