"""
Author: zed.ai
Reviewer:
2023.11.26
"""
import pandas as pd
from tqdm import tqdm

from database.db import Database
from database.entity.visit import Visit


class FireStoreUploader:
    def __init__(self, db: Database):
        self.db = db

    def update_visit_doc(
        self,
        tag,
        csv_path: str,
    ):
        visit_doc = self.db.db_client.collection("foodmap").document("visit")
        visit_dict = visit_doc.get().to_dict()

        visit_columns = list(Visit.__fields__.keys())
        visit_columns.pop(visit_columns.index("tags"))

        df = pd.read_csv(csv_path)
        for dict_row in tqdm(df[visit_columns].to_dict("records"), total=len(df)):
            dict_row["tags"] = [tag]
            visit_entity = Visit(**dict_row)

            location = visit_entity.location
            # 이미 방문 이력이 있는 가게일 경우. tag update
            if visit_dict.get(location, None):
                field = visit_dict[location]
                tags = field["tags"]
                tags.extend(visit_entity.tags)

                visit_entity.tags = tags

            visit_entity = visit_entity.dict()
            visit_entity.pop("location")

            visit_doc.update({location: visit_entity})


if __name__ == "__main__":
    db = Database()
    fsu = FireStoreUploader(db)
    csv_path = "/Users/imdohun/PycharmProjects/foodmap/crawl/kim3meals_part2.csv"
    fsu.update_visit_doc(tag="kim3meals", csv_path=csv_path)
