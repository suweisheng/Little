# encoding: utf8

import urllib2
import urllib
import cookielib
import ssl
import requests
import json

# urllib2.urlopen(url[, data[, timeout[, cafile[, capath[, cadefault[, context]]]]])
# url: 可以接收一个url字符串或Request对象
# data: 指定要发送到服务器的附加数据的字符串, 如果参数有值此时 http 请求从GET转为POST, 相关urllib.urlencode
# timeout: 阻塞最长时间

# 注意：httpbin.org 这个网站能测试 HTTP 请求和响应的各种信息，比如 cookie、IP、headers 和登录验证等，且支持 GET、POST 等多种方法，对 Web 开发和测试很有帮助

# ======== 构建请求头
headers = {
    # "User-Agent" : "Python-urllib/2.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36", # 浏览器
    "X-Requested-With": "XMLHttpRequest",  # 表示Ajax异步请求。
    "Content-Type": "application/x-www-form-urlencoded", # 表单数据会按照 key1=value1&key2=value2 键值对形式进行编码
    # "Content-Length": 144, # 是指发送的表单数据长度为144，也就是字符个数是144个。
    "Connection": "keep-alive",
    # "Cookie": "xx",
    # "Accept":"application/json",
}

# ======== 构建 http pos data
data = urllib.urlencode({"a":2, "b":1})
data = urllib.urlencode([("a", 1), ("b", 2)])

# ======== 忽略未经证实的证书
context = ssl._create_unverified_context()

def test_urlopne():
    # ======== 最简单的请求
    response = urllib2.urlopen(url='https://www.baidu.com')

    # ======== 带header的请求, Request实例
    request = urllib2.Request(url='https://www.baidu.com', data=None, headers=headers)
    response = urllib2.urlopen(url=request, timeout=5, context=context)

    # ======== request 方法
    print "method:", request.get_method() # "GET" or "POS"
    print "full_url:", request.get_full_url() # http://192.168.170.12:30080/index
    print "type:", request.get_type() # http, https, ftp
    print "host:", request.get_host() # 192.168.170.5:30080
    print "selector:", request.get_selector() # /index
    # request.add_header("a", "b")
    # request.add_unredirected_header("c", "b")
    # print "header_items", request.header_items() # 请求头列表
    # print request.add_data(data)
    # print request.get_data()
    # request.set_proxy(host=None, type=None) # 设置代理


    # ======== 自定义handle并且创建opener对象 urlopen 是一个特殊的opener对象
    # http_handler = urllib2.BaseHandler() # 基类，简单的功能
    # http_handler = urllib2.HTTPHandler() # 支持处理HTTP的请求
    # http_handler = urllib2.HTTPSHandler() # 支持处理HTTPS的请求
    # http_handler = urllib2.FTPHandler() # 支持处理FTP的请求
    # ======== 存放cookie的容器
    # 其实大多数情况下，我们只用CookieJar()，如果需要和本地文件交互，就用 MozillaCookjar() 或 LWPCookieJar()

    # ======== 获取Cookie，并保存到CookieJar()对象中
    # cookie = cookielib.CookieJar() # cookie 在内存中
    # http_handler = urllib2.HTTPCookieProcessor(cookie) # 支持处理Cookie的请求
    # opener = urllib2.build_opener(http_handler)
    # urllib2.install_opener(opener)
    # response = opener.open("https://www.baidu.com") # or response = opener.open(url=request")
    # cookie_str = ""
    # for item in cookie:
    #     cookie_str = cookie_str + item.name + "=" + item.value + ";"
    #     # print item.version, item.port, item.path, item.expires, item.is_expired()
    #     # print item.discard # session cookie
    #     # print item.comment
    # print "cookie:", cookie_str[:-1]

    # ======== 访问网站获得cookie，并把获得的cookie保存在cookie文件中
    # cookie = cookielib.MozillaCookieJar(filename="cookie.txt")
    # # cookie = cookielib.LWPCookieJar(filename="cookie.txt")
    # http_handler = urllib2.HTTPCookieProcessor(cookie)
    # opener = urllib2.build_opener(http_handler)
    # urllib2.install_opener(opener)
    # response = opener.open("https://www.baidu.com")
    # cookie.save()

    # ======== 从文件中获取cookies，做为请求的一部分去访问
    cookie = cookielib.MozillaCookieJar()
    cookie.load(filename="cookie.txt")
    http_handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(http_handler)
    urllib2.install_opener(opener)
    response = opener.open("https://www.baidu.com")

    # ======== 请求状态
    print "state_code:", response.code # 状态码 (response.getcode())
    # print "full_url:", response.url # 网址 (response.geturl())
    # print "meta info:", response.info() # 回应页面的元信息

    # ======== 获取 content 编码
    # encoding = re.search(r"charset=(.+)", response.info()["Content-Type"]).group(1)

    # ======== 获取 html 静态内容, 支持文件对象的操作方法
    # encoding = "utf8"
    # print response.read().decode(encoding) # 可以指定读N个字节的数据
    # print response.readline().decode(encoding)
    # print response.readlines().decode(encoding)

def test_requests():
    # https://requests.readthedocs.io/en/latest/ request wike

    # requests.request("GET") ~= requests.get()
    # requests.request("POST") ~= requests.post()

    # =========== requests.request(method, url, **kwargs)
    params = {'p1':'p1', 'p2':'p2'} # params 提供字典用于与 url 拼接, 构成查询字符串
    data = {'d1':'d1', 'd2':'d2'} # data 是POST请求时提交的form表单, get 方法会忽略 data; 类型是字符串是data, 字典时是form, 
    json_data = json.dumps(data) # json 是POST请求时提交的json数据, get 方法会忽略, 有data时会忽略，
    headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",} # 请求头
    timeout = 0.1 # 最多等待服务器回应多少秒,几乎所有生产代码都应在几乎所有请求中使用此参数。不这样做可能会导致您的程序无限期挂起
    timeout = (5, 0.2) # 连接、读取超时

    res = requests.request("GET", "http://httpbin.org/get", params=params, headers=headers)
    res = requests.request("POST", "http://httpbin.org/post", params=params, data=data, json=json_data, headers=headers)

    # cookies = {"cookies":"cookies"} # Dict or CookieJar object
    # cookies = requests.cookies.RequestsCookieJar() # domain path 适合在多个域或路径上使用
    # cookies.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
    # cookies.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
    # res = requests.request("GET", "http://httpbin.org/cookies", cookies=cookies)

    # res = requests.request("GET", "https://github.com/", timeout=timeout)

    # allow_redirects = True # 是否允许重定向, 会影响 res.history
    # res = requests.request("GET", "http://github.com/", timeout=10) # 会将http请求重定向为https
    # res = requests.request("GET", "http://httpbin.org/absolute-redirect/3", allow_redirects=False)

    # 强烈建议以二进制模式打开文件。这是因为 Requests 会尝试为提供 Content-Length 标头
    # file 可以明确设置文件名、内容类型和标题, 也可以直接使用字符串
    # files = {
    #     "file1": open('names.csv', 'rb'),
    #     'file2': ("filename.lua", open('names.csv', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'}),
    #     "file3": ('report.csv', 'some,data,to,send\nanother,row,to,send\n'),
    #     "image1": ('foo.png', open('foo.png', 'rb'), 'image/png'),
    # }
    # res = requests.request("POST", "http://httpbin.org/post", files=files)

    # auth = ("sws", 123)
    # res = requests.request("GET", "http://httpbin.org/basic-auth/sws/123", auth=auth)

    # def print_url(r, *args, **kwargs):
    #     print(r.url)
    # def record_hook(r, *args, **kwargs):
    #     r.hook_called = True
    #     return r
    # hooks = {'response': [print_url, record_hook]} # 钩子触发回调
    # res = requests.request("GET", 'https://httpbin.org/get', hooks=hooks)

    # stream 是否流式传输,避免将大响应的内容直接加载进内存
    # res = requests.request("GET", 'http://httpbin.org/stream/2', stream=True)
    # if r.encoding is None: r.encoding = 'utf-8'
    # for chunk in res.iter_content(chunk_size=128):
    #     print chunk
    # for line in res.iter_lines(chunk_size=2, decode_unicode=True, delimiter="xxxxxx"):
    #     print line

    # proxies = {
    #     'http': 'http://61.191.56.60:8085',
    #     # 'https': 'http://10.10.1.10:1080',
    # }
    # res = requests.request("GET", 'http://example.org', proxies=proxies)

    # verify = True # true or false 是否验证服务器ssl证书, 路径时可以验证一些私有证书
    # cert = "/path/cert" # 客户端证书
    # res = requests.request("GET", 'https://requestb.in', verify=verify, cert=None)

    # =========== HttpResponse 响应对象，该对象具有以下常用属性
    print res.status_code # 返回HTTP响应码
    # print res.encoding # 查看或者指定响应字符编码
    # print res.url # 查看请求的最终 URL 位置 地址
    # print res.headers # 不区分大小写的响应标头字典
    # print res.cookies # 服务器发回的 CookieJar
    print res.text # 以字符串形式输出
    # print rets.content # 以字节流形式输出，若要保存下载图片需使用该属性。
    # print res.json() # 以json格式输出，Response content type: application/json
    # print res.elapsed # 发送请求和响应到达之间经过的时间
    # print res.history # 来自请求历史的响应对象列表。任何重定向响应都将在这里结束。该列表按从最早到最近的请求排序
    # print res.raw # 原始套接字响应,可以使用read方法
    # print res.reason # 响应的文本原因， “Not Found” or “OK”.


def test_session():
    # Session 对象允许您跨请求保留某些参数。它还在会话实例发出的所有请求中保留 cookie，并将使用 urllib3 的连接池。
    # 因此，如果您向同一主机发出多个请求，则底层 TCP 连接将被重用，这可能会显着提高性能
    s = requests.Session()
    s.headers.update({'x-test': 'true'}) # 添加固定请求头参数
    # requests.utils.add_dict_to_cookiejar(s.cookies, {"a":1})
    # print s.cookies

    res = s.get('https://httpbin.org/get')
    print res.text

    res = s.get('https://httpbin.org/get', headers={'x-test2': 'false'})
    print res.text


def test_cookie():
    cookie_dict = dict(a=2, b=3) # cookies 字典
    cookiejar = None # 在该cookiejar上更新
    overwrite = None # 是否覆盖旧的，当key相同时
    cookies_jar = requests.cookies.cookiejar_from_dict(cookie_dict=cookie_dict, cookiejar=None, overwrite=True)
    cookies_jar = requests.utils.add_dict_to_cookiejar(cj=None, cookie_dict=cookie_dict)
    print cookies_jar
    print cookies_jar.get_dict()
    print cookies_jar.items()
    for key, val in cookies_jar.iteritems(): # iterkeys(), itervalues(), keys(), values()
        print key, val
    cookies_jar.update(dict(c=1))
    cookies_jar.set("d", 4)

    cookies_dict = requests.utils.dict_from_cookiejar(cj=cookies_jar)
    print cookies_dict

def main():
    # test_urlopne()
    # test_requests()
    test_session()
    # test_cookie()

if __name__ == "__main__":
    main()