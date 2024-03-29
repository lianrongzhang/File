import requests
import json
import time
import schedule

apiKey = "645ecd741073d157ee4d5c8d211bbede"
lineToken = "BkBG7w8QJgKjvPaUIGaoxhNIqNAalpzOp9KzXOQNu1f"


def getData(key):
    url = (
        "https://api.openweathermap.org/data/2.5/weather?id=1668338&units=imperial&appid="
        + key
    )

    r = requests.get(url)
    data = json.loads(r.text)

    def tempToC(fTemp):
        return round((fTemp - 32) * 5 / 9, 1)

    now_temp = tempToC(data["main"]["temp"])
    feels_like = tempToC(data["main"]["feels_like"])
    temp_max = tempToC(data["main"]["temp_max"])
    temp_min = tempToC(data["main"]["temp_min"])
    temp = f"{data['name']} \n當前氣溫 {now_temp} \n體感溫度 {feels_like}\n最高溫 {temp_max}\n最低溫 {temp_min}"

    return temp


temp = getData(apiKey)


def sendToLine(token):
    url = "https://notify-api.line.me/api/notify"
    payload = {"message": {temp}}
    headers = {"Authorization": "Bearer " + lineToken}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

schedule.every(10).seconds.do(sendToLine, (lineToken))
