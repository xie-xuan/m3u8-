import requests
import re
from threading import Thread
proxy = {
	'http': '192.168.43.1:7890',
	'https': '192.168.43.1:7890'
}

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537'
}

main_url='https://www.baidu.com'

def proxy_set():
    global proxy
    host=input('请输入代理地址:')
    if host=='':
        proxy=None
    while re.match('((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}',host) ==None:
        print('输入地址不合法,请重新输入')
        host=input('请输入代理地址:')

    port=input('请输入代理端口:')

    while not (int(port)>=0 and int(port) <=65535):
        print('输入端口不合法请重新输入')
        port=input('请输入代理端口:')

    proxy={
        'http'  :host+':'+port,
        'https' :host+':'+port
    }

def url_set():
    global main_url
    main_url=input('请输入视频网址:')

def main():




if __name__=="main":
    main()



