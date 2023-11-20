# coding:utf-8

import requests
import time

def search_gradients(keyword):
    # 楽天商品検索API (BooksGenre/Search/)のURL
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"

    # URLのパラメータ
    param = {
    "applicationId" : "1061215062415058415",
    "keyword" : keyword,
    "format" : "json"
    }

    # APIを実行して結果を取得する
    result = requests.get(url, param)
    # jsonにデコードして出力する
    json_result = result.json()
    # 整形した結果を格納する辞書型変数を宣言
    price = ""
    url = ""
    name = ""
    icon = ""

    # 取得結果を取り出す
    try:
        item = json_result["Items"][0]["Item"]
    except:
        item = f"{keyword}は検索に失敗しました。"
        name = item
        price = ""
        url = ""
        icon = ""
        return name, price, url, icon
    name = item["itemName"]
    # keyに「商品名（itemName）」、valueに「値段（itemPrice）」を設定する
    price = item["itemPrice"]
    url = item["itemUrl"]
    icon = item["mediumImageUrls"][0]["imageUrl"]

    # 整形した結果を1件ずつ出力する
    print(keyword, name, price, "円")
    print("URL:", url)
    #返り値
    #・商品の名前
    #・商品の値段
    #・商品のURL
    return name, price, url, icon


import openai
openai.api_key = ''
def get_gradients(prompt):
    
    #応答してもらう処理
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {'role': 'user', 'content': "Aは、Bから構成されるものです。以下のAとBのやり取りを踏まえ、Bを出力してください。\nA:ハンバーグ\nB:挽き肉、たまねぎ、パン粉、卵、塩、こしょう、油\nA:シチュー\nB:シチュークリーム、鶏肉、玉ねぎ、じゃがいも、にんじん、サラダ油、水、牛乳\nA:ポテトサラダ\nB:じゃがいも、玉ねぎ、きゅうり、にんじん、ハム、マヨネーズ、塩、こしょう\nA:チャーハン\nB:米、卵、長ネギ、サラダ油、醤油、塩、こしょう\nA:餃子\nB:キャベツ、塩、長ネギ、生姜、にら、豚挽き肉、醤油、ごま油、こしょう、餃子の皮、サラダ油、ごま油\nA:カジュアル系\nB:Tシャツ、デニム、キャップ、ボーダー、スニーカー\nA:キレイ系\nB:ジャケット、スラックス、ミモレ丈スカート、革靴、パンプス\nA:コンサバ系\nB:シャツ、ホワイトパンツ、トレンチコート、ベージュ\nA:フェミニン系\nB:ブラウス、シフォンスカート、花柄、ジレ、ロングカーディガン\nA:ストリート系\nB:キャップ、スウェット、ワイドパンツ、スポーツブランド\nA:" + prompt}
        ]
    )

    #応答テキストを引っ張り出す
    chat_response = response.choices[0].message.content
    print("chat_response:", chat_response)
    chat_response = chat_response.replace('B', "")
    chat_response = chat_response.replace(":", "")
    ret = chat_response.split('、')
    #chat_response = conversation.predict(input=prompt)
    return ret

def main():
    prompt = "シチュー"
    gradients = get_gradients(prompt)
    for g in gradients:
        search_gradients(g)
        time.sleep(1)
        print("---------------------------------------")

def set_payload():

  payload = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://img3.imepic.jp/image/20230823/492510.png?4f4cc730107974fe9f15681d09b56609",
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
        "text": "作りたいものを入力してください(料理名やファッションコーデなど)。その素材を提案いたします。",
        "size": "xl",
        "weight": "bold",
        "wrap" : True
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

def add_bubble_to_contents(payload, name, price, url, icon):

    bubble = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://img3.imepic.jp/image/20230823/492510.png?4f4cc730107974fe9f15681d09b56609",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": name,
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold",
                    "wrap": True
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": price,
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0
                  }
                ],
                "spacing": "lg"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "icon",
                        "url": url
                      },
                      {
                        "type": "text",
                        "text": "商品のリンクへ飛ぶ",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xxl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": url
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          }
        ],
        "paddingAll": "0px"
      }
    }

    payload["contents"].append(bubble)
    return payload


def set_payload_answer(reply, response, names, prices, urls, icons):

    page1 = {"type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://img3.imepic.jp/image/20230823/492510.png?4f4cc730107974fe9f15681d09b56609",
    "size": "full",
    "aspectRatio": "20:30",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": reply,
        "weight": "bold",
        "size": "25px"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "テスト",
                "wrap": True
              }
            ]
          }
        ]
      }
    ]
  }
}
    idx = 0
    payload = {"type": "carousel", "contents": []}
    payload["contents"].append(page1)
    for name in names:
        print(name, "のpayloadを作成中")
        print("[payload]\n", payload)
        print("[name]\n", name)
        print("[price]\n", prices[idx])
        print("[url]\n", urls[idx])
        print("[icons]\n", icons[idx])
        #payload = add_bubble_to_contents(payload, name, prices[idx], urls[idx], icons[idx])
        idx += 1
    return payload