from llama_index.core.readers.base import BaseReader
from llama_index.core import Document
import json

class BlogExtractor(BaseReader):
    def load_data(self, file, extra_info=None):
        with open(file, "r") as f:
            text = f.read()
        doc_list = map(lambda x:x.strip(), text.split("---"))
        return [Document(text=doc, extra_info=extra_info or {}) for doc in doc_list if doc != ""]

class FaqExtrator(BaseReader):
    def load_data(self, file, extra_info=None):
        with open(file, "r") as f:
            text = f.read()
        qa_list = map(lambda x:x.strip(), text.split("==="))
        return [Document(text=qa, extra_info=extra_info or {}) for qa in qa_list if qa != ""]

class GoogleMapExtrator(BaseReader):
    def load_data(self, file, extra_info=None):
        with open(file, "r") as f:
            feedbacks = json.load(f)
        docs = []
        for each in feedbacks:
            docs.append(Document(text=f"評分：{each['rating']}, 評論：{each['comment']}", extra_info=extra_info or {}))
        return docs