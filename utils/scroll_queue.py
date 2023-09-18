"""
youtube 동영상 페이지 무한 스크롤을 위한 Queue
- 아래로 스크롤 해 더보기를 통해 동적으로 이전 영상들을 불러와야 하는 경우에 사용
- 기본적으로 유튜버가 업로드한 영상이 30개를 넘는 경우 백엔드 크롤링으로 불가능하기에 큐 자료구조를 사용해야 한다.
- 참조: https://manyda.tistory.com/10
"""


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
