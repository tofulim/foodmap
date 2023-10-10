import re
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup


class AbstractParser(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def parse(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def get_naver_url(
        total_page: str,
    ):
        pattern = "https?://naver.me/[^-\\\]+"
        total_pattern = re.search(pattern, total_page).group()

        return total_pattern

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
    네이버 맵 url 내에 있는 가게 주소와 상호명을 가져온다
    """

    def __init__(self):
        # 더보기란에서 정보를 얻겠다는 것
        self.type = "more_info"
        self.request_url = "https://www.youtube.com/watch?v={video_id}"

    # TODO: scraper로 분리해서 thumnail이랑 더보기란이나 댓글을 key:value로 구분해서 key: html_Source로 하게 해야함
    def parse(self, video_id: str, **kwargs):

        # response = requests.get(
        #     url=self.request_url.format(video_id=video_id), verify=False
        # )
        # html_source = BeautifulSoup(response.text, "html.parser")
        #
        # html_source.find()
        # naver_url = self.get_naver_url(
        #     total_page=target_video_source,
        # )
        # video_id = self.get_match_pattern_string(
        #     head_string=r'videoId"\:"',
        #     target_string="",
        #     tail_string=r'"\,"',
        #     total_page=target_video_source,
        # )
        # title = self.get_match_pattern_string(
        #     head_string=r'text"\:"',
        #     target_string="",
        #     tail_string=r'"\}\]',
        #     total_page=target_video_source,
        # )
        # thumbnail_list = self.get_match_pattern_string(
        #     head_string=r'url"\:"',
        #     target_string="",
        #     tail_string=r'"\,"',
        #     total_page=target_video_source,
        # )
        # naver_map_source = requests.get(naver_url, verify=False)
        # # ISO-8859-1 인코딩 문제로 한글 깨지는 문제 해결
        # naver_map_source.encoding = "utf-8"
        # naver_map_source = naver_map_source.text
        # store_info = self.get_store_info(naver_map_source=naver_map_source)
        #
        # return {
        #     "video_id": video_id[0],
        #     "playlist_title": title[0],
        #     "thumbnail_list": thumbnail_list,
        #     "naver_url": naver_url,
        #     **store_info,
        # }
        pass

    def get_store_info(self, naver_map_source: str):
        pass
        # pattern = '{target}="([^"]+)"'
        # name = re.search(
        #     pattern.format(target=self.naver_url_shop_title_pattern), naver_map_source
        # ).group(1)
        # location = re.search(
        #     pattern.format(target=self.naver_url_shop_location_pattern),
        #     naver_map_source,
        # ).group(1)
        #
        # return {
        #     "shop_name": name,
        #     "shop_location": location,
        # }
