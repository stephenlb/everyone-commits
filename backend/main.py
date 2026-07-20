from contextlib import asynccontextmanager

import videos
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# Ensure the schema + column migration is in place before serving.
@asynccontextmanager
async def lifespan(app: FastAPI):
    videos.setup()
    yield

app = FastAPI(lifespan=lifespan)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allows all origins
    allow_credentials=True,   # Allows cookies and credentials
    allow_methods=["*"],      # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],      # Allows all headers
)

@app.get("/")
async def root():
    return {"Beep": "Boop"}

@app.get("/stream")
async def stream(video_id: str):
    streamable = videos.stream(video_id)
    return StreamingResponse(streamable, media_type="video/mp4")
    
@app.get("/video")
async def video(query: str, limit: int = 2):
    results = videos.search(query, limit)
    return {"videos": results}

@app.get("/videos")
async def list_videos(limit: int = 5, offset: int = 0):
    results = videos.list_videos(limit, offset)
    return {"videos": results}

@app.post("/upload")
async def upload(
    title: str,
    description: str,
    file: UploadFile,
):
    video_id = videos.insert(title, description)
    #new_name, original = videos.upload(video_id, file)
    new_name, original = videos.upload_cdn(video_id, file)

    # CDN upload failed — drop the orphan row instead of leaving an
    # unplayable video in the feed, and report the error.
    if not original:
        videos.delete(video_id)
        raise HTTPException(status_code=502, detail="CDN upload failed")

    return {
        "id": video_id,
        "title": title,
        "description": description,
        "original" : original,
        "name" : new_name,
    }
