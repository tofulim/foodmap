import re
from abc import ABC

import requests
from bs4 import BeautifulSoup


class AbstractParser(ABC):
    def __init__(self):
        pass

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

    @staticmethod
    def get_youtuber_mark_image(youtuber_tag: str):
        """
        youtuber의 대표 이미지의 url을 추출한다.
        해당 이미지를 지도의 마크로 사용하기 위함.

        Args:
            youtuber_tag (str): 유튜버 태그 ex. kim3meals

        Returns:
            mark_url (str): 썸네일 마크 이미지 url

        """
        url = f"https://www.youtube.com/@{youtuber_tag}"
        response = requests.get(
            url,
            headers={
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
            },
        )
        response.encoding = "utf-8"

        pattern = (
            '<link itemprop="url" href="'
            + "(https://yt3.+?)"
            + '"><meta itemprop="width" content="900">'
        )
        mark_url = re.search(pattern, response.text).group(1)

        return mark_url


if __name__ == "__main__":
    youtuber_tags = [
        "kim3meals",
        "jazziseverywhere",
        "leeplay.official",
    ]

    abs_parser = AbstractParser()
    for youtuber_tag in youtuber_tags:
        mark_url = abs_parser.get_youtuber_mark_image(youtuber_tag)
        print(mark_url)
