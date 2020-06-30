import requests


def send(mobile, captcha):
    url = "http://v.juhe.cn/sms/send"
    params = {
        'mobile': mobile,
        'tpl_id': '214383',
        'tpl_value': '#code#=' + captcha,
        'key': 'ed7c428f0eaa511b2a2cb3d9fcf5f574',
    }

    response = requests.get(url, params=params)
    result = response.json()
    print(result)
    if result['error_code'] == 0:
        return True
    else:
        return False