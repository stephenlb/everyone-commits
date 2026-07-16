import videos
import database
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    videos.setup()
    videos.insert("Hello", "World")
    return {"Beep": "Boop"}

@app.post("/video")
async def video(body: dict):
    return {
        "status": "success",
        "body": body,
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
