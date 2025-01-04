# Refers: https://docs.llamaindex.ai/en/stable/examples/query_engine/RouterQueryEngine/

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from extractor import BlogExtractor, FaqExtrator, GoogleMapExtrator
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.response.pprint_utils import pprint_response

# LLm and embeddings
llm = Ollama(model="llama3.2:3b", request_timeout=600)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

# Load data
qa_docs = SimpleDirectoryReader(input_files=["./data/faq.qa"], file_extractor={".qa": FaqExtrator()}).load_data()
blog_docs = SimpleDirectoryReader(input_files=["./data/blog.md"], file_extractor={".md": BlogExtractor()}).load_data()
google_map_docs = SimpleDirectoryReader(input_files=["./data/google-map.json"], file_extractor={".json": GoogleMapExtrator()}).load_data()

# Build index
qa_index = VectorStoreIndex.from_documents(
    documents=qa_docs,
    embed_model=embed_model
)
blog_index = SummaryIndex.from_documents(
    documents=blog_docs,
    embed_model=embed_model
)
googlemap_index = SummaryIndex.from_documents(
    documents=google_map_docs,
    embed_model=embed_model
)

# Build query engine
qa_query_engine = qa_index.as_query_engine(llm=llm)
blog_query_engine = blog_index.as_query_engine(llm=llm)
googlemap_query_engine = googlemap_index.as_query_engine(llm=llm)

# Build query tool
faq_tool = QueryEngineTool.from_defaults(
    query_engine=qa_query_engine,
    description=(
        "依據餐廳的FAQ資訊提供解答"
    ),
)
blog_tool = QueryEngineTool.from_defaults(
    query_engine=blog_query_engine,
    description=(
        "針對餐廳的任何網紅或Youtuber撰寫的美食評論及部落格文章"
    ),
)
googlemap_tool = QueryEngineTool.from_defaults(
    query_engine=googlemap_query_engine,
    description=(
        "針對Google Map上的評論與評分"
    ),
)

# Build query router
query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(llm=llm),
    query_engine_tools=[
        faq_tool,
        blog_tool,
        googlemap_tool
    ],
    llm=llm
)

# Test query
queries = [
    "Sandy Hsu 有針對這家餐廳做出什麼評價嗎？他寫了幾篇部落格來記錄呢?分別是什麼時候寫的呢？",
    # "這家餐廳有什麼推薦的招牌料理？",
    # "情人節有什麼優惠活動嗎？",
    # "這家餐廳在Google Map上的評價如何？",
    # "我想要跨年去這家餐廳用餐，我需要注意什麼事項嗎？",
    # "這家店可以訂位嗎？是否有低消？我家的狗狗可以去用餐嗎？另外，我的朋友只能吃素，不知道這家餐廳有沒有素食料理呢",
    # "請幫我找出所有Google Map上低於4分的留言，並總結他們的意見"
]

for i in range(len(queries)):
    res = query_engine.query(queries[i])
    pprint_response(res, show_source=True)
    print("\n\n")


# 1. 自定義解析器，可以解決斷詞的不確定性 (ex: md, qa, json)，即使是json這種資料結構，解析後如何解讀也可以自定義
# 2. Blog 的作者查詢顯示了 SummaryIndex 和 VectorStoreIndex 的差，前者會把所有Nodes丟給 LLM，後者會先用向量搜尋相似的再丟給 LLM
# 3. 透過 Router 自己區分問題的流向