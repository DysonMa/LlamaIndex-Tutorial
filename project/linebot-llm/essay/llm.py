from llama_index.readers.papers import ArxivReader
from llama_index.core import VectorStoreIndex, Response
from llama_index.core.response.pprint_utils import pprint_response

loader = ArxivReader()

def summarize_essay(query: str, llm, embed_model, max_results=1) -> str:
    if not llm or not embed_model:
        raise Exception("No llm orembed_model")
    try:
        documents = loader.load_data(
            search_query=query,
            max_results=max_results
        )

        if len(documents) == 0:
            return f"Oops...沒有找到任何與'{query}'有關的文章"

        metadata = documents[0].metadata
        title = metadata["Title of this paper"]
        author = metadata["Authors"]
        publish_date = metadata["Date published"]
        url = metadata["URL"]

        index = VectorStoreIndex.from_documents(
            documents=documents,
            embed_model=embed_model
        )
        query_engine = index.as_query_engine(llm=llm)
        res: Response = query_engine.query("請詳細列點解釋文章的各個觀點")
        # pprint_response(res, show_source=True)
        return f"文章標題：{title}\n作者：{author}\n發布時間：{publish_date}\nURL: {url}\n{res}"
    except Exception as e:
        print(e)
        return f"Oops...沒有找到任何與'{query}'有關的文章"