"""
Author: zed.ai
Reviewer:
2023.11.26
"""
from glob import glob

import firebase_admin
from firebase_admin import credentials, firestore


class Database:
    """
    Firstore로 DB를 구성하고 nosql 형태의 db를 다룬다.
    주로 크롤링한 데이터를 db에 업로드하는 과정을 처리한다.
    """

    def __init__(self, config_path: str = "./config"):
        file_path = glob(f"{config_path}/foodmap*.json")[0]

        if not firebase_admin._apps:
            cred = credentials.Certificate(file_path)
            self.app = firebase_admin.initialize_app(cred)

        self.db_client = firestore.client()

    def update(
        self,
        document: str,
        values: dict,
        collection: str = "foodmap",
    ):
        """
        nosql 형태의 Firestore에 데이터를 추가한다.
        add는 document 자체를 갈아끼우므로 update method를 이용한다.

        Examples::
            foodmap(collection) - tag2mark(document)의 값을 추가한다.

        Args:
            document (str): 문서 (loc2info | tag2mark | ...)
            values (dict): key: value 형태의 모든 값
            collection (str): project name foodmap

        Returns:
            None

        """
        doc = self.db_client.collection(collection).document(document)

        try:
            doc.update(values)
        except Exception as e:
            print(f"{document}에 값 {values}를 업로드 하는 과정에서 {e}에러가 발생하였습니다.")


if __name__ == "__main__":
    db = Database()
    db.update(document="tag2mark", values={"te": "test"})
