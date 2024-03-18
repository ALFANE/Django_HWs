import requests

resonse = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
resonse = resonse.json()
for i in resonse:
    print(i['ccy'])
# print(resonse[0])