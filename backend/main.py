import videos
import database
from fastapi import FastAPI, UploadFile
app = FastAPI()

@app.get("/")
async def root():
    videos.setup()
    return {"Beep": "Boop"}

@app.get("/video")
async def video(query: str, limit: int = 2):
    results = videos.search(query, limit)
    return {"videos": results}

## Video Container return Video ID
@app.post("/video")
async def video(body: dict):
    ## ARyzenCPU - ADD VALIDITION
    title = body['title']
    description = body['description']
    video_id = videos.insert(title, description)
    return {
        "id": video_id,
    }

@app.post("/upload")
async def upload(
    title: str,
    description: str,
    file: UploadFile,
):
    video_id = videos.insert(title, description)
    new_name, original = videos.upload(video_id, file)
    return {
        "id": video_id,
        "title": title,
        "description": description,
        "original" : original,
        "name" : new_name,
    }

## TODO Upload Videos
## -> sign URL for S3 direct upload
## -> store video metadata in DB
## -> PUT to Queue for procoessing
## -> Thumbnail

## TODO Fetch Videos
## -> homepage
## -> trending - last 7 days
## -> search
## -> infinite scroll


## TODO Task Management - Nureddin @Nooreldien
## TODO Likes API
## TODO Track views counter
## TODO 
