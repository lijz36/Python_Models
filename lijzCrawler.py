from urllib import request, error
from requests import RequestException
import lijzMD5
from lijzLog import *
import requests
import json, re, time, random, os
from selenium import webdriver
from bs4 import BeautifulSoup



UserAgentList = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"
]


def __singletion(cls):
    """
    单例模式的装饰器函数
    :param cls: 实体类
    :return: 返回实体类对象
    """
    instances = {}
    def getInstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getInstance


@__singletion
class C_CrawlerGet(object):
    """
    普通的Get爬虫爬去数据
    """
    def __init__(self, url, pattern):
        self.url = url
        self.pattern = pattern
        self.logger = C_Logger('lijzCrawler', 'lijzCrawler.log', out=1).getLogger()

    def startCrawler(self):
        html = self.__getPage()
        for info in self.__getRealInfo(html):
            self.__writeInfo(info)
            time.sleep(random.randint(1, 5))

    def __getPage(self):
        try:
            # 自定义添加一些请求头信息
            self.headers = {
                'User-Agent': random.choice(UserAgentList),
            }
            response = requests.get(self.url, headers=self.headers)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException as e:
            self.logger.exception(e)
            return None

    def __getRealInfo(self, html):
        regex = re.compile(self.pattern)
        results = re.findall(regex, html)
        for item in results:
            yield {
                'title': item[0].strip(' \n'),
                'star': item[1].strip(' \n'),
                'releasetime': item[2].strip(' \n'),
            }

    def __writeInfo(self, info):
        with open('lijzCrawler.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(info, ensure_ascii=False) + '\n')


@__singletion
class C_ProxyCrawlerGet(object):
    """
    可以使用代理服务器Get进行爬虫数据抓取
     proxy = {"http": "394996257:a1jnn6er@112.74.198.237:16818"}
    """
    def __init__(self, url, pattern, proxy=None, reqnum=5, charset='utf-8'):
        self.url = url
        self.pattern = pattern
        self.proxy = proxy
        self.reqnum = reqnum
        self.charset = charset
        self.logger = C_Logger('lijzProxyCrawler', 'lijzProxyCrawler.log', out=1).getLogger()

    def startCrawler(self):
        self.logger.info("开始爬取数据... ... ...")
        if random.randint(1, 11) < 3:
            self.logger.info("禁用代理服务器爬取数据...")
            self.proxy = None

        proxy_handler = request.ProxyHandler(self.proxy)
        opener = request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', random.choice(UserAgentList))]
        request.install_opener(opener)
        try:
            response = request.urlopen(self.url)
            self.logger.info("爬取数据成功...")
            count = 0
            html = response.read().decode(self.charset)
            for info in self.__getRealInfo(html):
                count += 1
                self.logger.info("写入第 %d 条数据" % count)
                self.__writeInfo(info)
                time.sleep(random.randint(1, 3))
            return True
        except error.HTTPError as e:
            self.logger.error(e)
            self.__againReq(e)
            return False
        except error.URLError as e:
            self.logger.error(e)
            return False

    def __getRealInfo(self, html):
        regex = re.compile(self.pattern)
        results = re.findall(regex, html)
        for item in results:
            yield {
                'title': item[0].strip(' \n'),
                'star': item[1].strip(' \n'),
                'releasetime': item[2].strip(' \n'),
            }

    def __writeInfo(self, info):
        with open('lijzProxyCrawler.txt', 'a', encoding=self.charset) as f:
            f.write(json.dumps(info, ensure_ascii=False) + '\n')

    def __againReq(self, e):
        if self.reqnum > 0:
            self.logger.info("抓取不成功，再次抓取中... ...")
            if hasattr(e, 'code') and 500 <= e.code <= 600:
                time.sleep(random.randint(5, 11))
                self.reqnum -= 1
                self.startCrawler()


@__singletion
class C_SeleniumPhantomJSCrawler(object):
    def __init__(self, url, browserPath, outPath, parser='html5lib'):
        self.url = url
        self.browserPath = browserPath
        self.outPath = outPath
        self.parser = parser
        self.logger = C_Logger('SeleniumPhantomJSCrawler', 'SeleniumPhantomJSCrawler.log', out=1).getLogger()

    def __makeDir(self, path):
        isExists = os.path.exists(path)
        if not isExists:
            try:
                os.makedirs(path)
            except NotImplementedError:
                self.logger.error("makedir %s is Error" % path)
                return False
        return True

    def startCrawler(self):
        self.__makeDir(self.outPath)
        driver = webdriver.Chrome(executable_path=self.browserPath)
        driver.get(self.url)
        bsObj = BeautifulSoup(driver.page_source, self.parser)
        girlsList = driver.find_element_by_id('J_GirlsList').text.split('\n')
        imagesUrl = re.findall('\/\/gtd\.alicdn\.com\/sns_logo.*\.jpg', driver.page_source)
        girlsUrl = bsObj.find_all("a", {"href": re.compile("\/\/.*\.htm\?(userId=)\d*")})
        # 所有妹子的名字地点
        girlsNL = girlsList[::3]
        # 所有妹子的身高体重
        girlsHW = girlsList[1::3]
        # 所有妹子的个人主页地址
        girlsHURL = [('http:' + i['href']) for i in girlsUrl]
        # 所有妹子的封面图片地址
        girlsPhotoURL = [('https:' + i) for i in imagesUrl]
        # 姓名地址 girlNL，        身高体重 girlHW
        # 个人主页地址 girlHRUL,   封面图片 URL
        girlsInfo = zip(girlsNL, girlsHW, girlsHURL, girlsPhotoURL)
        for girlNL, girlHW, girlHURL, girlCover in girlsInfo:
            # 为妹子建立文件夹
            self.__makeDir(self.outPath + girlNL)
            # 获取妹子封面图片
            data = request.urlopen(girlCover).read()
            with open(self.outPath + girlNL + '/cover.jpg', 'wb') as f:
                f.write(data)
            # 获取妹子个人主页中的图片
            self.__getImgs(girlHURL, self.outPath + girlNL)
        driver.close()

    def __getImgs(self,url,  path):
        driver = webdriver.Chrome(executable_path=self.browserPath)
        driver.get(url)
        bsObj = BeautifulSoup(driver.page_source, self.parser)
        imgs = bsObj.find_all("img", {"src": re.compile(".*\.jpg")})
        for i, img in enumerate(imgs[1:]):
            try:
                data = request.urlopen("http:" + img['src']).read()
                names = lijzMD5.md5_uuid()[:9]
                fileName = path + "/" + names + "_" + str(i+1) + ".jpg"
                with open(fileName, 'wb') as f:
                    f.write(data)
            except:
                self.logger.error("请求地址错误！")
        driver.close()


@__singletion
class C_ProxySpider(object):
    def __init__(self, url, fileName, proxy=None, reqnum=5, charset='utf-8'):
        self.url = url
        self.fileName = fileName
        self.proxy = proxy
        self.charset = charset
        self.reqnum = reqnum
        self.spider_queue = []
        self.spidered_queue = []
        self.logger = C_Logger('ProxySpider', 'ProxySpider.log', out=1).getLogger()

    def startSpider(self):
        html = self.__getHtml()
        if html is not None:
            lists = self.__getAllList(html)
            if len(lists) > 0:
                for item in lists:
                    result = self.__getOne(item) + '\n'
                    self.__writeFiles(result);
                self.logger.info("爬取成功：" + self.url)
            else:
                self.logger.error("没有爬取到页面数据：" + self.url)
                return

            pattern = '(https://www.douban.com/doulist/3516235/\?start=.*?)"'
            itemUrls = re.findall(pattern, html)
            self.spidered_queue.append(self.url)
            if len(itemUrls) > 0:
                for itemUrl in itemUrls:
                    if itemUrl not in self.spidered_queue \
                            and itemUrl not in self.spider_queue:
                        self.spider_queue.append(itemUrl)
                while self.spider_queue:
                    self.url = self.spider_queue.pop(0)
                    self.startSpider()
            else:
                self.logger.error("没有更多页面数据了！")
                return
        else:
            self.logger.error("获取页面信息失败")
            return

    def __writeFiles(self, results):
        with open(self.fileName, 'a', encoding=self.charset) as f:
            f.write(results)

    def __getHtml(self):
        html = None
        if random.randint(1, 11) < 3:
            self.proxy = None

        proxy_handler = request.ProxyHandler(self.proxy)
        opener = request.build_opener(proxy_handler)
        opener.addheaders = [('User-Agent', random.choice(UserAgentList))]
        request.install_opener(opener)
        try:
            response = request.urlopen(self.url)
            html = response.read().decode(self.charset)
        except UnicodeError as e:
            self.logger.error(e)
        except error.HTTPError or error.URLError as e:
            self.logger.error(e)
            if self.reqnum > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    self.reqnum -= 1
                    html = self.__getHtml()
        return html

    def __getAllList(self, html):
        soup = BeautifulSoup(html, 'lxml')
        lists = soup.find_all('div', class_='bd doulist-subject')
        return lists

    def __getOne(self, item):
        dic = {}
        soup = BeautifulSoup(str(item), 'lxml')
        titles = soup.find_all('div', class_='title')
        soup_title = BeautifulSoup(str(titles[0]), 'lxml')
        dic['title'] = (soup_title.a.string).strip(' \n')

        nums = soup.find_all('span')
        if len(nums) == 3:
            soup_num = BeautifulSoup(str(nums[2]), 'lxml')
            dic['common'] = soup_num.string[1:-1]
        else:
            dic['common'] = "暂无评价"

        info = soup.find_all('div', class_='abstract')
        if len(info) == 1:
            soup_info = BeautifulSoup(str(info[0]), 'lxml')
            strs = ''
            for item in soup_info.stripped_strings:
                strs += item
            dic['performer'] = strs
        else:
            dic['performer'] = '暂无演员'
        return json.dumps(dic, ensure_ascii=False)



