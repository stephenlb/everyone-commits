import videos
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    video = videos.Video('asdf')
    print(video)
    return {"Hello": "World"}




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
