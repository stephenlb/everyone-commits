#!/bin/zsh

## Index Test
curl http://0.0.0.0:8000/

## Upload Video Test
VIDEO='{"title":"Beep Boop", "description":"My First Video"}'
curl -s http://0.0.0.0:8000/video -d $VIDEO -X POST -H "Content-Type: application/json" | jq
