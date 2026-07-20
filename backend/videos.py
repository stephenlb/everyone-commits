from pathlib import Path
import shutil

from fastapi import UploadFile
import database
import uuid_utils as uuid

## CDN
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'demo'  # Replace with your subscribe key
pnconfig.publish_key = 'demo'    # Replace with your publish key
pnconfig.user_id = 'python-server'

pubnub = PubNub(pnconfig)

# Channel files are sent to / downloaded from.
CDN_CHANNEL = 'new_videos'

CHUNK_SIZE = 1024 * 1024  # 1MB per chunk
PWD = Path(__file__).parent.parent

SCHEMA="""
    CREATE TABLE IF NOT EXISTS videos (
        id TEXT PRIMARY KEY,
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        title TEXT DEFAULT '',
        description TEXT DEFAULT '',
        views INT DEFAULT 0,
        likes INT DEFAULT 0,
        file_id TEXT DEFAULT '',
        file_name TEXT DEFAULT ''
    );
"""

# Existing databases created before file storage need the columns added.
MIGRATE="""
    ALTER TABLE videos ADD COLUMN IF NOT EXISTS file_id TEXT DEFAULT '';
    ALTER TABLE videos ADD COLUMN IF NOT EXISTS file_name TEXT DEFAULT '';
"""

SET_FILE="""
    UPDATE videos
    SET file_id = %s, file_name = %s
    WHERE id = %s
"""

GET_FILE="""
    SELECT file_id, file_name
    FROM videos
    WHERE id = %s
"""

DELETE_VIDEO="""
    DELETE FROM videos
    WHERE id = %s
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

LIST_VIDEOS="""
    SELECT *
    FROM videos
    WHERE file_id <> ''
    ORDER BY upload_date DESC, id DESC
    LIMIT %s
    OFFSET %s
"""

def setup():
    database.execute(SCHEMA)
    return database.execute(MIGRATE)

def insert(title: str, description: str):
    video_id = str(uuid.uuid7())
    database.execute(
        INSERT_VIDEO,
        (video_id, title, description),
    )
    return video_id

def search(query: str, limit: int = 1):
    return database.query(
        QUERY_VIDEOS,
        (query, query, limit),
    )

def list_videos(limit: int = 5, offset: int = 0):
    return database.query(
        LIST_VIDEOS,
        (limit, offset),
    )

def delete(video_id: str):
    return database.execute(DELETE_VIDEO, (video_id,))

def get_video_file(video_id: str):
    return PWD / UPLOAD_DIRECTORY / f'{video_id}.mp4'

def get_file_ref(video_id: str):
    rows = database.query(GET_FILE, (video_id,))
    return rows[0] if rows else None

def stream(video_id: str):
    ref = get_file_ref(video_id)

    # Stored on the PubNub CDN — download and stream those bytes.
    if ref and ref['file_id']:
        response = pubnub.download_file() \
            .channel(CDN_CHANNEL) \
            .file_id(ref['file_id']) \
            .file_name(ref['file_name']) \
            .sync()

        data = response.result.data
        for start in range(0, len(data), CHUNK_SIZE):
            yield data[start:start + CHUNK_SIZE]
        return

    # Fall back to a local disk file (e.g. preset videos).
    filename = get_video_file(video_id)
    with open(filename, mode='rb') as handle:
        while True:
            chunk = handle.read(CHUNK_SIZE)
            if not chunk: break
            yield chunk

UPLOAD_DIRECTORY = Path('data/videos')
def upload(video_id: str, file: UploadFile):
    filename = get_video_file(video_id)

    with open(filename, 'wb') as handle:
       shutil.copyfileobj(file.file, handle)

    return filename, file.filename

def upload_cdn(video_id: str, file: UploadFile):
    # Use the video id as the CDN file name so downloads are predictable.
    file_name = f'{video_id}.mp4'

    try:
        response = pubnub.send_file() \
            .channel(CDN_CHANNEL) \
            .file_name(file_name) \
            .message({"upload": "Success"}) \
            .file_object(file.file) \
            .sync()

        file_id = response.result.file_id
        stored_name = response.result.name

        # Persist the CDN identifiers so stream() can fetch it back.
        database.execute(SET_FILE, (file_id, stored_name, video_id))

        print("File sent:", file_id)
        return stored_name, file_id

    except PubNubException as e:
        print(f"Error: {e}")

    return False, False
