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

url='https://www.baidu.com'
main_url=''



class DownloadTask(Thread):
    def __init__(self,list_o):
        super().__init__()
        self.list=list_o

    def run(self):
        for i in self.list:   #设置任务片
            url=main_url+'/'+i
            download_start(url,'./videos/'+i)

def INIT_go(process,list_o): #线程数，任务数
    task=len(list_o)
    if process=='':
        process=25
    else:
        process=int(process)
    num=task//process
    
    l=['a0']
    for i in range(1,process+1):
       l.append('a'+str(i))
    
    for i in range(process):
        l[i]=DownloadTask(list_o[i*num:(i+1)*num])
        l[i].start()
    l[process]=DownloadTask(list_o[num*process:task-1])
    l[process].start()

    for i in range(process+1):
        l[i].join()

class download_toolkit():
    def __init__(self,url):
        self.url     =  url 
    def m3u8_url(self):
        r = requests.get(url=self.url,headers=headers,proxies=proxy,timeout=5)
        r.encoding=('utf-8')
        url=re.findall(r'https.*.m3u8',r.text)
        try:
            t=str(url[0]).replace('\\','')
        except IndexError:
            print('对不起没有找到m3u8链接，或许对该网站不支持')
            return 0
        else:
             return t

    def main(self):
        url=self.m3u8_url()
        main_url=re.findall('http.+(?=/{1}.+m3u8)',url)
        main_url=main_url[0]
        r = requests.get(url=url,headers=headers,proxies=proxy,timeout=5)
        r.encoding=('utf-8')
        key=re.findall(r'(?<=URI=").*ts',r.text)
        try:
            key=str(key[0]).replace('\\','')
        except IndexError:
            print('该网站视频未加密,或未能找到密钥')
            return 0
        vi =re.findall(r'(?<=IV).*',r.text)
        vi =str(vi[0]).replace('=0x','')
        r=requests.get(url=main_url+'/'+key,headers=headers,proxies=proxy,timeout=5)
        key_v=r.content.hex()
        org={
            'main_url':main_url,
            'vi':vi,
            'key':key_v
        }
        return org
    def download_url(self):
        r=requests.get(url=self.m3u8_url(),headers=headers,proxies=proxy)
        t=r.text
        u=re.findall('\d+.ts',t)
        i=re.findall('\d+.ts',self.main().get('key'))
        try:
            for o in i:
                u.remove(o) 
        except ValueError:
            None
        return u

def download_start(url,f_name):   #下载函数
    i=0
    while i<5:
        try:
            r = requests.get(url=url,headers=headers,proxies=proxy,timeout=3)

        except requests.exceptions.ProxyError:
            i+=1
        else:
            with open(f_name,'wb') as fp:
                fp.write(r.content)
                print(f_name+' is download success! @_0_@')
            break

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
    global url
    url=input('请输入视频网址:')

def main():
    global main_url
    proxy_set()
    url_set()
    a1=input('请输入线程数(默认为25): ')
    a=download_toolkit(url)
    t=a.main()
    main_url=t.get('main_url')
    INIT_go(a1,a.download_url())
    print(t)





if __name__=="__main__":
    main()





