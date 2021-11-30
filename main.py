import config
import sys
from googleapiclient.discovery import build
from rich import print

from utils import extract_video_id, VideoStats

API_KEY = config.API_KEY
youtube = build(serviceName='youtube', version='v3', developerKey=API_KEY)


def get_stats(video_id: str) -> dict:

    requestStats = youtube.videos().list(
                part="statistics",
                id=video_id
            )
            
    responseStats = requestStats.execute()

    return VideoStats(
        views=int(responseStats["items"][0]["statistics"]["viewCount"]),
        likes=int(responseStats["items"][0]["statistics"]["likeCount"]),
        dislikes=int(responseStats["items"][0]["statistics"]["dislikeCount"]),
        comments=int(responseStats["items"][0]["statistics"]["commentCount"])
    )


if __name__ == "__main__":
    target_video_id = extract_video_id(sys.argv[1])
    stats = get_stats(target_video_id)
    print(stats)