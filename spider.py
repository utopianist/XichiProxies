import requests
import csv
import re

def getHTML(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return (r.text)
    except:
        return ""


def parseHTML(html, pxyList):
    pattern = re.compile('<tr class=".*?">.*?<td.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>', re.S)
    data = re.findall(pattern, html)
    for item in data:
        pxyURL = "http://{0}:{1}".format(item[0], item[1])
        pxyList.append(pxyURL)

def testPxy(pxyList):
    pxy = [] #用于存放真正可用的代理
    url = 'https://www.baidu.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    for item in pxyList:
        try:
            print("正在测试",item)
            proxies = {
                "https": item,  # "https"的代理速度较慢
                'http': item
            }
            r = requests.get(url, headers=headers, proxies=proxies, timeout=30)
            if r.status_code == 200:
                pxy.append(item)
        except:
            print( "代理无效", item)
    with open('xichiProxies.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(pxy)


def main():
    pxyList = []
    offset = 10  #爬取西刺高匿代理前十页
    for i in range(offset):
        xcURL = 'http://www.xicidaili.com/nn/' + str(i+1)
        html = getHTML(xcURL)
        parseHTML(html, pxyList)
        print(pxyList)
        testPxy(pxyList)

main()


