import database

INSERT_VIDEO="""
    INSERT INTO videos (
        id, upload_date,
        title, description,
        views, likes
    )
    VALUES (?, NOW(), ?, ?, 0, 0)
"""

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
