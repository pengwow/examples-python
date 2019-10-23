# coding=utf-8
import requests
import time

def main():
    url = 'https://shanghaicity.openservice.kankanews.com/public/bus/Getstop'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {"stoptype": 0,
            "stopid": "1.",
            "sid": "de82841bae84af0e7df130cc51bb417d"}
    while True:
        result = requests.post(url, data=data,headers=headers)
        result = result.json()
        if not result.get('error'):
            print("1111111111111111")
        else:
            print("未发车！%s" % str(result))
        time.sleep(1)


if __name__ == '__main__':
    main()
