import re
from dataclasses import dataclass, field
from rich import print

@dataclass
class VideoStats:
    '''class which holds basic stats about a video'''
    views: int
    likes: int
    dislikes: int
    comments: int
    total_reactions: int = field(init=False)
    like_ratio: float = field(init=False)
    dislike_ratio: float = field(init=False)
    like_ratio_perc: str = field(init=False)
    dislike_ratio_perc: str = field(init=False)
    
    def __post_init__(self):
        self.total_reactions = self.likes + self.dislikes

        self.like_ratio = self.likes / self.total_reactions
        self.dislike_ratio = self.dislikes / self.total_reactions

        self.like_ratio_perc = f"{round(self.like_ratio*100, 2)}%"
        self.dislike_ratio_perc = f"{round(self.dislike_ratio*100, 2)}%"



class InvalidYoutubeVideoURLError(Exception):
    pass

class NoStatsRetrievedError(Exception):
    pass


def extract_video_id(url: str) -> str:
    '''utility function which extracts video_id from a Youtube video URL'''
    pattern = re.compile(r'(\/|v=)([a-zA-Z0-9-_]{11})(.*)')
    match = re.search(pattern, url)

    if match:
        return match.group(2)
    else:
        raise InvalidYoutubeVideoURLError("Not a valid video URL")


def get_stats(youtube_api_client, video_id: str) -> VideoStats:
    '''main function executed by API which fetches and returns video stats'''
    requestStats = youtube_api_client.videos().list(
                part="statistics",
                id=video_id
            )
            
    responseStats = requestStats.execute()
    print(responseStats)


    if len(responseStats["items"]) == 0:
        raise NoStatsRetrievedError("No stats retrieved from supplied URL")


    return VideoStats(
        views=int(responseStats["items"][0]["statistics"]["viewCount"]),
        likes=int(responseStats["items"][0]["statistics"]["likeCount"]),
        dislikes=int(responseStats["items"][0]["statistics"]["dislikeCount"]),
        comments=int(responseStats["items"][0]["statistics"]["commentCount"])
    )


if __name__ == "__main__":
    dummy  = {'statistics': {'viewCount': '1263994', 'likeCount': '22060', 'dislikeCount': '893', 'favoriteCount': '0', 'commentCount': '2759'}}
    v = VideoStats(
        int(dummy["statistics"]["viewCount"]),
        int(dummy["statistics"]["likeCount"]),
        int(dummy["statistics"]["dislikeCount"]),
        int(dummy["statistics"]["commentCount"])
    )
    print(v)