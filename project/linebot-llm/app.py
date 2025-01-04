from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import uvicorn
import asyncio
from dotenv import load_dotenv
from linebot import LineBot
from restaurant.llm import get_restaurant_info
from ytranscript.llm import summarize_youtube
from essay.llm import summarize_essay

load_dotenv()

llm = Ollama(model="llama3.2:3b", request_timeout=600)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
app = FastAPI()
linebot = LineBot()

# Store each user's current selected topic (ex: essay, youtube, restaurant)
lock = asyncio.Lock()
user_topics = {}

@app.get("/users")
async def get_user_topics():
    async with lock:
        return JSONResponse(
            content=user_topics,
            status_code=200
        )

@app.post("/webhook")
async def callback(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Line-Signature")

    try:
        payload = linebot.extract_message(signature=signature, body=body)
        print(payload)

        user_id = payload['user_id']
        group_id = payload['group_id']  # If comes from personal chat, this will be empty string
        message = payload['message']
        reply_token = payload["reply_token"]

        # Update users when user select different topic
        topic = None
        res = ""
        await lock.acquire()
        if message == "essay":
            user_topics[user_id] = "essay"
            res = "請提供論文關鍵字:"
        elif message == "youtube":
            user_topics[user_id] = "youtube"
            res = "請提供YouTube網頁連結:"
        elif message == "restaurant":
            user_topics[user_id] = "restaurant"
            res = "你想問什麼餐廳資訊呢？"
        else:
            if user_id in user_topics:
                topic = user_topics[user_id]
                del user_topics[user_id]
        lock.release()

        # Ask LLM to answer user's question
        if topic == "essay":
            res = summarize_essay(query=message, llm=llm, embed_model=embed_model)
        elif topic == "youtube":
            res = summarize_youtube(youtube_link=message, llm=llm, embed_model=embed_model)
        elif topic == "restaurant":
            res = get_restaurant_info(query=message, llm=llm, embed_model=embed_model)

        if res:
            linebot.reply_message(reply_token=reply_token, message=res)
            
        return Response(content="OK", status_code=status.HTTP_200_OK)
   
    except Exception as e:
        print(f"Error handling webhook from linebot: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)