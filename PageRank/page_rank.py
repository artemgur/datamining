from psycopg2.pool import ThreadedConnectionPool
import static_array
from matrix import Matrix
from crawler import connection_parameters
from py_linq import Enumerable
#import multiprocessed_matrix_multiplier
import concurrent.futures


__postgres_pool = ThreadedConnectionPool(1, 10, **connection_parameters)
__iterations = 5
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


def run() -> (Matrix, list[str]):
    matrix, unique_links = build_transition_matrix()
    n = matrix.rows
    vector = __create_vector_from_value(1 / n, n)
    dumping_vector = __create_vector_from_value((1 - __dumping_factor) / n, n)
    for i in range(__iterations):
        print(i)
        vector = __run_iteration(vector, matrix, dumping_vector)
    __write_results_to_database(vector, unique_links)
    return vector, unique_links


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


def to_sorted_tuples(matrix: Matrix, unique_links: list[str]):
    result:list[(float, str)] = []
    for x in range(matrix.rows):
        result.append((matrix[x][0], unique_links[x]))
    return sorted(result, key=lambda x: x[0])

def write_tuple(rank: float, name: str):
    conn = __postgres_pool.getconn()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO page_rank VALUES (%s, %s)', rank, name)
    conn.commit()
    __postgres_pool.putconn(conn)


def __write_results_to_database(vector: Matrix, unique_links: list[str]):
    conn = __postgres_pool.getconn()
    cursor = conn.cursor()
    cursor.execute(\
    '''CREATE TABLE IF NOT EXISTS page_rank(
    value FLOAT,
    url TEXT)''')
    cursor.execute('TRUNCATE TABLE page_rank')
    conn.commit()
    __postgres_pool.putconn(conn)
    list_of_tuples = [(vector.get(i, 0), unique_links[i]) for i in range(len(unique_links))]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        pool.map(lambda x: __write_results_to_database(x[0], x[1]), list_of_tuples)



