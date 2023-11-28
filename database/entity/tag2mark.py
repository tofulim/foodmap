"""
Author: zed.ai
Reviewer:
2023.11.26
"""
from pydantic import BaseModel


class Tag2Mark(BaseModel):
    tag: str
    mark_url: str
