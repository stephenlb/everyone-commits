#!/bin/zsh

## Index Test
#curl http://0.0.0.0:8000/

## Upload Video Test
#VIDEO='{"title":"Beep Boop", "description":"My First Video"}'
#curl -s http://0.0.0.0:8000/video -d $VIDEO -X POST -H "Content-Type: application/json" | jq

## List Videos
#curl -s 'http://0.0.0.0:8000/video?query=hello&limit=2'

## Upload Video
TITLE="Beep"
DESCRIPTION="Boop"
FILE="video-short.mp4"
VIDEO_DATA=$(curl -sL -F "file=@${FILE}" \
    "http://0.0.0.0:8000/upload?title=${TITLE}&description=${DESCRIPTION}")

VIDEO_ID=$(echo $VIDEO_DATA | jq -r '.id')
echo $VIDEO_DATA
echo $VIDEO_ID

## Stream Video
#curl -sL "http:/0.0.0.0:8000/stream?video_id=${VIDEO_ID}"

