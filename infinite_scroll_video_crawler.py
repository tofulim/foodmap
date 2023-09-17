import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# TODO: 무한 스크롤 큐를 utils로 빼고 클래스화해야함
# Queue의 기본적인 기능 구현
class Queue:
    def __init__(self, maxsize):
        self.queue = []
        self.maxsize = maxsize

    # Queue에 Data 넣음
    def enqueue(self, data):
        self.queue.append(data)

    # Queue에 가장 먼저 들어온 Data 내보냄
    def dequeue(self):
        dequeue_object = None
        if self.isEmpty():
            print("Queue is Empty")
        else:
            dequeue_object = self.queue[0]
            self.queue = self.queue[1:]
        return dequeue_object

    # Queue에 가장 먼저들어온 Data return
    def peek(self):
        peek_object = None
        if self.isEmpty():
            print("Queue is Empty")
        else:
            peek_object = self.queue[0]
        return peek_object

    # Queue가 비어있는지 확인
    def isEmpty(self):
        is_empty = False
        if len(self.queue) == 0:
            is_empty = True
        return is_empty

    # Queue의 Size가 Max Size를 초과하는지 확인
    def isMaxSizeOver(self):
        queue_size = len(self.queue)
        if queue_size > self.maxsize:
            return False
        else:
            return True


if __name__ == "__main__":
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
    driver = webdriver.Chrome(service=service, options=options)

    # target of crawling
    driver.get("https://www.youtube.com/@kim3meals/videos")

    # 페이지 Open 후 기다리는 시간
    time.sleep(5.0)

    # down the scroll
    body = driver.find_element(By.TAG_NAME, "body")

    last_page_height = driver.execute_script(
        "return document.documentElement.scrollHeight"
    )

    # max size 50의 Queue 생성
    # 0.1sec * 50 = 5sec 동안 Scroll 업데이트가 없으면 스크롤 내리기 종료
    szQ = Queue(50)
    enqueue_count = 0

    while True:
        # Scroll 내리기
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);"
        )

        # Scroll Height를 가져오는 주기
        time.sleep(0.1)
        new_page_height = driver.execute_script(
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

    print("all video has scrolled")

    _html = driver.page_source
    driver.close()
    html = BeautifulSoup(_html, "html.parser")

    # 페이지 내 영상 덩어리별로 findall
    video_htmls = html.findAll(
        "ytd-rich-item-renderer", {"class": "style-scope ytd-rich-grid-row"}
    )
    print(f"len of videos is {len(video_htmls)}")

    video_info = []
    for video_html in video_htmls:
        # youtube 영상 하나의 고유 vid 추출
        video_id = video_html.find("a", {"id": "thumbnail"})["href"]
        video_id = video_id.split("/watch?v=")[-1]

        # youtube 영상의 메타 데이터 (조회 수, 업로드 시점) 추출
        meta_datas = video_html.find(
            "div", {"class": "style-scope ytd-video-meta-block"}
        ).text.split()
        num_click, uploaded_time = meta_datas[3], " ".join(meta_datas[4:])

        video_info.append(
            {
                "video_id": video_id,
                "num_click": num_click,
                "uploaded_time": uploaded_time,
            }
        )

    base_videos_info_df = pd.DataFrame(
        video_info, columns=["video_id", "num_click", "uploaded_time"]
    )
    base_videos_info_df.to_csv(
        "./base_video_info_kim3meals.csv", index=False, encoding="utf-8-sig"
    )
