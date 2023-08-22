import re


class Parser:
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
    def get_naver_url(
        total_page: str,
    ):
        pattern = "https?://naver.me/[^-\\\]+"
        total_pattern = re.search(pattern, total_page).group()

        return total_pattern
