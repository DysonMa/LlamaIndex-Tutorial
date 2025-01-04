from fastapi import FastAPI, Request
import uvicorn
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

line_channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
line_reply_endpoint = "https://api.line.me/v2/bot/message/reply"
app = FastAPI()

@app.post("/webhook")
async def handle_webhook(request: Request):
    # Part1
    # payload = await request.json()

    # {
    #     "destination": "Uad7f0e5f912726628b4d1eebfa6fadca",
    #     "events": [
    #         {
    #             "type": "message",
    #             "message": {
    #                 "type": "text",
    #                 "id": "540729090534277289",
    #                 "quoteToken": "SrWP8Y7PJX5ndBbYwxGm8AWjoP8Mskk0Jch-EZcFaZjBgdX9KRWe1x6tEB0uSNZKaqKfpdlyQ4tfY4WiJXQLFaGEmIOUrXO2u_5YkzMW9tVt6EZ4LTfr6RBq6TV6dcO9C2mr1OntVb3XkHq6y_NaFA",
    #                 "text": "聖誕節"
    #             },
    #             "webhookEventId": "01JFYXTJEWGB1YRG4QV32FQ692",
    #             "deliveryContext": {
    #                 "isRedelivery": false
    #             },
    #             "timestamp": 1735130957795,
    #             "source": {
    #                 "type": "group",
    #                 "groupId": "C116cc3f864e1e9d03093234eaaabccbe",
    #                 "userId": "Ue53a6a75366daefae624d29862cede85"
    #             },
    #             "replyToken": "0a49db55a9d24cbea5c442cc2c3c38c5",
    #             "mode": "active"
    #         }
    #     ]
    # }
    
    # print(f"Received webhook data: {payload}")
    # return {"message": "Webhook received successfully"}

    # Part2
    payload = await request.json()
    event = payload["events"][0]
    reply_token = event["replyToken"]
    message = event["message"]["text"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {line_channel_access_token}"
    }
    data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": f"重複一次：{message}",
            }
        ]
    }
    requests.post(line_reply_endpoint, headers=headers, data=json.dumps(data))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)