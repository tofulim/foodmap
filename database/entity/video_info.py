"""
Author: zed.ai
Reviewer:
2023.11.26
"""
from pydantic import BaseModel


class VideoInfo(BaseModel):
    tag: str
    location: str
    id: str
    title: str
    thumbnail: str
