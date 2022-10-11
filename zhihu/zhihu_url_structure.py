# url地址
URL = "https://www.zhihu.com/api/v4/questions/281282523/answers?include=content&limit=2&offset=0&sort_by=default"

# 相关中英翻译
word = {
    "is_start" : "首页",
    "is_end" : "尾页",
    "previous" : "上一页",
    "total" : "总回答数量",
    "data" : "内容",
    "limit" : "限制每次访问回答数量",
    "sort_by" : "排序规则",
    "offset" : "偏移量",
    "relationship" : "关系",
    "title" : "标题",
}

# respose 数据
json_data = {
    'paging':{
        "is_start":True,
        "is_end":False,
        "total":7688,
        "previous":"https://www.zhihu.com/api/v4/questions/281282523/answers?include=content\u0026limit=2\u0026offset=0\u0026sort_by=default",
        "next":"https://www.zhihu.com/api/v4/questions/281282523/answers?include=content\u0026limit=2\u0026offset=2\u0026sort_by=default",
    },
    'data':[
        {
            "id":430150733,
            "type":"answer",
            "answer_type":"normal",
            "is_copyable":True,
            "is_collapsed":False,
            "created_time":1530328732,
            "updated_time":1534987991,
            "url":"https://www.zhihu.com/api/v4/answers/430150733",
            "question":{
                "type":"question",
                "id":281282523,
                "title":"哪些表情包让你看一次笑一次？",
                "question_type":"normal",
                "created":1529160325,
                "updated_time":1546676490,
                "url": "https://www.zhihu.com/api/v4/questions/281282523",
                "relationship":{}
            },
            "author": {
                "id":"0b445873bfe0a1bb050a42b37d275c37",
                "url_token":"qdqzxgs123456",
                "name":"崧高维岳",
                "avatar_url":"https://pic2.zhimg.com/v2-eddd55649d3412a2182cced1679ce776_is.jpg",
                "avatar_url_template":"https://pic2.zhimg.com/v2-eddd55649d3412a2182cced1679ce776_{size}.jpg",
                "is_org":False,
                "type":"people",
                "url":"https://www.zhihu.com/api/v4/people/0b445873bfe0a1bb050a42b37d275c37",
                "user_type":"people",
                "headline":"喝酒 烫头 不抽烟",
                "badge":[],
                "gender":1,
                "is_advertiser":False,
                "is_privacy":False
            },
            "extras":"",
            "content":r"\u003cp\u003e\ src=\"https://pic3.zhimg.com/50/v2-f3c3cb4a80b1ead78ec9f0716d1dcc9d_hd.jpg\" data-rawwidth=\"50\" data-rawheight=\ ...", # html数据
            #  picture_list = re.findall(r'data-original="(.+?)"', data.get('content')) # 寻到图片集
            # ['https://pic4.zhimg.com/v2-db89f1a285ddeca2d9ea902443b019a2_r.jpg\',]
            #
            # video_id_list = re.findall(r'data-lens-id="(\d+)"', i.get("content")) # 寻找视频集 m3u8协议
            # ['1138233741104332800\', '1139612838325886976\',]
            # video_api = 'https://lens.zhihu.com/api/videos/{0}'; video_api.format(1138233741104332800) -> https://lens.zhihu.com/api/videos/1138233741104332800
            # url = https://lens.zhihu.com/api/videos/1138233741104332800
            # 下载时必须使用请求表头:
                # 'Referer' : 'https://v.vzuu.com/video/{0}',
                # 'Origin' : 'https://v.vzuu.com',
                # 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                # 'Content-Type' : 'application/json',
            # 根据视频品质 [ld, sd, hd] 选择对应的 player_url 下载 

            #  gif_list = re.findall(r'data-actualsrc="(.+?)"', data.get('content')) # 寻到gif集
            # gif_list = [x for x in picList if ".gif" in x]
            # ['https://pic4.zhimg.com/50/v2-c4016f3e96024155f251840f4eb3296a_hd.gif',]
        }
    ]
}

video_url = "https://lens.zhihu.com/api/videos/1138233741104332800"
json = {
    "title": "",
    "cover_info": {
        "width": 0,
        "thumbnail": "https://pic4.zhimg.com/v2-e5603d68c13e7374d1c18bbb892bccfb.jpg",
        "height": 0
    },
    "duration": 11.03,
    "id": 1138233741104332800,
    "misc_info": {},
    "playlist":{
        "ld": {
            "format": "mp4",
            "play_url": "https://vdn1.vzuu.com/LD/b9807bf2-afbc-11e9-938e-0a580a42a3d7.mp4?disable_local_cache=1&bu=com&expiration=1567754456&auth_key=1567754456-0-0-1feb147c663fc02729cf63afcaff609b&f=mp4&v=hw",
            "height": 640,
            "width": 360,
            "fps": 25.0,
            "duration": 11.03,
            "bitrate": 520.493,
            "size": 717631
        },
        "hd": {
            "format": "mp4",
            "play_url": "https://vdn1.vzuu.com/HD/b9807bf2-afbc-11e9-938e-0a580a42a3d7.mp4?disable_local_cache=1&bu=com&expiration=1567754456&auth_key=1567754456-0-0-5b5a6cd93c198287bdf69b38c4bf24ed&f=mp4&v=hw",
            "height": 1280,
            "width": 720,
            "fps": 25.0,
            "duration": 11.03,
            "bitrate": 2034.619,
            "size": 2805231
        },
        "sd": {
            "format": "mp4",
            "play_url": "https://vdn1.vzuu.com/SD/b9807bf2-afbc-11e9-938e-0a580a42a3d7.mp4?disable_local_cache=1&bu=com&expiration=1567754456&auth_key=1567754456-0-0-47959ebe39ecd1ffb733a8f28d33687a&f=mp4&v=hw",
            "height": 848,
            "width": 478,
            "fps": 25.0,
            "duration": 11.03,
            "bitrate": 900.855,
            "size": 1242055
        }
    },
}