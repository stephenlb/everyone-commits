import psycopg
from psycopg.rows import dict_row

CONNECTION="postgresql://youtube:youtube@0.0.0.0:5432/youtube"

def query(statement, params=None):
    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(statement, params)
            return [row for row in cursor]
    
def execute(statement, params=None):
    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cursor:
            return cursor.execute(statement, params)
    
