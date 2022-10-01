#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import xlsxwriter
import xlrd
import time
import os
import requests
import re
import sys


'''
u'data': {
u'totalPage': 5, 
u'goods': [{
    u'sGoodsSlogan': None,
    u'limitPerOrder': u'1',
    u'propDesc': u'影哨 阿克尚',
    u'related': False,
    u'propCoverId': u'',
    u'actId': u'3',
    u'category': {
        u'subCategory': u'41',
        u'mainCategory': u'16'},
        u'dtBegin': u'2021-07-20 16:46:43',
        u'sGoodsDesc': u'影哨 阿克尚',
        u'recommend': u'19',
        u'valiDate': [{
            u'code': u'27623',
            u'oldPrice': u'4500',
            u'dtLimitedEnd': u'0000-00-00 00:00:00',
            u'pic': u'http://ossweb-img.qq.com/images/daoju/app/lol/rectangle/N-lol-1-100000-149088.jpg?_t=1626925910',
            u'isFunc': 0,
            u'gameCode': u'166',
            u'gold_price_rush': 0,
            u'twin_dq_price': 0,
            u'dq_price_rush': 0,
            u'twin_code': u'',
            u'acctPlat': u'0',
            u'twin_price': 0,
            u'isskin': 0,
            u'label': 1,
            u'iGoldPrice': u'6300',
            u'iAmsType': 0,
            u'sCustomLabel': [],
            u'rushPrice': 0,
            u'iOrgPrice': u'4500',
            u'pinPrice': 0,
            u'supportCart': u'1',
            u'sendType': 1,
            u'dtLimitedBegin': u'0000-00-00 00:00:00',
            u'rushEnd': u'0000-00-00 00:00:00',
            u'flashSaleTimeInfo': [],
            u'award': {
                u'list': [{
                    u'sItemId': u'3395',
                    u'sDesc': u'',
                    u'iShowNum': u'1',
                    u'iSupportPayType': 1,
                    u'sMrmsGid': u'1389698',
                    u'giftType': u'appJifen',
                    u'sAmsModId': u'374273',
                    u'destinationUrl': u'',
                    u'iActiveId': 753,
                    u'iAmsType': u'-106',
                    u'sMarketMark': u'实付满5元抽免单，多买多抽',
                    u'sAmsBiz': u'dj',
                    u'iPacketNum': u'1',
                    u'channel': u'app',
                    u'sMrmsPid': u'2164921',
                    u'bPresale': u'0',
                    u'sMrmsGiftId': u'IEGAMS-339085-374273',
                    u'sGoodsPic': None,
                    u'sAmsActId': u'339085',
                    u'iQuantity': u'1',
                    u'iUidType': u'1',
                    u'sGoodsName': u'道聚城LOL抽免单',
                    u'iSendDst': u'1',
                    u'iGoodsId': u'436951_105042_1_dj_1',
                    u'iActType': 2,
                    u'sActivityDesc': u'',
                    u'iPrice': u'0',
                    u'iSendType': u'109'
                }]
            },
            u'lTotalBuyNum': 0,
            u'fingerprint': u'1-166',
            u'pinEnd': u'0000-00-00 00:00:00',
            u'day': u'永久',
            u'picMid': u'http://ossweb-img.qq.com/images/daoju/app/lol/medium/N-lol-1-100000-149088.jpg?_t=1626925933',
            u'rushBegin': u'0000-00-00 00:00:00',
            u'name': u'影哨 阿克尚',
            u'waterMark': u'',
            u'iDqPrice': u'4500',
            u'supportPresent': u'1',
            u'flashSaleLimit': 0,
            u'pinBegin': u'0000-00-00 00:00:00',
            u'curPrice': u'4500',
            u'flashSaleLimitInfo': 0,
            u'pinDqPrice': 0
        }],
        u'heroSkin': [],
        u'type': u'3',
        u'propImg2': u'',
        u'propVideoId': u'',
        u'propId': u'27623',
        u'isCombinPkg': 0,
        u'busId': u'lol',
        u'sAdText': None,
        u'propName': u'影哨 阿克尚',
        u'totalLimit': u'0',
        u'dtEnd': u'2030-12-31 23:59:59',
        u'propImg': u'http://ossweb-img.qq.com/images/daoju/app/lol/rectangle/N-lol-1-100000-149088.jpg?_t=1626925910'
    }, 
'''

def get_last_xml_data():
    dir_name, file_name = os.path.split(os.path.abspath(sys.argv[0]))
    xml_file_name = u"LOLHeroList.xlsx"
    xml_file_path = os.path.join(dir_name, xml_file_name)

    if not os.path.exists(xml_file_path):
        # raise Exception("the file is not exist")
        return None, None

    workbook = xlrd.open_workbook(xml_file_path, on_demand=True)
    sheet = workbook.sheet_by_index(0)
    start_row, start_col = 1, 1
    head_list = sheet.row_values(start_row, start_col)
    data_dict = {}
    for i in range(start_row+1, sheet.nrows):
        info = sheet.row_values(i, start_col)
        data_dict[int(info[0])] = info
    return head_list, data_dict

def get_lol_hero_data():
    # 道聚城
    url = "https://apps.game.qq.com/daoju/v3/api/hx/goods/app/v71/GoodsListApp.php"
    payload = {
        "appSource": 'pc', # 请求来源
        "plat":1, # 平台，0 ios ，1android
        "output_format": 'json',# 接口返回类型，json还是jsonp
        "biz": "lol", # 业务
        "view": 'biz_cate', # 接口请求类型，全部:biz_portal;大类:biz_cate;子类:biz_sub_cate;指定物品:goods_detail
        "page": 1, # 当前页码
        "pageSize": 5, # 每页数量
        "orderby": "dtShowBegin",
        "ordertype": "dtShowBegin",
        "cate":16,
        "_": int(time.time() * 1000)
        # "iGoodsId": iSeqId, # 道具ID
        # "flows":iSeqId,
    }
    temp_data = requests.get(url, params=payload).json()["data"]
    shop_hero_dict = {}
    for i in xrange(1, temp_data["totalPage"]+1):
        payload["page"] = i
        data = requests.get(url, params=payload).json()["data"]
        for hero in data["goods"]:
            hero = hero["valiDate"][0]
            shop_hero_dict[hero["gameCode"]] = (hero["name"], hero["iGoldPrice"])

    # 官方, 官方英雄价格有延迟
    url = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"
    std_hero_list = requests.get(url).json()["hero"]

    if len(shop_hero_dict) != len(std_hero_list):
        print len(shop_hero_dict), len(std_hero_list)
        raise Exception("the hero num not equal")

    hero_list, hero_dict = [], {}
    for std_hero in std_hero_list:
        hero_id = std_hero["heroId"]
        shop_hero = shop_hero_dict[hero_id]
        hero_title, hero_name = shop_hero[0].split(None, 1)
        hero_price = shop_hero[1]
        hero_info = [hero_id, hero_title, hero_name, hero_price]
        hero_list.append(hero_info)
        hero_dict[hero_id] = hero_info

    return hero_list, hero_dict

def build_new_xml_file(hero_list, old_xml_dict=None):
    dir_name, file_name = os.path.split(os.path.abspath(sys.argv[0]))
    xml_file_name = u"LOLHeroList.xlsx"
    workbook = xlsxwriter.Workbook(xml_file_name)
    sheet = workbook.add_worksheet(u'英雄列表')

    start_row, start_col = 1, 1
    headings = [
        u"英雄ID", u"英雄标签", u"英雄名", u"是否拥有", u"价格",
        u"碎片数量", u"成品数量", u"碎片价格", u"成品价格", u"合成消耗",
        u"剩余价值",
    ]
    sheet.write_row(start_row, start_col, headings)
    head_num = len(headings)
    index = start_row + 2
    for hero in hero_list:
        data = [''] * head_num
        # 英雄id, 英雄标签, 英雄名称
        data[0], data[1], data[2] = int(hero[0]), hero[1], hero[2]
        data[4] = int(hero[3]) # 英雄价格
        if old_xml_dict and old_xml_dict[data[0]]:
            data[3] = old_xml_dict[data[0]][3] # 是否拥有
            data[5] = old_xml_dict[data[0]][5] # 碎片数量
            data[6] = old_xml_dict[data[0]][6] # 成品数量
        else:
            data[3] = 0
            data[5] = 0
            data[6] = 0
        data[7] = "=F{row}/5".format(row=index)# 碎片价格,价格字段在F列
        data[8] = "=F{row}/2".format(row=index)# 成品价格,价格字段在F列
        data[9] = data[7] + "*3" # 合成消耗
        data[10] = "=if(E{row}=1,G{row}*I{row}+H{row}*J{row},if(G{row}=0,-F{row}," \
                    "(G{row}-1)*I{row}-K{row}))".format(row=index)
        sheet.write_row(index-1, start_col, data)
        index += 1
    # 汇总
    sheet.write("D1", "=sum(L{}:L{})".format(start_row+2, index-1)) # 所有碎片价值
    sheet.write("E1", 0) # 已有蓝色精粹
    sheet.write("F1", "=D1+E1") # 折算成蓝色精粹

    workbook.close()


def main():
    head_list, data_dict = get_last_xml_data()
    hero_list, hero_dict = get_lol_hero_data()
    build_new_xml_file(hero_list, data_dict)

if __name__ == '__main__':
    main()
