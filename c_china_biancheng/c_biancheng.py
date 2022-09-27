#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import os
import sys
import time
import multiprocessing
import json

def read_filter_index():
    file_name = "bc_filter_index.log"
    root_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_path = os.path.join(root_path, file_name)

    if not os.path.exists(file_path):
        return {"finish_list":list(), "error_list":list(), "index_set":set()}

    content = ""
    with open(file_path, 'r') as f:
        content = f.read()

    data = filter_index_decode(content)
    return data

def filter_index_decode(content):
    point = "=" * 15
    index_str = "([\d,\n]*)"
    def _decode(flag):
        re_str = "{point} {flag}\n{index_str}{point} {flag}\n".format(point=point, flag=flag, index_str=index_str)
        _str = re.search(re_str, content).group(1)
        index_list = list()
        if _str:
            _str_list = _str.split("\n")
            if _str_list[-1] == "": _str_list = _str_list[:-1]
            for v in _str_list:
                v = v.split(",")
                if v[-1] == "": v = v[:-1]
                index_list.extend(v)
        return index_list

    finish_list = _decode("finish")
    error_list = _decode("error")
    index_set = set(finish_list) | set(error_list)
    return {"finish_list":finish_list, "error_list":error_list, "index_set":index_set}


def write_filter_index(data):
    content = filter_index_encode(data)

    file_name = "bc_filter_index.log"
    root_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_path = os.path.join(root_path, file_name)

    with open(file_path, 'w') as f:
        content = f.write(content)

    return True

def filter_index_encode(data):
    point = "=" * 15
    def _encode(flag, index_list):
        index_str = ''
        step = 30
        if index_list:
            for i in xrange(len(index_list)):
                index_str += str(index_list[i]) + ","
                if ((i+1) % step == 0):
                    index_str += "\n"
        if index_str and index_str[-1] != "\n":
            index_str = index_str + "\n"
        
        ret = "{point} {flag}\n{index_str}{point} {flag}\n".format(point=point, flag=flag, index_str=index_str)
        return ret

    finish_str = _encode("finish", data.get("finish_list", None))
    error_str = _encode("error", data.get("error_list", None))
    return finish_str + "\n\n" +error_str



def get_right_url_and_title(index_list):
    url_format = r'http://c.biancheng.net/view/{}.html'
    title_list = list()
    error_list = list()
    finish_list = list()
    for index in index_list:
        url = url_format.format(index)
        rsp = requests.get(url)
        if rsp.status_code == requests.codes.ok:
            title = re.search(r'<title>(.+)</title>', rsp.content).group(1)
            title_list.append((url, title))
            finish_list.append(index)
        else:
            error_list.append(index)
    data = {"title_list":title_list, "error_list":error_list, "finish_list":finish_list}
    return data

def write_url_file(data_list):
    root_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_name = 'bc_url.log'
    log_path = os.path.join(root_path, file_name)
    count = 1
    with open(log_path, 'a') as f:
        for url, title in data_list:
            f.write("{}. {} === {}\n".format("*", title, url))
            count += 1

def main():
    # task args
    url_count = 1000
    step = 30
    index_data = read_filter_index()
    index_set = index_data.get("index_set", set())
    task_args_list = list()
    task_args = list()
    count = 0
    for i in range(url_count):
        if str(i) in index_set: continue
        count += 1
        task_args.append(i)
        if count == step:
            count = 0
            task_args_list.append(task_args)
            task_args = list()
    if task_args:
        task_args_list.append(task_args)

    # runging task
    title_sum = list()
    err_sum = index_data["error_list"]
    fin_sum = index_data["finish_list"]

    if False:
        for args in task_args_list:
            data = get_right_url_and_title(args)
            title_sum.extend(data["title_list"])
            err_sum.extend(data["error_list"])
            fin_sum.extend(data["finish_list"])
    else:
        pool = multiprocessing.Pool(4)
        ret = pool.map_async(func=get_right_url_and_title, iterable=task_args_list,)
        ret = ret.get(99999)
        for data in ret:
            title_sum.extend(data["title_list"])
            err_sum.extend(data["error_list"])
            fin_sum.extend(data["finish_list"])

    # write data
    write_filter_index(index_data)
    write_url_file(title_sum)

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print "\n[Finish]\nstart_ts:{}, end_ts:{}, run_time:{:.6}".format(start_time, end_time, end_time-start_time)