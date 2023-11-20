def set_payload():

  payload = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://img3.imepic.jp/image/20230823/521630.png?0b3edc55959f5a695db21d343b1977d7",
    "size": "full",
    "aspectRatio": "20:20",
    "aspectMode": "cover"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "text",
        "text": "作詞に必要なキーワードを入力してください",
        "wrap": True,
        "size": "xl",
        "weight": "bold"
      },
      {
        "type": "text",
        "text": "左下のキーボードから入力できます。5分経っても表示されない場合は再度試してください。",
        "wrap": True
      }
    ]
  }
}
  return payload

def set_payload_answer(response):
  payload = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://img3.imepic.jp/image/20230823/521630.png?0b3edc55959f5a695db21d343b1977d7",
    "size": "full",
    "aspectRatio": "20:20",
    "aspectMode": "cover"
    },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "text",
        "text": response,
        "wrap": True
      }
    ]
  }
}
  return payload