"""
Author: zed.ai
Reviewer:
2023.11.26
"""
from pydantic import BaseModel


class Visit(BaseModel):
    shop_location: str
    shop_name: str
    tags: list[str]
