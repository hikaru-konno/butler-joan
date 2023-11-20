import json
import database as db
import requests

API_KEY = "ee0a56f0fa76674256d39d2b7962abdf" # xxxに自分のAPI Keyを入力。
baseUrl = "http://api.openweathermap.org/data/2.5/weather?"


# def set_payload():

def set_payload():

  payload = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://www.illust-box.jp/db_img/sozai/00006/62580/watermark.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "text",
        "text": "都市を入力してくださいませ",
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

def temp_payload(response):
  payload = {
    "type": "bubble",
    "hero": {
      "type": "image",
      "url": "https://illust8.com/wp-content/uploads/2018/08/weather_sun_solar_illust_1081.png",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover",
      "action": {
        "type": "uri",
        "uri": "https://linecorp.com"
      }
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "spacing": "md",
      "action": {
        "type": "uri",
        "uri": "https://linecorp.com"
      },
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

def set_payload_answer(info, icon):
  payload = {
    "type": "bubble",
    "hero": {
      "type": "image",
      "url": "https://openweathermap.org/img/wn/" + icon + "@2x.png",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover",
      "action": {
        "type": "uri",
        "uri": "https://linecorp.com"
      }
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "spacing": "md",
      "action": {
        "type": "uri",
        "uri": "https://linecorp.com"
      },
      "contents": [
        {
          "type": "text",
          "text": info,
          "wrap": True
        }
      ]
    }
  }
  return payload

def set_payload_answer2(reply,info):
  city, weat, temp_max, temp_min, icon, current=  weather_function(reply)
  print(city,temp_max,temp_min,current,weat,icon)

  if city == "none":
    payload = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://www.illust-box.jp/db_img/sozai/00006/62580/watermark.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "text",
        "text": "都市が見つかりませんでした。",
        "size": "xl",
        "weight": "bold"
      },
      {
        "type": "text",
        "text": "別の都市をお試しください。", "wrap": True
      }
    ]
  }
}
    return payload


  payload = {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "image",
          "url": "https://openweathermap.org/img/wn/" + icon + "@2x.png",
          "size": "full",
          "aspectMode": "cover",
          "position": "absolute",
          "offsetTop": "40px",
          "offsetStart": "none"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "text",
              "text": city,
              "size": "30px",
              "color": "#000000",
              "wrap": True
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "🌡最高："+ temp_max +"℃"
                },
                {
                  "type": "text",
                  "text": "🌡最低："+ temp_min +"℃"
                },
                {
                  "type": "text",
                  "text": "🌡現在："+ current +"℃"
                }
              ]
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "text",
              "text": weat,
              "size": "20px"
            }
          ]
        }
      ],
      "height": "300px"
    },
    "footer": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": info,
          "color": "#ffffff",
          "wrap": True
        }
      ],
      "background": {
        "type": "linearGradient",
        "angle": "0deg",
        "startColor": "#000000",
        "endColor": "#000000"
      }
    }
  }
  return payload




def find_city(location, list):
  print(location)
  for idx, name in enumerate(list):
    if name.find(location) != -1 or location.find(name) != -1:
      print("find:", name)
      return idx

def weather_function(city_input):
  
  try:
    # アルファベットで都市名の名前を入力
    cityName = db.city[find_city(city_input, db.city_jp)]
  except:
    return "none", "none", "none", "none", "none", "none"
  print("cityjp:", db.city[find_city(city_input, db.city_jp)])
  # URL作成
  completeUrl = baseUrl + "appid=" + API_KEY + "&q=" + cityName 

  # レスポンス
  response = requests.get(completeUrl) 

  # レスポンスの内容をJSONフォーマットからPythonフォーマットに変換
  cityData = response.json() 
  #print(cityData)

# Codが404だと都市名が見つかりませんの意味
#def weather_function(location):
  if cityData["cod"] != "404":
    print("都市名==>",   cityData["name"])
    print("天気==>",db.weather[cityData["weather"][0]["description"]]["日本語表記"])
    print("現在の気温==>",cityData["main"]["temp"] - 273.15,"℃")
    print("最高気温==>",cityData["main"]["temp_max"] - 273.15,"℃")
    print("最低気温==>",cityData["main"]["temp_min"] - 273.15,"℃")
    print("湿度==>",cityData["main"]["humidity"])
    print("気圧==>",cityData["main"]["pressure"])
    print("湿度==>",cityData["main"]["humidity"])
    print("風速==>",cityData["wind"]["speed"])
    weather =  cityData["weather"][0]["description"]
    temp = cityData["main"]["temp"] - 273.15,"℃"

    weather_ans = weather #, "気温":temp}]
  else: 
	#print("都市名がみつかりませんでした。")
    wweather_anseather_ans = "都市名がみつかりませんでした。"
    return 
  #返り値
  #日本語の都市名・天気・最高気温・最低気温
  return db.city_jp[find_city(city_input, db.city_jp)], db.weather[cityData["weather"][0]["description"]]["日本語表記"], str(round(cityData["main"]["temp_max"] - 273.15,2)), str(round(cityData["main"]["temp_min"] - 273.15,2)), db.weather[cityData["weather"][0]["description"]]["Icon"][0],str(round(cityData["main"]["temp"] - 273.15,2))
