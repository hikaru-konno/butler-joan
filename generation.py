def set_payload():

  payload = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://img3.imepic.jp/image/20230824/489870.png?0ef09b91a5d962998cec9d8f0a4effaf",
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
        "text": "作成してほしい問題を教えてください",
        "wrap": True,
        "size": "xl",
        "weight": "bold"
      },
      {
        "type": "text",
        "text": "左下のキーボードから入力できます"
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
    "url": "https://img3.imepic.jp/image/20230824/489870.png?0ef09b91a5d962998cec9d8f0a4effaf",
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