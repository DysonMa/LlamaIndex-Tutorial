from youtube_transcript_api import YouTubeTranscriptApi
from llama_index.readers.youtube_transcript import YoutubeTranscriptReader
from llama_index.core import VectorStoreIndex, Response
from llama_index.core.response.pprint_utils import pprint_response

# Laptop
# "https://www.youtube.com/watch?v=zIwLWfaAg-8"

# Mobile
# https://youtu.be/XuN6sF8UGSw?si=Gt5G8ijyXDbPo2-x

def summarize_youtube(youtube_link: str, llm, embed_model) -> str:
    if not llm or not embed_model:
        raise Exception("No llm orembed_model")

    try:
        # Only works for web link, not mobile link
        ytb_id = youtube_link.split("?v=")[1]
        print(ytb_id)
        
        language_code = ""
        transcript_list = YouTubeTranscriptApi.list_transcripts(ytb_id)
        for transcript in transcript_list:
            language_code = transcript.language_code
        print(language_code)
        
        loader = YoutubeTranscriptReader()
        documents = loader.load_data(
            ytlinks=[youtube_link],
            languages=["zh", "zh-TW", "en", language_code]  # Decreasing priority
        )

        index = VectorStoreIndex.from_documents(
            documents=documents,
            embed_model=embed_model
        )
        query_engine = index.as_query_engine(llm=llm)
        res: Response = query_engine.query("請用繁體中文總結這篇文章的內容，並條列式列出所有重點")
        # pprint_response(res, show_source=True)
        return res.response
    except Exception as e:
        print(e)
        return "Oops...無法總結這篇YouTube影片的內容"
