import re
from dataclasses import dataclass, field


@dataclass
class VideoStats:
    views: int
    likes: int
    dislikes: int
    comments: int
    total_reactions: int = field(init=False)
    like_ratio: float = field(init=False)
    dislike_ratio: float = field(init=False)
    
    def __post_init__(self):
        self.total_reactions = self.likes + self.dislikes
        self.like_ratio = self.likes / self.total_reactions
        self.dislike_ratio = self.dislikes / self.total_reactions


def extract_video_id(url: str) -> str:
    pattern = re.compile(r'(\/|v=)([a-zA-Z0-9-_]{11})(.*)')
    match = re.search(pattern, url)

    if match:
        return match.group(2)

    return 'Could not extract video ID from URL.'


if __name__ == "__main__":
    dummy  = {'statistics': {'viewCount': '1263994', 'likeCount': '22060', 'dislikeCount': '893', 'favoriteCount': '0', 'commentCount': '2759'}}
    v = VideoStats(
        int(dummy["statistics"]["viewCount"]),
        int(dummy["statistics"]["likeCount"]),
        int(dummy["statistics"]["dislikeCount"]),
        int(dummy["statistics"]["commentCount"])
    )