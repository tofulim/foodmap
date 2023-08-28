from abc import ABC, abstractmethod


class AbstractScraper(ABC):
    @abstractmethod
    def scrape(self, *args, **kwargs):
        raise NotImplementedError


class MoreInfoScraper(AbstractScraper):
    """
    youtube 영상 내 더보기란 스크래퍼
    """

    # TODO : 기초 구현이 필요함
    def scrape(self, target_url: str, **kwargs):
        # get target sub_string from total_string which has all data
        target_video_sources = self.get_match_pattern_string(
            head_string="richItemRenderer",
            target_string="",
            tail_string="navigationEndpoint",
            # total_page=page_source,
        )

        return target_video_sources
