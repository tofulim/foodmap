import re
from abc import ABC, abstractmethod

import requests


class BaseExtractor(ABC):
    """
    youtube 영상 내 주소를 추출하기 위한 추상 클래스

    기본적으로 문자열에서 주소만을 추출해 반환하는 동작을 정의한다.
    지금 단계에서는 크게 두 가지 용도를 위한다.

    1. rule-base 추출
    - ex. 더보기란 내 첫째 줄, 채널 고정 댓글의 n번째 라인
    2. NER model base 추출
    - ner의 address entity를 이용해 주소를 추출한다.

    """

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class RuleBaseExtractor(BaseExtractor):
    """
    여러 기본적인 패턴들을 위함이다.

    1. naver 지도 애플리케이션으로 redirect되는 url 추출 (regex base)
    2. youtube 영상 더보기란 내 string location
    """

    def __init__(self):
        self.naver_url_shop_title_pattern = "data-line-title"
        self.naver_url_shop_location_pattern = "data-line-description"

    def __call__(self, extract_method: str = "naver_url", **kwargs):
        """
        parse된 base text 혹은 naver url을 전달받아 (상호, 주소)를 추출한다

        Args:
            extract_method (str): 네이버 url을 기반으로 추출할지 혹은 다른 방식일지에 대한 case 명시
            **kwargs (dict): kwargs

        Returns:
            result (dict): status_code, title, location을 담은 dict

        """
        if extract_method == "naver_url":
            naver_url = kwargs.pop("naver_url")
            result = self.get_from_naver_url(naver_url=naver_url)

        return result

    def get_from_naver_url(self, naver_url: str):
        naver_map_response = requests.get(url=naver_url)
        status_code = naver_map_response.status_code

        title, location = "", ""
        if status_code == 200:
            response_text = naver_map_response.text
            title = re.search(self.naver_url_shop_title_pattern, response_text)
            location = re.search(self.naver_url_shop_location_pattern, response_text)

        return {
            "status_code": status_code,
            "title": title,
            "location": location,
        }
