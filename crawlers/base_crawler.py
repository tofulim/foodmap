from abc import ABC, abstractmethod


# TODO: total crawler를 주로 사용하도록 하고 행동을 바꿔야함.
class AbstractCrawler(ABC):
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

    def __init__(self, scraper, parser):
        self.scraper = scraper
        self.parser = parser

    @abstractmethod
    def crawl(self, *args, **kwargs):
        raise NotImplementedError
