import json

import requests


def translate(text,key,secret,url):
    data = {
        "text": text,
        "source_lang": "EN",
        "target_lang": "ZH"
    }

    headers = {'Content-Type': 'application/json', 'Authorization': key}
    json_data = json.dumps(data)

    response = requests.post(url, data=json_data, headers=headers)
    ret = json.loads(str(response.content, encoding='utf-8'))
    # ret = json.loads(str(response.content))
    # print(ret)
    if ret['code'] == 200:
        return ret['data']
    else:
        return "API错误，错误代码" + ret['code']
# if __name__ == "__main__":
#     translate('Test','','','http://10.0.2.1:1188/translate')