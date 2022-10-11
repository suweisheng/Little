#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import requests
import os
import time
import sys
import logging
import uuid
import datetime
import math

def newLogObj():
    cur_path = os.path.split(os.path.realpath(__file__))[0]
    cur_path = cur_path + r"\picture"
    if not os.path.exists(cur_path):
        os.mkdir(cur_path)
    logFile = cur_path + "\\" + time.strftime("%Y-%m-%d", time.localtime()) + ".log"
    if not os.path.exists(logFile):
        with open(logFile, "w") as f: pass

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "[%Y-%m-%d %H:%M:%S]")
    # logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(levelname)s - %(message)s',datefmt="[%Y-%m-%d %H:%M:%S]")
    logger = logging.getLogger(__name__)
    logging.root.setLevel(logging.NOTSET)

    file_handler = logging.FileHandler(logFile)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # logger.info("Start print log")
    # logger.debug("Do something")
    # logger.warning("Something maybe fail.")
    # logger.info("Finish")
    return logger

logger =  newLogObj()

def getTime():
    return time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())

def log(msg):
    print getTime() + " " + msg

def mkdir(path):
    path = path.decode("utf8")
    if not os.path.exists(path):
        os.mkdir(path)
        logger.info("Create folder success: " + path)
    else:
        logger.warning("Folder is already exist: " + path)

def savePic(html_content, session, path, headers):
    picList = re.findall(r'data-original="(.+?)"', html_content)
    if not picList: return
    picList = list(set(picList)) # Remove duplicate elements
    for picLink in picList:
        rindex = picLink.rfind('/')
        picName = picLink[rindex:]
        pic = session.get(picLink, headers=headers)
        if pic.status_code == requests.codes["ok"]:
            fileName = path.decode("utf8")+picName
            if os.path.exists(fileName):
                logger.warning("Picture is already exist: " + picName)
            else:
                with open(fileName,'wb') as f:
                    f.write(pic.content)
                    logger.info('Save pictur: ' + picName)
                    time.sleep(1)
        else:
            logger.error("Picture get fail: " + pic.status_code + " " + picLink)
            time.sleep(1)

def saveGif(html_content, session, path, headers):
    picList = re.findall(r'data-actualsrc="(.+?)"', html_content)
    if not picList: return
    picList = [x for x in picList if ".gif" in x]
    picList = list(set(picList)) # Remove duplicate elements
    for picLink in picList:
        rindex = picLink.rfind('/')
        picName = picLink[rindex:]
        pic = session.get(picLink, headers=headers)
        if pic.status_code == requests.codes["ok"]:
            fileName = path.decode("utf8")+picName
            if os.path.exists(fileName):
                logger.warning("Gif is already exist: " + picName)
            else:
                with open(fileName,'wb') as f:
                    f.write(pic.content)
                    logger.info('Save pictur: ' + picName)
                    time.sleep(1)
        else:
            logger.error("Gif get fail: " + pic.status_code + " " + picLink)
            time.sleep(1)

def saveVideo(html_content, session, page, headers):
    video_ids = re.findall(r'data-lens-id="(\d+)"', html_content)
    if not video_ids: return
    v_headers = {
        'Referer' : 'https://v.vzuu.com/video/{}',
        'Origin' : 'https://v.vzuu.com',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        'Content-Type' : 'application/json',
    }
    video_api = 'https://lens.zhihu.com/api/videos/'
    for id in video_ids:
        v_headers['Referer'].format(id)
        video_url = video_api + id
        v_response = session.get(video_url, headers=headers)
        v_response_dict = v_response.json()
        
        download_url = v_response_dict['playlist']['ld']['play_url']
        video_format = v_response_dict['playlist']['ld']['format']
        video_name = "{}.{}".format(id, video_format)
        video = requests.get(download_url, headers=v_headers)
        if video.status_code == requests.codes["ok"]:
            path = page + "//" + video_name
            path = path.decode('utf8')
            if os.path.exists(path):
                logger.warning("Video is already exist: " + path)
            else:
                with open(path, 'wb') as f:
                    f.write(video.content)
                    logger.info('Save video: ' + path)
                    # time.sleep(1)
        else:
            logger.error("Video get fail: " + video.status_code + " " + path)
            # time.sleep(1)

def checkIsEmptyFolder(path):
    path = path.decode("utf8")
    if not os.listdir(path):
        os.removedirs(path)
        logger.info("Empty folder delete: " + path)

def getBasicInfo(question_id=286086375, limit=20, offset=0):
    # baseDir = 'C://Users//Admin//Desktop//zhihu_spider//'
    # url = 'https://www.zhihu.com/api/v4/questions/281282523/answers?include=content&limit=20&offset=0&sort_by=default'
    baseDir = os.path.split(os.path.realpath(__file__))[0]
    baseDir = baseDir + r"\picture"
    questionId = question_id
    limit = limit
    url = "https://www.zhihu.com/api/v4/questions/%d/answers?include=content&limit=%d&offset=%d&sort_by=default" % (questionId, limit, offset*limit)
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    # https://www.zhihu.com/api/v4/questions/23213328/answers?include=content&limit=1&offset=0&sort_by=default
    cookies = '''SESSIONID=exwH14Yffb9lDeyYvjK8xeWuGA5Rc4CxaJJPYABJ7O7; JOID=WlgcA06-ysSs73IZI7avmoYCZZ823qG66tcjSU7Ziv_NojdBGEaUQMbqcxkvEc6S5nnzH8HugBFHLi7zFFgds48=; osd=UlwdAU62zsWu73odIrSvkoIDZ58-2qC46t8nSEzZgvvMoDdJHEeWQM7uchsvGcqT5Hn7G8DsgBlDLyzzHFwcsY8=; _zap=da572251-f4cd-4258-a5a1-57394ec908a3; d_c0="AMDQm-AfgxSPTvA04_0CiY_oEQmUWnFfVmc=|1645177001"; z_c0="2|1:0|10:1645177023|4:z_c0|92:Mi4xanZOb0FRQUFBQUFBd05DYjRCLURGQ1lBQUFCZ0FsVk52N2I4WWdBcnl3aFRQQlB3MUpSd2RTbWFWVy1OXzhJNTRB|04da69c5c5e8a184183d8ba00677889860de66d09c156526a1407f6e31f5995c"; _xsrf=UbxykZGJhZWgUmqIvxZoXdrxbdObXkpw; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1651801372; tst=h; NOT_UNREGISTER_WAITING=1; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1653104376; KLBRSID=0a401b23e8a71b70de2f4b37f5b4e379|1653104376|1653104374'''
    cookies = dict([l.split("=", 1) for l in cookies.split("; ")])
    print cookies
    return {
        "baseDir" : baseDir,
        "url" : url,
        "headers" : headers,
        "cookies" : cookies,
    }

def getUrlJsonData(session, url, headers, cookies=None):
    r = session.get(url, headers=headers, cookies=cookies)
    if r.status_code == requests.codes["ok"]:
        logger.info("Connect success: " + r.url)
    else:
        logger.error("Connect fail: " + str(r.status_code) + r.url)
        return
    json_obj = json.loads(r.content.decode("utf8"))
    data = json_obj.get("data")
    if not data:
        logger.error("NO data: " + str(r.status_code) + r.url)
        return
    return json_obj

def pictureDowload(id=None, limit=None, start=1):
    start -= 1
    info = getBasicInfo(id, limit, start)
    baseDir, headers = info["baseDir"], info["headers"]
    url, cookies = info["url"], info["cookies"]

    mkdir(baseDir) # Create save folder

    session = requests.session()
    json_obj = getUrlJsonData(session, url, headers, cookies)
    if not json_obj: return
    data = json_obj.get("data")
    titleName = data[0]["question"]["title"].encode("utf8")
    mkdir(baseDir + titleName)
    logger.warning ("Question：%s， number：%d" % (titleName, json_obj.get('paging').get('totals')))

    index = start
    while True:
        if url == '':break # is last page
        index += 1 # page number, every page has limit number

        json_obj = getUrlJsonData(session, url, headers, cookies)
        if not json_obj: return
        page = '第{}页'.format(index)
        page = baseDir + titleName + "//" + page
        mkdir(page)

        for i in json_obj.get("data"):
            savePic(i.get('content'), session, page, headers)

        checkIsEmptyFolder(page)
        if json_obj.get('paging').get('is_end'): break # is last last page
        url = json_obj.get('paging').get('next') # next page
    logger.info("Dowload End")

def videoDowload(id=None, limit=None, start=1):
    start -=  1
    info = getBasicInfo(id, limit, start)
    baseDir, headers = info["baseDir"], info["headers"]
    url, cookies = info["url"], info["cookies"]

    mkdir(baseDir) # Create save folder

    session = requests.session()
    json_obj = getUrlJsonData(session, url, headers, cookies)
    if not json_obj: return
    data = json_obj.get("data")
    titleName = data[0]["question"]["title"].encode("utf8")
    mkdir(baseDir + titleName)
    log("Question：%s， number：%d" % (titleName, json_obj.get('paging').get('totals')))


    index = start
    while True:
        if url == '':break # is last page
        index += 1 # page number, every page has limit number

        json_obj = getUrlJsonData(session, url, headers, cookies)
        if not json_obj: return
        page = '第{}页'.format(index)
        page = baseDir + titleName + "//" + page
        mkdir(page)

        for i in json_obj.get("data"):
            saveVideo(i.get('content'), session, page, headers)

        checkIsEmptyFolder(page)
        if json_obj.get('paging').get('is_end'): break # is last last page
        url = json_obj.get('paging').get('next') # next page
        time.sleep(1)
    logger.info("Dowload End")

def gifDowload(id=None, limit=None, start=1):
    start -= 1
    info = getBasicInfo(id, limit, start)
    baseDir, headers = info["baseDir"], info["headers"]
    url, cookies = info["url"], info["cookies"]

    mkdir(baseDir) # Create save folder

    session = requests.session()
    json_obj = getUrlJsonData(session, url, headers, cookies)
    if not json_obj: return
    data = json_obj.get("data")
    titleName = data[0]["question"]["title"].encode("utf8")
    mkdir(baseDir + titleName)
    logger.warning ("Question：%s， number：%d" % (titleName, json_obj.get('paging').get('totals')))

    index = start
    while True:
        if url == '':break # is last page
        index += 1 # page number, every page has limit number

        json_obj = getUrlJsonData(session, url, headers, cookies)
        if not json_obj: return
        page = '第{}页'.format(index)
        page = baseDir + titleName + "//" + page
        mkdir(page)

        for i in json_obj.get("data"):
            saveGif(i.get('content'), session, page, headers)

        checkIsEmptyFolder(page)
        if json_obj.get('paging').get('is_end'): break # is last last page
        url = json_obj.get('paging').get('next') # next page
    logger.info("Dowload End")




if __name__ == '__main__':
    pictureDowload(533725354, 10, 1)
    # videoDowload(321570806, 10, 1)
    # gifDowload(23213328, 1, 1)

