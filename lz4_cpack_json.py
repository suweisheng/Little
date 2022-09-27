#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import cPickle
import json
import copy
import lz4.frame
import hashlib

def test_cpack():
    data = {"data":[1,2,3], "key":set([1,2]), "value":5}
    # dump()、 load()、 dumps()、 loads()
    # dumps 将内存对象序列化成字符串, loads 将字符串反序列化成内存对象

    # 序列化，反序列化后的结果保存在内存中
    content = cPickle.dumps(data)
    data = cPickle.loads(content)

    # 序列化后结果保存到文件
    f = open("cpack.obj", 'w+')
    cPickle.dump(data, f)
    f.close()
    # 从文件内容读取数据后反序列化
    f = open("cpack.obj", 'r+')
    data = cPickle.load(f)
    f.close

def test_json():
    # dump 将 python 对象 转成 json 字符串(str对象)
    # # encoding="utf" 可以指定编码
    # print json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}, 2, "fff"])
    # print json.dumps("\\")
    # print json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True) # dict key sort
    # print json.dumps([1,2,3,{'4': 5, '6': 7}], separators=('===','=')) # list,dict分隔符
    # print json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4, separators=('===', '? ')) #indent缩进空格数

    # loads 将 json 字符串 转成 python 对象
    print json.loads('"\\"foo\\bar"')
    print json.loads('{"c": 0, "b": 0, "a": 0}')

    # 注意：
    # JSON 的键/值对中的键始终是 str 类型。当字典转换为 JSON 时，字典的所有键都被强制转换为字符串。
    # 因此，如果将字典转换为 JSON，然后再转换回字典，则字典可能不等于原始字典。
    # 也就是说，loads(dumps(x)) != x 如果 x 有非字符串键

    obj = {1:"a", 2:"b"}
    print obj
    print json.dumps(obj)
    print json.loads(json.dumps(obj))


def test_copy():
    data = ['foo', {'bar': ('baz', None, 1.0, 2)}, 2, "fff"]
    shallow_data = copy.copy(data)
    data[0] = "zzz"
    data[1]["bar"] = 23
    print shallow_data

    data = ['foo', {'bar': ('baz', None, 1.0, 2)}, 2, "fff"]
    deep_data = copy.deepcopy(data)
    data[0] = "zzz"
    data[1]["bar"] = 23
    print deep_data

def test_lz4():
    # os.urandom 返回适合加密使用的 n 个随机字节的字符串
    input_data = 20 * 128 * os.urandom(1024)  # Read 20 * 128 kb
    compressed = lz4.frame.compress(input_data)
    decompressed = lz4.frame.decompress(compressed)

    input_data = "里号"
    compressed = lz4.frame.compress(input_data)
    decompressed = lz4.frame.decompress(compressed)
    print decompressed.decode("utf8")

def test_hashlib():
    content = "fff eee"
    m = hashlib.md5() # 构造哈希对象（md5, sha1, sha224, sha256, sha384, sha512）
    m.update(content) # 构造哈希对象
    print m.hexdigest() # 随机获取目前为止提供给它的字符串的串联
    m.update(" the spammish repetition")
    print m.hexdigest()

    print hashlib.sha1(content).hexdigest() # 简练的方式

def main():
    # test_cpack()
    test_json()
    # test_copy()
    # test_lz4()
    # test_hashlib()


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print "\n[Finish {:.4f} s]".format(end_time-start_time)