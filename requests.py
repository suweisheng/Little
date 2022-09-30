# encoding: utf8

import re
import urllib2
import urllib
import ssl
import cookielib

# urllib2.urlopen(url[, data[, timeout[, cafile[, capath[, cadefault[, context]]]]])
# url: 可以接收一个url字符串或Request对象
# data: 指定要发送到服务器的附加数据的字符串, 如果参数有值此时 http 请求从GET转为POST, 相关urllib.urlencode
# timeout: 阻塞最长时间
def test_urlopne():

    response = urllib2.urlopen(url='http://192.168.170.5:30080/index')
    print response.code # 状态码 (response.getcode())
    print response.url # 网址 (response.geturl())
    print response.info() # 回应页面的元信息

    # 获取 content 编码
    encoding = re.search(r"charset=(.+)", response.info()["Content-Type"]).group(1)
    # 获取 html 静态内容, 支持文件对象的操作方法
    # print response.read().decode(encoding) # 可以指定读N个字节的数据
    # print response.readline().decode(encoding)
    # print response.readlines().decode(encoding)

    # 构建data, http pos data
    data = urllib.urlencode({"a":2, "b":1})
    data = urllib.urlencode([("a", 1), ("b", 2)])

    # 构建请求头
    headers = {
        # "User-Agent" : "Python-urllib/2.6",
        "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
        "X-Requested-With": "XMLHttpRequest",  # 表示Ajax异步请求。
        "Content-Type": "application/x-www-form-urlencoded", # 表单数据会按照 key1=value1&key2=value2 键值对形式进行编码
        "Content-Length": 144, # 是指发送的表单数据长度为144，也就是字符个数是144个。
        "Connection": "keep-alive",
        "Cookie": "xx",
    }

    # 忽略未经证实的证书
    context = context = ssl._create_unverified_context()

    # Request实例
    request = urllib2.Request(url='http://192.168.170.5:30080/index', data=None, headers={})

    # print request.get_method()

    # print request.get_full_url() # http://192.168.170.5:30080/index
    # print request.get_type() # http, https, ftp
    # print request.get_host() # 192.168.170.5:30080
    # print request.get_selector() # /index

    # # print request.has_data()
    # print request.add_data(data)
    # print request.get_data()

    # print request.add_header("a", "b")
    # print request.add_unredirected_header("a", "b")
    # # print request.has_header()
    # print request.get_header(header_name="User-Agent", default=None)
    # print request.header_items()

    # request.set_proxy(host=None, type=None) # 设置代理

    response = urllib2.urlopen(url=request, timeout=5, context=context)
    
    
    # 自定义handle
    http_handler = urllib2.BaseHandler() # 基类，简单的功能
    http_handler = urllib2.HTTPHandler() # 支持处理HTTP的请求
    http_handler = urllib2.HTTPSHandler() # 支持处理HTTPS的请求
    http_handler = urllib2.FTPHandler() # 支持处理FTP的请求

    # 存放cookie的容器
    cookie = cookielib.CookieJar()

    # cookie = cookielib.FileCookieJar(filename="cookie.txt")
    # cookie = cookielib.MozillaCookieJar(filename="cookie.txt")
    # print cookie.filename
    # # cookie.load()
    # for item in cookie:
    #     print "==== cookie ----", item.name + "=" +item.value
    # print "--"

    http_handler = urllib2.HTTPCookieProcessor() # 支持处理Cookie的请求



    # 自定义 opener
    opener = urllib2.build_opener(http_handler) # 创建opener对象 urlopen 是一个特殊的opener对象
    # urllib2.install_opener(opener) # 将 opener 定义为全局，程序里所有的请求都使用自定义的opener

    request = urllib2.Request(url='http://www.baidu.com', data=None, headers={})
    response = opener.open(request) # url 可以是处理器对象
    # print cookie.make_cookies(response=response, request=request)

    for item in cookie:
        # continue
        print "==== cookie ----", item.name + "=" +item.value
        # print item.version, item.port, item.path, item.expires, item.is_expired()
        # print item.discard # session cookie
        # print item.comment
        
    # cookie.add_cookie_header(request)
    # print request.header_items()

    response

    # cookie.save(ignore_expires=True)
    # cookie.revert()

    print response.code

def main():
    test_urlopne()

if __name__ == "__main__":
    main()