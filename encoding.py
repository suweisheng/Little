# encoding: utf8

import os
import sys
import time
import codecs
import locale

# Python2.x中的编码问题
# https://www.cnblogs.com/huxi/archive/2010/12/05/1897271.html

# python2中文乱码
# https://blog.csdn.net/Daningliu/article/details/121709077

# python2x 与 python3x的编码区别
# https://blog.csdn.net/pipisorry/article/details/44136297


# 乱码的本质是字符的编码格式与显示字符的环境编码格式不一致引起的
# 环境编码：windows下命令行的默认编码是gbk的，Linux环境下命令行的默认编码是utf-8的

def test_encoding():
    # python2 默认使用 ASCII 来读取代码源文件
    # 源代码文件中，如果有用到非ASCII字符，则需要在文件头部进行字符编码的声明 # -*- coding: utf8 -*-
    # 来告诉python解释器使用utf8编码来读取、执行代码文件。否则如果有中文等会出错

    # 英文表达中，encoding 一般是名词，指utf8等编码，与代码里的decode，encode无关
    # decode，encode 是基于unicode来说的
    # 其他编码-> unicode 是解码decode; unicode -> 其他编码 是编码encode

    # python 的内部都是使用unicode来处理的，但是unicode的使用需要考虑的是它的编码格式有两种
    # 一是UCS-2，它一共有65536个码位，另一种是UCS-4，它有2147483648个码位。
    # 对于这两种格式，python 都是支持的，这个是在编译时通过–enable- unicode=ucs2或–enable-unicode=ucs4来指定的。
    # 查看安装的python用什么编码可以通过 sys.maxunicode 的值来判断
    # sys.maxunicode 的值为65535,那么就是UCS-2,如果是1114111就是UCS-4编码
    print sys.maxunicode # 65536  UCS-2


    # python2 中的字符串有 str 和 unicode 两种内部表示,都是basestring的子类
    # str 对象，字面量的字符串，或是从文件中open read 到的字符串；unicode 对象，带u的字面量字符串
    # 严格意义上说，str其实是字节串，它是unicode经过编码后的字节组成的序列
    # unicode才是真正意义上的字符串，对字节串str使用正确的字符编码进行解码后获得

    # repr(obj) # 将对象转化为供解释器读取的形式,返回一个对象的 string 格式
    # python在做编码转换时，通常需要以 unicode 作为中间编码
    # 即先将其他编码的字符串解码（decode）成unicode，再从unicode编码（encode）成另一种编码。

    # 在python中
    # 对于print，输出都是接收字节序列（可以看成str对象），然后stdout会按照自己编码规则解码后（不同平台不同的编码）输出人类可识别的文字
    # 对于任何str类型的对象，打印时会直接将字节序列（源文件开头指定的编码（# encoding: utf8））传递给stdout
    # 对于任何Unicode类型的对象，打印时会自动根据环境编码（stdout编码）转为特定编码后传递给stdout
    
    print repr("汉"), # 汉 的utf8字节编码 '\xE6\xB1\x89'
    print repr(u"汉") # 汉 的unicod字节编码 '\u6c49'
    print len("汉"), len(u"汉")

    # 在win32下，环境编码是 gbk （sys.stdout.encoding 可以查看）
    # 乱码的本质：字符的编码格式与显示字符的环境编码格式不一致
    # 在python中，对于任何 Unicode 类型编码的字符，打印时会自动根据环境编码转为特定编码后再显示

    print ""
    print "platform ->", sys.platform
    print "stdout encoding ->", sys.stdout.encoding # win平台下cp936 就是 gbk

    # str -> unicode 和 unicode -> str，都要指定编码，不指定默认编码都是sys.getdefaultencoding()
    # encode的不正常使用
    # 对str类型进行encode，因为encode需要的是Unicode类型，这个时候python会用默认编码decode成Unicode类型，再用你给出编码进行encode
    # 注意这里默认编码不是源文件开头的encoding，而是sys.getdefaultencoding 的 ASCII编码）
    # 字符串前面加'u'，将str对象强制按照源文件开台的encoding解码成unicode对象

    if sys.platform == 'win32':
        print "汉" # 乱码，变量在程序中是utf8编码，stdout解码是gbk
        print u"汉" # 正常，unicode输出时会自动根据环境编码转成str对象
        print u"汉".encode("gbk") # 正常
        print "汉".decode("utf8").encode("gbk") # 正常
        print "汉" == u'汉'.encode("utf8") # true
        print u"汉" == '汉'.decode("utf8") # true
        print '汉'.encode("gbk") # error 相当于 '汉'.decode(sys.getdefaultencoding()).encode("gbk")
    if sys.platform.startswith('linux'):
        print "汉" # 正常，变量在程序中是utf8编码，stdout解码是utf8
        print u"汉" # 正常，unicode输出时会自动根据环境编码转成str对象
        print u"汉".encode("utf8") # 正常
        print "汉".decode("utf8").encode("utf8") # 正常
        print "汉" == u'汉'.encode("utf8") # true
        print u"汉" == '汉'.decode("utf8") # true

    
    # python3中，
    # 所有python3文件默认都是utf-8来编码的，无需在文件开头指定encoding，但是一般为了兼容python2还是建议写上
    # 其实无论给encoding参数设定什么取值，其编码方式都是utf-8
    # 字符串类型统一为unicode，不再需要在中文前面加u来使中文字符变为Unicode这种写法

    # 2.x中字符串有str和unicode两种类型，str有各种编码区别，unicode是没有编码的标准形式。
    # unicode通过编码转化成str，str通过解码转化成unicode。

    # 3.x中将字符串和字节序列做了区别，字符串str是字符串标准形式与2.x中unicode类似，bytes类似2.x中的str有各种编码区别。
    # bytes通过解码转化成str，str通过编码转化成bytes。
    

def test_default_encoding():
    print "system default encoding ->", sys.getdefaultencoding() # Unicode 用的当前默认字符串编码(不分平台)
    if sys.platform == 'win32':
        # platform -> win32
        # stdout encoding -> cp936

        # # win平台下cp936 就是 gbk
        # dos 平台：chcp 936 更改编码为gbk，chcp 65001 更改编码为utf8
        print "platform ->", sys.platform
        print "stdout encoding ->", sys.stdout.encoding # sys.stdin也是一致的
        ENCODING = "gbk"
    elif sys.platform.startswith('linux'):
        # platform -> linux2
        # stdout encoding -> UTF-8

        # linux 下都是
        print "platform ->", sys.platform
        print "stdout encoding ->", sys.stdout.encoding # sys.stdin也是一致的
        ENCODING = "utf8"

    # # 调用setdefaultencoding时必须要先reloa
    # # 在python安装目录的Lib文件夹下有一个叫site.py的文件;在里面可以找到main()
    # # 因为这个site.py默认会在python虚拟机启动时初始化
    # # setencoding() 函数，将 ascii 设置默认 Unicode 字符编码
    # # if hasattr(sys, "setdefaultencoding"): del sys.setdefaultencoding  初始化加载的sys后 删除了setdefaultencoding函数
    # # 如果需要重新设置 Unicode 字符编码 需要 reload(sws)，这样才能找到 setdefaultencoding 函数
    reload(sys)
    sys.setdefaultencoding(ENCODING) # Unicode 实现使用的当前默认字符串编码
    print "now system encoding ->", sys.getdefaultencoding()

    # 小技巧, 将某编码的字节序列输出正确的中文
    # 在 window 下的 python 环境命令行下，环境编码是gbk
    # >>> a='中'
    # >>> a
    # '\xd6\xd0'
    # >>> a='\xd6\xd0'
    # >>> a
    # 中
    # 在 linux 下的 python 环境命令行下，环境编码是utf8
    # >>> a='中'
    # >>> a
    # '\xe4\xb8\xad'
    # >>> a='\xe4\xb8\xad'
    # >>> a
    # 中

def test_file():
    # 读取文件时，内置的open()方法打开文件时, read write 接收的都是str对象
    # read()读取的是str，读取后需要使用正确的编码格式（文件存储时用的编码）进行decode()。
    # write()写入时，如果参数是unicode，Python将先使用默认的字符编码进行编码然后写入
    # 书写文件名时，为了保证平台系统正确识别，建议都使用unicode

    with open(u"encoding_test_file.txt", 'w') as f:
        # 使用源代码文件声明的字符编码写入文件，最终文件编码utf8
        content = "你好"
        f.write(content)
    with open(u"encoding_test_file.txt", 'w') as f:
        # 最终文件编码gbk
        content = "你好"
        f.write(content.decode("utf8").encode("gbk"))
    with open(u"encoding_test_file.txt", 'w') as f:
        # 最终文件编码tf8, 直接写入会报错，因为此时 sys.getdefaultencoding()为ascii
        content = u"你好"
        f.write(content.encode("utf8"))

    with open(u"encoding_test_file.txt", 'r') as f:
        # 文件是以utf8编码存储的
        content = f.read()
        print type(content)
        print content # 乱码，因为str是utf8编码，stdout是gbk编码
        print content.decode("utf8") # 正常
    with open(u"encoding_test_file.txt", 'r') as f:
        # 文件是以gbk编码存储的
        content = f.read()
        print type(content)
        print content # 正常，因为str是gbk编码，stdout是gbk编码
        # print content.decode("utf8") # 报错，用utf8无法解码gbk的字符
        print content.decode("gbk") # 正常

def test_codecs():
    # 使用codecs模块

    # open() 指定encoding参数，使用具体的编码将读取文件内容解码成unicode
    with codecs.open(u"encoding_test_file.txt", encoding='gbk') as f:
        # 文件是以gbk编码存储的
        content = f.read()
        print type(content)
        print content

    # with codecs.open(u"encoding_test_file.txt", encoding='UTF-8') as f:
    #     # 文件是以utf8编码存储的
    #     content = f.read()
    #     print type(content)
    #     print content
    
    # 写入时，如果参数是unicode，则使用open()时指定的编码进行编码后写入
    # 如果参数是str，则使用 getsys.getdefaultencoding() decode成unicode，再按照上述规则
    # with codecs.open(u"encoding_test_file.txt", 'w', encoding='UTF-8') as f:
    #     #  文件是以utf8编码存储的
    #     content = "哈哈" # 直接写入报错，默认的编码是ascii
    #     content = content.decode("utf8")
    #     f.write(content)

    # with codecs.open(u"encoding_test_file.txt", 'w', encoding='gbk') as f:
    #     #  文件是以gbk编码存储的
    #     content = "哈哈" # 直接写入报错，默认的编码是ascii
    #     content = content.decode("utf8")
    #     f.write(content)

def test_locale():
    def p(f):
        print '%s.%s(): %s' % (f.__module__, f.__name__, f())
    # 返回当前系统所使用的默认字符编码(unicode)
    p(sys.getdefaultencoding)
    # 返回用于转换Unicode文件名至系统文件名所使用的编码
    p(sys.getfilesystemencoding)
    # 获取默认的区域设置并返回元祖(语言, 编码)
    p(locale.getdefaultlocale)
    # 返回用户设定的文本数据编码
    p(locale.getpreferredencoding)

    # Python中编码'MBCS'与'DBCS'是同义词，指当前Windows环境中MBCS指代的编码。
    # Linux的Python实现中没有这种编码，所以一旦移植到Linux一定会出现异常！
    # 另外，只要设定的Windows系统区域不同，MBCS指代的编码也是不一样的.
    with open("中文.txt".decode("utf8").encode("gbk"), 'r') as f:
        pass
    with open(u"中文.txt", 'r') as f:
        pass

def test_str_unicode():
    unicode_obj = unicode("汉", encoding='utf8') # 将str对象按照encoding解码成unicode对象,默认是是sys.getdefaultencoding
    unicode_obj = unicode(u"汉")
    print unicode_obj

    # str_obj = str(u"汉") # 将unicode对象按照sys.getdefaultencoding编码成str对象, 这里默认是ascii，所以会报错
    str_obj = str("汉") # 如果是str对象，直接返回，这里是utf8编码的str对象
    print str_obj


def test_json():
    # 特殊场景：JSON
    # json.dumps需要特别注意，内部会在dumps的时候，默认把str decode为unicode，decode采用的编码是源文件头的encoding
    import json
    obj = [u'foo', {'bar': ('baz', None, 1.0, 2)}, 2, u"汉"]
    
    # encoding="utf8" 默认utf8, 可以指定编码, 用于解码对象中的str
    # ensure_ascii=true 默认true, 确保了所有非ASCII字符都转义成 \uXXXX 的ASCII序列
    print obj
    ret = json.dumps(obj, ensure_ascii=True, encoding="utf8") # 结果是ASCII序列
    print type(ret) # str
    print ret # 只能输出中文的utf8码

    ret = json.dumps(obj, ensure_ascii=False, encoding="utf8", ) # 结果是unicode序列
    print type(ret) # unicode
    print repr(ret)
    print ret # 能正确输出中文

def main():
    # test_encoding()
    # test_default_encoding()
    # test_file()
    # test_codecs()
    # test_locale()
    # test_str_unicode()
    test_json()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print "\n[Finish {:.4f} s]".format(end_time-start_time)