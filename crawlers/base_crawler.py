from abc import ABC, abstractmethod


# TODO: total crawler를 주로 사용하도록 하고 행동을 바꿔야함.
class AbstractCrawler(ABC):
    """
    youtube 영상 내 원하는 정보들을 수집하고 추출하기 위한 추상 클래스

    크게 두가지 동작을 정의하고 사용한다.

    1. Crawler
    - youtuber tag를 받아 해당 유튜버의 모든 동영상 정보를 얻어온다
        - video_id
        - title
        - num_click
        - uploaded_time
    2. Scraper
    - video_id로 get 요청하여 얻어온 source의 target 구간 문자열 추출
    - thumbnail, 업로드 날짜 추출
    - ex. 더보기란 내 첫째 줄, 채널 고정 댓글의 n번째 라인
    3. Parser
    - target 구간 내 추가적으로 원하는 정보 추출
    - ex. 더보기란 내 주소, 상호명 추출, 네이버지도 url 접속해 세부 정보 추출

    """

    def __init__(self, scraper, parser):
        self.scraper = scraper
        self.parser = parser

    @abstractmethod
    def crawl(self, *args, **kwargs):
        raise NotImplementedError
