import openai
import json
import weather

openai.api_key = ''

#ユーザー入力
#user_prompt = input()

def situziGPTv2(new_message_text:str, past_messages:list = []):

    new_past_messages = []
    for s in past_messages:
        new_past_messages.append({"role": "user", "content": s})
    past_messages = new_past_messages

    if len(past_messages) == 0:
        system = {"role": "system", "content": "貴方は優秀でエレガントな執事です。"}
        past_messages.append(system)
    new_message = {"role": "user", "content": new_message_text}
    past_messages.append(new_message)

    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=past_messages
    )
    response_message = {"role": "assistant", "content": result.choices[0].message.content}
    past_messages.append(response_message)
    response_message_text = result.choices[0].message.content
    return response_message_text, past_messages

def getWeatherInfo(reply):
    city, weth, max_temp, min_temp, icon, current = weather.weather_function(reply) 
    new_response, past_messages = situziGPTv2("次の気象情報について、簡潔に教えてください。またその気象情報について簡潔にアドバイスをしてください。都市名:" + city + "、天気：" + weth + "、最高気温：" + max_temp+ "、最低気温：" + min_temp+"、現在気温："+current, [])
    
    return new_response


def getFuncInfo(prompt):
    prompt_test = "天気を調べる"
    response = openai.ChatCompletion.create( 
    model = "gpt-3.5-turbo-0613", 
    messages=[ 
        {"role": "user", "content": prompt}, 
    ], 
    functions = [
        {   "name":"weather_function", 
            "description": prompt_test, 
            "parameters": { 
                 "type": "object", 
                 "properties": { 
            # 引数についての情報を記載する 
                    "location": { 
                    "type": "string", 
                    "description": "京都", 
                    }, 
                }, 
                "required": ["location"],
            }, 
        } 
    ] , 

    function_call="auto"

    ) 
    message = response["choices"][0]["message"]
    function_name = response["choices"][0]["message"]["function_call"]["name"]
    arguments = response["choices"][0]["message"]["function_call"]["arguments"]

    print("arg:", arguments)

    # 関数を実行 
    function_response = weather.weather_function( 
        location=arguments) 
    
    second_response = openai.ChatCompletion.create( 
    model="gpt-3.5-turbo-0613", 
    messages=[ 
    {"role": "user", "content": prompt}, 
    message, 
    { 
    "role": "function", 
    "name": function_name, 
    "content": function_response, 
    } 
    ] 
    ) 
    print("関数実行終了")
    return second_response.choices[0]["message"]["content"]

def situziGPT(prompt):
    
    #応答してもらう処理
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {'role': 'system', 'content': 'あなたは優秀でエレガントな執事です。'},
            {'role': 'user', 'content': prompt}
        ]

    )


    #応答テキストを引っ張り出す
    chat_response = response.choices[0].message.content
    
    #chat_response = conversation.predict(input=prompt)
    return chat_response

#print(situziGPT(user_prompt))


