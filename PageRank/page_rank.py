from psycopg2.pool import ThreadedConnectionPool
import static_array
from matrix import Matrix
from crawler import connection_parameters
from py_linq import Enumerable


__postgres_pool = ThreadedConnectionPool(1, 10, **connection_parameters)
__iterations = 20
__dumping_factor = 0.85


def build_transition_matrix() -> (Matrix, list[str]):
    """Builds transition matrix of network topology from the database

    :return:Tuple: (<transition matrix>, <list of links in transition matrix in the same order>)
    """
    conn = __postgres_pool.getconn()
    cursor = conn.cursor()
    original_link = get_original_link()
    cursor.execute('SELECT DISTINCT destination FROM topology')
    unique_links: list[str] = Enumerable(cursor.fetchall()).select(lambda x: x[0]).to_list()
    if original_link not in unique_links:
        unique_links.append(original_link)
    result = Matrix(len(unique_links), len(unique_links))
    for i in range(len(unique_links)):
        cursor.execute('SELECT DISTINCT source FROM topology WHERE destination = %s', (unique_links[i],))
        source_links = Enumerable(cursor.fetchall()).select(lambda x: x[0]).to_list()
        row = __to_transition_row(source_links, unique_links)
        result[i] = row
    __postgres_pool.putconn(conn)
    __set_transition_probabilities(result)
    return result, unique_links


def __to_transition_row(source_links: list[str], unique_links: list[str]) -> static_array.Array:
    result = static_array.Array(len(unique_links))
    for i in range(len(unique_links)):
        if unique_links[i] in source_links:
            result[i] = 1
    return result


def __set_transition_probabilities(matrix: Matrix):
    for c in range(matrix.columns):
        indexes_with_values = []
        for r in range(matrix.rows):
            if matrix[r][c] != 0:
                indexes_with_values.append(r)
        if len(indexes_with_values) == 0:
            continue
        probability = __dumping_factor / len(indexes_with_values)
        for i in indexes_with_values:
            matrix[i][c] = probability


def run():
    matrix = build_transition_matrix()[0]
    n = matrix.rows
    vector = __create_vector_from_value(1 / n, n)
    dumping_vector = __create_vector_from_value((1 - __dumping_factor) / n, n)
    for i in range(__iterations):
        vector = __run_iteration(vector, matrix, dumping_vector)
    return vector


def __create_vector_from_value(value, n: int):
    result = Matrix(n, 1)
    for i in range(n):
        result[i][0] = value
    return result


def __run_iteration(vector: Matrix, matrix: Matrix, dumping_vector: Matrix) -> Matrix:
    return matrix * vector + dumping_vector


def get_original_link() -> str:
    conn = __postgres_pool.getconn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM original_link LIMIT 1')
    result = cursor.fetchall()[0][0]
    __postgres_pool.putconn(conn)
    return result

