import psycopg

CONNECTION="postgresql://youtube:youtube@0.0.0.0:5432/youtube"


SCHEMA="""
    CREATE TABLE IF NOT EXISTS videos (
        id TEXT PRIMARY KEY,
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        title TEXT DEFAULT '',
        description TEXT DEFAULT '',
        views INT DEFAULT 0,
        likes INT DEFAULT 0
    );
"""


def setup():
    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cursor:
            result = cursor.execute(SCHEMA)

def query(statement):
    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cursor:
            return cursor.execute(SCHEMA)
    
def execute(statement):
    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cursor:
            return cursor

def connect():
    pass
    
