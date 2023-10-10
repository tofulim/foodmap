import logging
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from utils.scroll_queue import Queue

logger = logging.getLogger()
# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)
# log 출력 형식
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class InfinitScrollVideoCrawler:
    """
    유튜버의 동영상이 30개 이상일 경우 하단 스크롤을 통해야 동적으로 영상들이 로딩된다.
    이를 빠르게 수행하고 유튜버의 모든 영상에 대해 (vid, 조회수, 업로드 시간)을 수집해 csv로 반환하는 동작을 수행한다.
    """

    def __init__(self):
        # set option of selenium
        options = ChromeOptions()
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        options.add_argument("user-agent=" + user_agent)
        options.add_argument("lang=ko_KR")
        options.add_argument("headless")
        options.add_argument("window-size=1920x1080")
        options.add_argument("disable-gpu")
        options.add_argument("--no-sandbox")
        # 크롬 드라이버 최신 버전 설정
        service = ChromeService(executable_path=ChromeDriverManager().install())

        # chrome driver
        self.driver = webdriver.Chrome(service=service, options=options)

    def __call__(self, target_url: str, save_path: str):
        """
        infinite crawl 수행
        유튜버의 동영상들을 보여주는 페이지인 타겟 url을 받아 모든 동영상을 가져온다.

        Args:
            target_url (str): 모든 동영상들을 볼 수 있는 페이지 ex. https://www.youtube.com/@kim3meals/videos
            save_path (str): 모든 동영상들에 대한 columns(vid, 조회수, 업로드 시간)을 담은 df를 저장할 장소

        Returns:
            None
        """
        # target of crawling
        self.driver.get(target_url)

        # 페이지 Open 후 기다리는 시간
        time.sleep(5.0)

        # down the scroll
        _ = self.driver.find_element(By.TAG_NAME, "body")

        _ = self.driver.execute_script("return document.documentElement.scrollHeight")

        # max size 50의 Queue 생성
        # 0.1sec * 50 = 5sec 동안 Scroll 업데이트가 없으면 스크롤 내리기 종료
        szQ = Queue(50)
        enqueue_count = 0

        while True:
            # Scroll 내리기
            self.driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight);"
            )

            # Scroll Height를 가져오는 주기
            time.sleep(0.1)
            new_page_height = self.driver.execute_script(
                "return document.documentElement.scrollHeight"
            )

            # Queue가 꽉 차는 경우 스크롤 내리기 종료
            if enqueue_count > szQ.maxsize:
                break

            # 첫 Loop 수행 (Queue가 비어있는 경우) 예외 처리
            if szQ.isEmpty():
                szQ.enqueue(new_page_height)
                enqueue_count += 1

            # Queue에 가장 먼저 들어온 데이터와 새로 업데이트 된 Scroll Height를 비교함
            # 같으면 그대로 Enqueue, 다르면 Queue의 모든 Data를 Dequeue 후 새로운 Scroll Height를 Enqueue 함.
            else:
                if szQ.peek() == new_page_height:
                    szQ.enqueue(new_page_height)
                    enqueue_count += 1
                else:
                    szQ.enqueue(new_page_height)
                    for z in range(enqueue_count):
                        szQ.dequeue()
                    enqueue_count = 1

        logger.info("all video has scrolled")

        _html = self.driver.page_source
        self.driver.close()
        html = BeautifulSoup(_html, "html.parser")

        # 페이지 내 영상 덩어리별로 findall
        video_htmls = html.findAll(
            "ytd-rich-item-renderer", {"class": "style-scope ytd-rich-grid-row"}
        )
        logger.info(f"len of videos is {len(video_htmls)}")

        video_info = []
        for video_html in video_htmls:
            # youtube 영상 하나의 고유 vid 추출
            video_id = video_html.find("a", {"id": "video-title-link"})["href"]
            video_id = video_id.split("/watch?v=")[-1]

            # 제목 추출
            title = video_html.find("a", {"id": "video-title-link"})["title"]

            # youtube 영상의 메타 데이터 (조회 수, 업로드 시점) 추출
            meta_datas = video_html.find(
                "div", {"class": "style-scope ytd-video-meta-block"}
            ).text.split()
            num_click, uploaded_time = meta_datas[3], " ".join(meta_datas[4:])

            video_info.append(
                {
                    "video_id": video_id,
                    "title": title,
                    "num_click": num_click,
                    "uploaded_time": uploaded_time,
                }
            )

        base_videos_info_df = pd.DataFrame(
            video_info, columns=["video_id", "title", "num_click", "uploaded_time"]
        )
        base_videos_info_df.to_csv(save_path, index=False, encoding="utf-8-sig")
        logger.info(f"file saved at {save_path}")


if __name__ == "__main__":
    crawler = InfinitScrollVideoCrawler()
    crawler(
        target_url="https://www.youtube.com/@kim3meals/videos", save_path="./test.csv"
    )
