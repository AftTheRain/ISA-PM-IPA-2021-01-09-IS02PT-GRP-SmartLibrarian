from flask import Flask, request, make_response, jsonify
import requests
import json
import pandas as pd
import os

app = Flask(__name__)
## TODO: STEP 1
# APIKEY = "00284a794972b10c05b7275ef5ada115" # Place your API KEY Here...
#"8a81d247d650cb16469c4ba3ceb7d265"

# **********************
# UTIL FUNCTIONS : START
# **********************

# def getjson(url):
#     resp =requests.get(url)
#     return resp.json()
#
# #Information of categories are taking from https://en.wikipedia.org/wiki/Beaufort_scale
# def getWindSpeedCat(windspeed):
#     dir_cur = os.path.dirname(os.path.abspath(__file__))
#     dir_cat = os.path.join(dir_cur, r"wind_cat.csv")
#     wind_cat = pd.read_csv(dir_cat, encoding = "utf-8")
#     for index, row in wind_cat.iterrows():
#         print(float(row["Speed_Min"]))
#         if windspeed >= float(row["Speed_Min"]):
#             category = row["Category"]
#     return category
#
# def getWeatherInfo(location, aspect):
#     API_ENDPOINT = f"http://api.openweathermap.org/data/2.5/weather?APPID={APIKEY}&q={location}"
#     data = getjson(API_ENDPOINT)
#     print(data)
#     try:
#         success = True
#         if aspect == "weather":
#             for item in data["weather"]: description = item["description"]
#             return {"success": success, "description": description}
#         elif aspect == "temperature":
#             temp = round(data["main"]["temp"]/10, 1)
#             return {"success": success, "temp": temp}
#         elif aspect == "windspeed":
#             windSpeed = data["wind"]["speed"]
#             category = getWindSpeedCat(float(windSpeed))
#             return {"success": success, "windSpeed": windSpeed, "category": category}
#     except:
#         success = False
#         message = data["message"]
#         return {"success": success, "message": message}

# **********************
# UTIL FUNCTIONS : END
# **********************

# *****************************
# Intent Handlers funcs : START
# *****************************

# def getWeatherIntentHandler(location):
#     """
#     Get location parameter from dialogflow and call the util function `getWeatherInfo` to get weather info
#     """
#     info = getWeatherInfo(location, "weather")
#     print(info)
#     if info["success"] == True:
#         description = info["description"]
#         return f"Currently, it is {description} in {location}"
#     else:
#         message = info["message"]
#         return f"Sorry, {message}"
#
# def getTempIntentHandler(location):
#     """
#     Get location parameter from dialogflow and call the util function `getWeatherInfo` to get temperature info
#     """
#     info = getWeatherInfo(location, "temperature")
#     print(info)
#     if info["success"] == True:
#         temp = info["temp"]
#         return f"The current temperature in {location} is {temp}"
#     else:
#         message = info["message"]
#         return f"Sorry, {message}"
#
# def getWindSpeedIntentHandler(location):
#     """
#     Get location parameter from dialogflow and call the util function `getWeatherInfo` to get wind speed info
#     """
#     info = getWeatherInfo(location, "windspeed")
#     print(info)
#     if info["success"] == True:
#         windspeed = info["windSpeed"]
#         windcat = info["category"]
#         return f"Currently, in {location}, there is {windcat} with wind speed of {windspeed} m/s"
#     else:
#         message = info["message"]
#         return f"Sorry, {message}"

# ***************************
# Intent Handlers funcs : END
# ***************************


# *****************************
# WEBHOOK MAIN ENDPOINT : START
# *****************************
@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(req)
    intent_name = req["queryResult"]["intent"]["displayName"]

    resp_text = "Unable to find a matching intent. Try again."
    if intent_name == "GetBookTitleIntent":
        bookTitle = req["queryResult"]["parameters"]["book-title"]
        resp_text = "Looking for " + bookTitle
    else:
        resp_text = "Unable to find a matching intent. Try again."

    return make_response(jsonify({'fulfillmentText': resp_text}))

# ***************************
# WEBHOOK MAIN ENDPOINT : END
# ***************************

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)
