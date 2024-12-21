import requests

# 定义请求的 URL
url = "http://airquality.icu/register"

# 定义要发送的数据
data = {
    "username": "asbasc",
    "password": "123521",
    "rember": "15"
}

# 发送 POST 请求
response = requests.post(url, json=data)

# 打印响应状态码和内容
print("Status Code:", response.status_code)
print("Response Body:", response.text)
