import psycopg2


def write(dictionary: dict[str, int]):
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='dmcourse13', host='datamining-db.ckzuyvzulw2u.us-east-1.rds.amazonaws.com')  # TODO connection string
    cursor = conn.cursor()
    # sort dictionary?
    cursor.execute('TRUNCATE vk_words_frequency')
    for key in dictionary:
        cursor.execute('INSERT INTO vk_words_frequency VALUES (%s, %s)', (key, dictionary[key]))
    conn.commit()
