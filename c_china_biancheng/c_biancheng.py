#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import os
import sys
import time
import multiprocessing
import json

def get_file_path(file_name):
    root_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_path = os.path.join(root_path, file_name)
    return file_path


def get_file_bc_filter_index():
    return get_file_path("bc_filter_index.log")

def read_filter_index():
    file_path = get_file_bc_filter_index()

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

    file_path = get_file_bc_filter_index()

    with open(file_path, 'w') as f:
        f.write(content)

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

def get_file_last_index():
    return get_file_path("bc_last_index.log")

def read_last_index():
    file_path = get_file_last_index()

    content = 0
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
    return int(content)

def write_last_index(index):
    file_path = get_file_last_index()
    with open(file_path, 'w') as f:
        f.write(str(index))


def write_url_file(data_list):
    file_path = get_file_path('bc_url.log')
    count = 1
    with open(file_path, 'a') as f:
        for url, title in data_list:
            f.write("{}. {} === {}\n".format("*", title, url))
            count += 1

def write_vip_file(data_list):
    file_path = get_file_path('bc_vip_url.log')
    count = 1
    with open(file_path, 'a') as f:
        for url, title in data_list:
            f.write("{}. {} === {}\n".format("*", title, url))
            count += 1

def get_right_url_and_title(index_list):
    url_format = r'http://c.biancheng.net/view/{}.html'
    title_list = list()
    error_list = list()
    finish_list = list()
    vip_list = list()
    for index in index_list:
        url = url_format.format(index)
        rsp = requests.get(url)
        if rsp.status_code == requests.codes.ok:
            title = re.search(r'<title>(.+)</title>', rsp.content).group(1)
            title_list.append((url, title))
            finish_list.append(index)
            if not re.search(r"window.prePageURL", rsp.content) \
                and not re.search(r"window.nextPageURL", rsp.content):
                vip_list.append(title_list[-1])
        else:
            error_list.append(index)
    data = {"title_list":title_list, "error_list":error_list, "finish_list":finish_list, "vip_list":vip_list}
    return data


def build_result_data(ret, data):
    ret["title_sum"].extend(data["title_list"])
    ret["vip_sum"].extend(data["vip_list"])
    if ret.has_key("err_num"):
        ret["err_sum"].extend(data["error_list"])
    if ret.has_key("fin_sum"):
        ret["fin_sum"].extend(data["finish_list"])

def once():
    # args
    url_count = 100
    step = 100
    is_mult_process = False

    # build all task
    index_data = read_filter_index()
    index_set = index_data.get("index_set", set())
    all_task, task_args = list(), list()
    count = 0
    for i in xrange(url_count):
        if str(i) in index_set: continue
        count += 1
        task_args.append(i)
        if count == step:
            count = 0
            all_task.append(task_args)
            task_args = list()
    if task_args:
        all_task.append(task_args)

    # runging task
    result = dict(
        title_sum = list(),
        err_sum = index_data["error_list"],
        fin_sum = index_data["finish_list"],
        vip_sum = list(),
    )

    if not is_mult_process:
        for args in all_task:
            data = get_right_url_and_title(args)
            build_result_data(result, data)
    else:
        cpu_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(cpu_count)
        all_data = pool.map_async(func=get_right_url_and_title, iterable=all_task,)
        all_data = all_data.get(99999)
        for data in all_data:
           build_result_data(result, data)

    # write data
    write_filter_index(index_data)
    write_url_file(result["title_sum"])
    write_vip_file(result["vip_sum"])

def many():
    # args
    url_count = 100
    step = 100
    is_mult_process = False

    # build all task
    start_index = read_last_index()
    all_task, task_args = list(), list()
    count = 0
    for i in xrange(start_index, url_count):
        count += 1
        task_args.append(i)
        if count == step:
            count = 0
            all_task.append(task_args)
            task_args = list()
    if task_args:
        all_task.append(task_args)

    # runging task
    result = dict(
        title_sum = list(),
        vip_sum = list(),
    )

    if not is_mult_process:
        for args in all_task:
            data = get_right_url_and_title(args)
            build_result_data(result, data)
    else:
        cpu_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(cpu_count)
        all_data = pool.map_async(func=get_right_url_and_title, iterable=all_task,)
        all_data = all_data.get(99999)
        for data in all_data:
           build_result_data(result, data)

    # write data
    write_url_file(result["title_sum"])
    write_vip_file(result["vip_sum"])
    write_last_index(url_count)

def main():
    import datetime
    print time.time()
    print datetime.datetime()


if __name__ == "__main__":
    start_time = time.time()
    # once()
    many()
    main()
    end_time = time.time()
    print "\n[Finish]\nstart_ts:{}, end_ts:{}, run_time:{:.6}".format(start_time, end_time, end_time-start_time)