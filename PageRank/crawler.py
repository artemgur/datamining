import requests
from bs4 import BeautifulSoup
import threading
from urllib.parse import urljoin
import concurrent.futures
from psycopg2.pool import ThreadedConnectionPool

connection_parameters = {
    'user': 'postgres',
    'password': 'dmcourse13',
    'host': 'datamining-db.ckzuyvzulw2u.us-east-1.rds.amazonaws.com',
    'port': 5432,
    'database': 'postgres'
}
__processed_links: set
# dead_end_links: set
__thread_local = threading.local()
__pool = concurrent.futures.ThreadPoolExecutor(max_workers=8)
__postgres_pool = ThreadedConnectionPool(1, 10, **connection_parameters)
__original_link: str


def run(url: str, iteration: int):
    __prepare_table()
    global __processed_links  # , dead_end_links
    __processed_links = set()
    # dead_end_links = set()
    global __original_link
    __original_link = url
    __write_original_link_to_database()
    __process_link(url, iteration)


def __get_session():
    if not hasattr(__thread_local, "session"):
        __thread_local.session = requests.Session()
    return __thread_local.session


def __process_link(url: str, iterations_left: int):
    __processed_links.add(url)
    session = __get_session()
    with session.get(url) as response:
        parsed = BeautifulSoup(response.content)
        # found_links = False
        for a in parsed.find_all('a'):
            # found_links = True
            maybe_relative: str = a.get('href')
            if not type(maybe_relative) == str:
                continue
            if '#' in maybe_relative:
                continue
            absolute = urljoin(url, maybe_relative)
            if (iterations_left > 1) and (absolute not in __processed_links):
                __pool.submit(__process_link, url=absolute, iterations_left=iterations_left - 1)
            __write_to_database(url, absolute)
        # if not found_links:
        #    dead_end_links.add(url)
        # links = py_linq.Enumerable(parsed.find_all('a')).select(lambda x:urljoin(url, x.get('href'))).to_list()
        # with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        #    executor.map(lambda x: __process_link(x, iteration-1), links)


def __write_to_database(source: str, destination: str):
    conn = __postgres_pool.getconn()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO topology VALUES (%s, %s)', (source, destination))
    conn.commit()
    __postgres_pool.putconn(conn)


def __prepare_table():
    conn = __postgres_pool.getconn()
    cursor = conn.cursor()
    cursor.execute(\
    '''CREATE TABLE IF NOT EXISTS topology(
    source TEXT,
    destination TEXT)''')
    cursor.execute('TRUNCATE TABLE topology')
    conn.commit()
    __postgres_pool.putconn(conn)


def __write_original_link_to_database():
    conn = __postgres_pool.getconn()
    cursor = conn.cursor()
    cursor.execute(\
    '''CREATE TABLE IF NOT EXISTS original_link(
    url TEXT)''')
    cursor.execute('TRUNCATE TABLE original_link')
    cursor.execute('INSERT INTO original_link VALUES (%s)', (__original_link,))
    conn.commit()
    __postgres_pool.putconn(conn)


# def __write_dead_ends():
#    pool.map(__write_dead_end, dead_end_links)


# def __write_dead_end(url: str):
#     conn = postgres_pool.getconn()
#     cursor = conn.cursor()
#     cursor.execute('UPDATE topology SET dead_end = true WHERE destination = %s', url)
#     conn.commit()
#     postgres_pool.putconn(conn)
