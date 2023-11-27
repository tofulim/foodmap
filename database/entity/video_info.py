"""
Author: zed.ai
Reviewer:
2023.11.26
"""
from pydantic import BaseModel


class VideoInfo(BaseModel):
    tag: str
    shop_location: str
    video_id: str
    title: str
    thumbnail: str = "null"
