"""
Author: zed.ai
Reviewer:
2023.11.26
"""
from pydantic import BaseModel


class Visit(BaseModel):
    location: str
    shop_name: str
    tags: list[str]


if __name__ == "__main__":
    v = Visit(location="d", shop_name="g", tags=["asd"])
    print(v.dict())
    print(Visit.__fields__.keys())
    cols = list(Visit.__fields__.keys())
    cols.pop(cols.index("tags"))
    import pandas as pd

    df = pd.read_csv("/Users/imdohun/PycharmProjects/foodmap/crawl/kim3meals_part2.csv")

    print(df[cols].to_dict("records")[0])
