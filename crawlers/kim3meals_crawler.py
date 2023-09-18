import argparse

import requests

from crawlers.base_crawler import AbstractCrawler
from crawlers.parsers.base_parser import NaverMapParser
from crawlers.scrapers.base_scraper import MoreInfoScraper


class Kim3MealsCrawler(AbstractCrawler):
    """
    youtube 영상 내 원하는 정보들을 수집하고 추출하기 위한 추상 클래스

    크게 두가지 동작을 정의하고 사용한다.

    1. Scraper
    - source의 target 구간 문자열 추출
    - ex. 더보기란 내 첫째 줄, 채널 고정 댓글의 n번째 라인
    2. Parser
    - target 구간 내 원하는 정보 추출
    - ex. 더보기란 내 주소, 상호명 추출

    """

    def __init__(self, scraper: str, parser: str):
        self.scraper = scraper
        self.parser = parser

    def crawl(self, target_youtuber_tag: str, **kwargs):
        """
        food youtuber crawler

        get food youtuber's restaurant title and location

        Args:
            target_youtuber_tag (str): playlist's owner(youtuber tag)

        Returns:
            video_information (list): consist of dict that has keys(video_id(str), title(str), thunbnail_list(list))

        """
        video_information_list = list()

        # youtube url
        page_url = f"https://www.youtube.com/@{target_youtuber_tag}/videos"
        page = requests.get(page_url, verify=False)
        page_source = page.text

        # get target sub_string from total_string which has all data
        target_video_sources = self.parser.get_match_pattern_string(
            head_string="richItemRenderer",
            target_string="",
            tail_string="navigationEndpoint",
            total_page=page_source,
        )

        for target_video_source in target_video_sources:
            try:
                video_information = self.parser.parse(
                    target_video_source=target_video_source
                )
                video_information_list.append(video_information)

            except Exception as e:
                print(f"error occur : {e}")

        return video_information_list

    def total_crawl(self, target_youtuber_tag: str, save_path: str, **kwargs):
        """
        food youtuber's total videos crawler

        get food youtuber's restaurant title and location

        Args:
            target_youtuber_tag (str): playlist's owner(youtuber tag)
            save_path (str): final save path

        Returns:
            video_information (list): consist of dict that has keys(video_id(str), title(str), thunbnail_list(list))

        """
        # infinite scroll video crawler를 이용해 모든 vids 들을 받는다.
        self.scraper()


if __name__ == "__main__":
    argsparser = argparse.ArgumentParser(description="Crawler Argparse")
    argsparser.add_argument("--target_youtuber_tag", type=str, default="kim3meals")

    args = argsparser.parse_args()

    # recent crawl
    # parser = NaverMapParser()
    # scraper = MoreInfoScraper()
    # crawler = Kim3MealsCrawler(scraper=scraper, parser=parser)
    # result = crawler.crawl(args.target_youtuber_tag)
    # print(f"total result: {result}")
    # print(f"result[0]: {result[0]}")
    # print(f"len of result is : {len(result)}")

    # total crawl
    parser = NaverMapParser()
    scraper = MoreInfoScraper()
    crawler = Kim3MealsCrawler(scraper=scraper, parser=parser)
    result = crawler.crawl(args.target_youtuber_tag)
    print(f"total result: {result}")
    print(f"result[0]: {result[0]}")
    print(f"len of result is : {len(result)}")
