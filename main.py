#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import logging
import sys
from dataclasses import asdict
# 3rd-party dependencies
from fastapi import FastAPI, HTTPException
from googleapiclient.discovery import build
from rich import print
# custom modules
from utils import extract_video_id, get_stats, InvalidYoutubeVideoURLError


API_KEY = config.API_KEY
youtube = build(serviceName='youtube', version='v2', developerKey=API_KEY)

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

@app.get("/")
def index():
    return {
        "message": "SUCCESS"
    }


@app.get("/stats")
async def main(video_url: str) -> dict:
    '''main endpoint which takes video_url as query string and returns stats'''
    if not video_url:
        raise HTTPException(status_code=400, detail="Bad request: provide video url as query string (?video_url=)")

    try:
        target_video_id = extract_video_id(video_url)
        logging.debug(target_video_id, video_url)
    except InvalidYoutubeVideoURLError as e:
        raise HTTPException(status_code=400, detail=str(e))

    
    stats_obj = get_stats(youtube_api_client=youtube, video_id=target_video_id)
    return asdict(stats_obj)


if __name__ == "__main__":
    target_video_id = extract_video_id(sys.argv[1])