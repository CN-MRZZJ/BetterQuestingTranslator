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
    
    try:
        response = requests.post(url, data=json_data, headers=headers)
        ret = json.loads(str(response.content, encoding='utf-8'))
        if ret['code'] == 200:
            return ret['data']
        else:
            raise Exception("API Error")
    except Exception:
        raise Exception("API Error")
# if __name__ == "__main__":
#     translate('Test','','','http://10.0.2.1:1188/translate')