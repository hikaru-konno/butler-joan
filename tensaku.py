def set_payload():

  payload = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://img3.imepic.jp/image/20230818/534630.png?4c05787a6db87f6f0f9072f7661be74a",
    "size": "full",
    "aspectRatio": "20:20",
    "aspectMode": "cover"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "お望みの文章をご入力くださいませ",
        "weight": "bold",
        "size": "xl",
        "wrap": True
      },
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": []
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
    "url": "https://img3.imepic.jp/image/20230818/534630.png?4c05787a6db87f6f0f9072f7661be74a",
    "size": "full",
    "aspectRatio": "20:20",
    "aspectMode": "cover"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": []
      },
      {
        "type": "text",
        "text": response,
        "wrap": True
      }
    ]
  }
 }
  return payload