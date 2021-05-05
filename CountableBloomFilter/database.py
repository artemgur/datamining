import psycopg2

def get_words() -> list[str]:
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='dmcourse13', host='datamining-db.ckzuyvzulw2u.us-east-1.rds.amazonaws.com')
    cursor = conn.cursor()
    cursor.execute('SELECT word FROM vk_words_frequency') #TODO proper field name
    return list(map(lambda x: x[0], cursor.fetchall()))
