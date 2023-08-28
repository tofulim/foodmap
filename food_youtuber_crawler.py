import argparse

import requests
from extractor import RuleBaseExtractor
from pattern_parser import Parser


def food_youtuber_crawl(
    target_youtuber_tag: str, extractor: RuleBaseExtractor, parser: Parser
):
    """food youtuber crawler
    get food youtuber's restaurant title and location
    Args:
        target_youtuber_tag (str): playlist's owner(youtuber tag)
        extractor (RuleBaseExtractor):

    Returns:
        video_information (list): consist of dict that has keys(video_id(str), title(str), thunbnail_list(list))

    """
    video_information_list = list()

    # youtube url
    page_url = f"https://www.youtube.com/@{target_youtuber_tag}/videos"
    page = requests.get(page_url, verify=False)
    page_source = page.text

    # get target sub_string from total_string which has all data
    target_video_sources = parser.get_match_pattern_string(
        head_string="richItemRenderer",
        target_string="",
        tail_string="navigationEndpoint",
        total_page=page_source,
    )

    for target_video_source in target_video_sources:
        try:
            naver_url = parser.get_naver_url(
                total_page=target_video_source,
            )

            video_id = parser.get_match_pattern_string(
                head_string='videoId"\:"',
                target_string="",
                tail_string='"\,"',
                total_page=target_video_source,
            )
            title = parser.get_match_pattern_string(
                head_string='text"\:"',
                target_string="",
                tail_string='"\}\]',
                total_page=target_video_source,
            )
            thumbnail_list = parser.get_match_pattern_string(
                head_string='url"\:"',
                target_string="",
                tail_string='"\,"',
                total_page=target_video_source,
            )

            video_information = {
                "video_id": video_id[0],
                "playlist_title": title[0],
                "thumbnail_list": thumbnail_list,
                "naver_url": naver_url,
            }

            video_information_list.append(video_information)
        except Exception as e:
            print(f"error occur : {e}")

    assert (
        video_id or title or thumbnail_list
    ), f"len doesn't match video_id {len(video_id)}, title {len(title)}, thumbnail_list {len(thumbnail_list)}"

    return video_information_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawler Argparse")
    parser.add_argument("--target_youtuber_tag", type=str, default="kim3meals")

    args = parser.parse_args()

    parser = Parser()
    extractor = RuleBaseExtractor()
    result = food_youtuber_crawl(args.target_youtuber_tag, extractor, parser)
    print(f"total result: {result}")
    print(f"result[0]: {result[0]}")
    print(f"len of result is : {len(result)}")
