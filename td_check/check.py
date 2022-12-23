# encoding: utf8

import xlrd
import xlwt
import xlsxwriter
import datetime
import re
import csv
import codecs

def get_maidian_excel_data():
    filename = u"K1埋点.xlsx"
    workbook = xlrd.open_workbook(filename)

    sheet = workbook.sheet_by_name(u"#用户数据")
    user_attr_dict = {}
    # print sheet.row_values(rowx=0)
    for i in xrange(1, sheet.nrows):
        v = sheet.row_values(rowx=i, start_colx=0, end_colx=sheet.ncols)
        if not v[0]: break
        if user_attr_dict.has_key(v[0]):
            raise Exception(u"duplicate user attr:"+v[0])
        user_attr_dict[v[0]] = v
    # print len(user_attr_dict)

    sheet = workbook.sheet_by_name(u"#公共事件属性")
    event_pub_attr_dict = {}
    # print sheet.row_values(rowx=0)
    for i in xrange(1, sheet.nrows):
        v = sheet.row_values(rowx=i, start_colx=0, end_colx=sheet.ncols)
        if not v[0]: break
        if event_pub_attr_dict.has_key(v[0]):
            raise Exception(u"duplicate event public attr:"+v[0])
        event_pub_attr_dict[v[0]] = v
    # print len(event_pub_attr_dict)

    sheet = workbook.sheet_by_name(u"#事件数据")
    # print sheet.row_values(rowx=0)
    event_dict = {}

    curr_name = None
    for i in xrange(1, sheet.nrows):
        name = sheet.cell_value(rowx=i, colx=0)
        if name:
            if event_dict.has_key(name):
                raise Exception(u"duplicate event name:"+curr_name)
            curr_name = name
            event_dict[curr_name] = sheet.row_values(rowx=i, start_colx=0, end_colx=4)
            event_dict[curr_name].append({})
            attr_info = sheet.row_values(rowx=i, start_colx=4, end_colx=8)
            if attr_info[0]:
                event_dict[curr_name][-1][attr_info[0]] = attr_info
        else:
            attr_info = sheet.row_values(rowx=i, start_colx=4, end_colx=8)
            if attr_info[0]:
                attr_dict = event_dict[curr_name][-1]
                if attr_dict.has_key(attr_info[0]):
                    raise Exception(u"duplicate event private attr:"+curr_name+", "+attr_info[0])
                attr_dict[attr_info[0]] = attr_info
            else:
                break

    event_pri_attr_dict = {}
    for event_name, event_data in event_dict.items():
        for attr_name, attr_data in event_data[-1].items():
            if event_pub_attr_dict.has_key(attr_name) and event_data[3] != u'客户端' and event_data[3] != u'虚拟账号“00000”上报':
                raise Exception(u"event private attr in public_attr_pool:"+event_name+", "+attr_name)
            if event_pri_attr_dict.has_key(attr_name):
                if event_pri_attr_dict[attr_name] != attr_data:
                    raise Exception(u"event private attr describe in conflict:"+event_name+", "+attr_name)
            else:
                event_pri_attr_dict[attr_name] = attr_data

    event_all_attr_dict = {}
    for attr_name, attr_data in event_pub_attr_dict.items():
        event_all_attr_dict[attr_name] = attr_data
    for attr_name, attr_data in event_pri_attr_dict.items():
        event_all_attr_dict[attr_name] = attr_data

    event_all_attr_name_dict = {}
    for attr_name, attr_data in event_all_attr_dict.items():
        if event_all_attr_name_dict.has_key(attr_data[1]):
            if event_all_attr_name_dict[attr_data[1]] != attr_name:
                print attr_data[1], event_all_attr_name_dict[attr_data[1]], attr_name
                raise Exception(u"event private attr show_name in duplicate:")
        else:
            event_all_attr_name_dict[attr_data[1]] = attr_name


    with open(u'user_attr_show_name.csv', 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile)
        writer.writerow(["用户属性", "显示名", "属性说明"])
        for attr_name, attr_data in user_attr_dict.items():
            writer.writerow([attr_name, attr_data[1].encode("utf8"), attr_data[4].encode("utf8")])

    with open(u'event_show_name.csv', 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile)
        writer.writerow(["事件名", "显示名", "事件说明"])
        for attr_name, attr_data in event_dict.items():
            writer.writerow([attr_name, attr_data[1].encode("utf8"), attr_data[2].encode("utf8")])

    with open(u'event_attr_show_name.csv', 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile)
        writer.writerow(["事件属性", "显示名", "属性说明"])
        for attr_name, attr_data in event_all_attr_dict.items():
            writer.writerow([attr_name, attr_data[1].encode("utf8"), attr_data[3].encode("utf8")])

get_maidian_excel_data()