from pathlib import Path
import shutil

from fastapi import UploadFile
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

QUERY_VIDEOS="""
    SELECT *
    FROM videos
    WHERE title ILIKE %s
    OR description ILIKE %s
    LIMIT %s
"""

def setup():
    return database.query(SCHEMA)
    
def insert(title: str, description: str):
    video_id = str(uuid.uuid7())
    database.execute(
        INSERT_VIDEO,
        (video_id, title, description),
    )
    return video_id

#@dataclass
#class Video():
#    id: str = ""
#    upload_date: int = 0
#    title: str = ""
#    description: str = ""
#    views: int = 0
#    likes: int = 0

def search(query: str, limit: int = 1):
    return database.query(
        QUERY_VIDEOS,
        (query, query, limit),
    )

UPLOAD_DIRECTORY = Path('data/videos')
def upload(video_id: str, file: UploadFile):
    filename = UPLOAD_DIRECTORY / f'{video_id}.mp4'

    #with open(filename, 'wb') as handle:
    #    #shutil.copyfileobj(file.file, handle)
    #    pass

    return filename, file.filename





