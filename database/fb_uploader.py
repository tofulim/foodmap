"""
Author: zed.ai
Reviewer:
2023.11.26
"""
import os

import pandas as pd
import requests
from tqdm import tqdm

from database.db import Database
from database.entity.video_info import VideoInfo
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

            location = visit_entity.shop_location
            # 이미 방문 이력이 있는 가게일 경우. tag update
            if visit_dict.get(location, None):
                field = visit_dict[location]
                tags = field["tags"]
                tags.extend(visit_entity.tags)

                visit_entity.tags = tags

            visit_entity = visit_entity.dict()
            visit_entity.pop("shop_location")

            xy_geolocation = self.get_xy_geolocation(location)

            if xy_geolocation is not None:
                visit_entity["geo_location"] = xy_geolocation

                visit_doc.update({location: visit_entity})

    def get_xy_geolocation(self, location: str):
        """
        네이버 지도에 사용자들이 등록한 도로명 주소를 받아 x, y 좌표를 반환한다.
        단, 도로명 주소가 없을 경우 None을 반환한다. 그리고 도로명 주소는 잘못된 주소일 수 있다.

        Args:
            location (str): 가게의 도로명 주소

        Returns:
            geo_location (tuple): (x, y) 좌표

        """
        url = os.getenv("NCP-GEOCODE-REQ-URL")
        params = {
            "query": location,
        }
        headers = {
            "X-NCP-APIGW-API-KEY-ID": os.getenv("X-NCP-APIGW-API-KEY-ID"),
            "X-NCP-APIGW-API-KEY": os.getenv("X-NCP-APIGW-API-KEY"),
        }
        response = requests.get(url, params=params, headers=headers)
        addresses = response.json()["addresses"]
        if len(addresses) == 0:
            return None
        return addresses[0]["x"], addresses[0]["y"]

    def update_video_info_doc(
        self,
        tag,
        part1_csv_path: str,
        part2_csv_path: str,
    ):
        part1_df = pd.read_csv(part1_csv_path)
        part2_df = pd.read_csv(part2_csv_path)

        total_df = part2_df.join(
            part1_df.set_index("video_id"), on="video_id", how="left"
        )

        video_info_doc = self.db.db_client.collection("foodmap").document("video_info")
        ori_tag_dict = video_info_doc.get().to_dict()
        ori_tag_dict = ori_tag_dict.get(tag, {})

        video_info_columns = list(VideoInfo.__fields__.keys())
        video_info_columns.pop(video_info_columns.index("tag"))

        for dict_row in tqdm(
            total_df[video_info_columns].to_dict("records"), total=len(total_df)
        ):
            dict_row["tag"] = tag
            if not isinstance(dict_row["thumbnail"], str):
                dict_row["thumbnail"] = ""
            visit_entity = VideoInfo(**dict_row)

            try:
                ori_tag_dict.update(
                    {
                        visit_entity.shop_location: {
                            "video_id": visit_entity.video_id,
                            "thumbnail": visit_entity.thumbnail,
                            "title": visit_entity.title,
                        }
                    }
                )
                video_info_doc.update({tag: ori_tag_dict})
            except Exception as e:
                print(f"error {e}")
                print(visit_entity)
                break


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv("/Users/imdohun/PycharmProjects/foodmap/crawl/config/conf.env")
    # print(os.getenv("X-NCP-APIGW-API-KEY-ID"))
    #
    db = Database()
    fsu = FireStoreUploader(db)
    # csv_path = "/Users/imdohun/PycharmProjects/foodmap/crawl/kim3meals_part2.csv"
    # fsu.update_visit_doc(tag="kim3meals", csv_path=csv_path)

    part1_path = "/Users/imdohun/PycharmProjects/foodmap/crawl/kim3meals_part1.csv"
    part2_path = "/Users/imdohun/PycharmProjects/foodmap/crawl/kim3meals_part2.csv"
    fsu.update_video_info_doc(
        tag="kim3meals", part1_csv_path=part1_path, part2_csv_path=part2_path
    )
