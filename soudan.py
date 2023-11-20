
def set_payload():

  payload = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://img3.imepic.jp/image/20230823/516460.png?96a5a4ffd2387ca83237b73c704394a9",
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
        "text": "相談を入力してください",
        "size": "xl",
        "weight": "bold"
      },
      {
        "type": "text",
        "text": "左下のキーボードから入力できます。5分経っても表示されない場合は再度試してください。", "wrap": True
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
    "url": "https://img3.imepic.jp/image/20230823/516460.png?96a5a4ffd2387ca83237b73c704394a9",
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