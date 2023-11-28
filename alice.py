import requests
from bs4 import BeautifulSoup

class chatbot():
    def __init__(self,botcust:str=None):
        if botcust is None:
            self.botcust=self.start()
        else:
            self.botcust=botcust
        
    def start(self):
        headers = {
            'Host': 'www.pandorabots.com',
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        }

        params = (
            ('botid', 'b8d616e35e36e881'),
            )

        response = requests.get('https://www.pandorabots.com/pandora/talk', headers=headers, params=params)
        botcust=response.headers['set-cookie']
        botcust=botcust[0: botcust.index(";")][9:]
        return botcust
    
    def text(self,msg):
        cookies = {
            'botcust2': self.botcust,
            }

        headers = {
            'Host': 'www.pandorabots.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'origin': 'https://www.pandorabots.com',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.pandorabots.com/pandora/talk?botid=b8d616e35e36e881',
            'accept-language': 'en-US,en;q=0.9',
                }
        
        params = (
            ('botid', 'b8d616e35e36e881'),
            )
        
        data = f'botcust2={self.botcust}&message={msg}'
        data=data.encode('utf-8')
        response = requests.post('https://www.pandorabots.com/pandora/talk', headers=headers, params=params, cookies=cookies, data=data)
        soup = BeautifulSoup(response.text,'html.parser')
        tag = soup.body
        count=0
        resp='meow'
        for string in tag.strings:
            if count==8:
                resp=string[1:]
                break
            count+=1
        return resp