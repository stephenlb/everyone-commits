import database
import uuid_utils as uuid

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

INSERT_VIDEO="""
    INSERT INTO videos (
        id, upload_date,
        title, description,
        views, likes
    )
    VALUES (%s, NOW(), %s, %s, 0, 0)
"""

def setup():
    return database.query(SCHEMA)
    
def insert(title: str, description: str):
    id = str(uuid.uuid7())
    return database.execute(
        INSERT_VIDEO,
        (id, title, description),
    )

#@dataclass
class Video():
    id: str = ""
    upload_date: int = 0
    title: str = ""
    description: str = ""
    views: int = 0
    likes: int = 0

async def fetch(video_id: int):
    pass

async def search(term: str):
    pass

async def upload():
    pass
