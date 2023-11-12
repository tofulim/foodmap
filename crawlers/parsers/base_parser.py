import re
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup


class AbstractParser(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def parse(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def get_naver_url_keys(
        total_page: str,
    ):
        pattern = "https?://naver.me/([a-zA-Z0-9]+?)\\\\n"
        naver_url_keys = re.findall(pattern, total_page)

        return list(set(naver_url_keys))

    @staticmethod
    def get_match_pattern_string(
        total_page: str,
        head_string: str,
        target_string: str,
        tail_string: str,
    ):
        pattern = f"(?<={head_string}).*?" + target_string + f"(?={tail_string})"
        total_pattern = re.findall(pattern, str(total_page))

        return total_pattern

    @staticmethod
    def get_thumbnail(html_source: BeautifulSoup) -> str:
        """
        bs4 html resource를 받아 문자열 썸네일을 반환한다.

        Args:
            html_source (BeautifulSoup):

        Returns:
            thumbnail_url: str

        """

        thumbnail = html_source.find("link", {"itemprop": "thumbnailUrl"})["href"]

        return thumbnail


class NaverMapParser(AbstractParser):
    """
    네이버 맵 url 내에 있는 가게 주소와 상호명을 가져온다.
    (+ naver map id)
    """

    def __init__(self):
        # 더보기란에서 정보를 얻겠다는 것
        self.request_url = "https://www.youtube.com/watch?v={video_id}"
        self.naver_url_shop_title_pattern = "data-line-title"
        self.naver_url_shop_location_pattern = "data-line-description"

    def parse(self, video_id: str, **kwargs):
        """
        개별 url의 영상을 분석해 thumbnail, store names, store address를 반환한다.

        Args:
            video_id (str): youtube vid
            **kwargs ():

        Returns:
            naver_map_result (dict | List(dict)): 복수 혹은 단수의 가게 정보

        """

        response = requests.get(
            url=self.request_url.format(video_id=video_id), verify=False
        )
        html_source = response.text
        naver_url_keys = self.get_naver_url_keys(
            total_page=html_source,
        )

        naver_map_results = []
        for naver_url_key in naver_url_keys:
            url = f"https://naver.me/{naver_url_key}"
            naver_map_source = requests.get(url, verify=False)
            # ISO-8859-1 인코딩 문제로 한글 깨지는 문제 해결
            naver_map_source.encoding = "utf-8"
            naver_map_source = naver_map_source.text
            store_info = self.get_store_info(naver_map_source=naver_map_source)

            naver_map_results.append(
                {
                    "video_id": video_id,
                    "naver_url_key": naver_url_key,
                    **store_info,
                }
            )

        return naver_map_results

    def get_store_info(self, naver_map_source: str):
        pattern = '{target}="([^"]+)"'
        name = re.search(
            pattern.format(target=self.naver_url_shop_title_pattern), naver_map_source
        ).group(1)
        location = re.search(
            pattern.format(target=self.naver_url_shop_location_pattern),
            naver_map_source,
        ).group(1)

        return {
            "shop_name": name,
            "shop_location": location,
        }


if __name__ == "__main__":
    nmp = NaverMapParser()
    vid = "LvfBEJipU6o"
    res = nmp.parse(video_id=vid)
    print(res)
