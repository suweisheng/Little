# encoding: utf8

import xlrd
import xlwt
import xlsxwriter
import datetime
import re

def get_maidian_excel_data():
    filename = u"K1埋点.xlsx"
    workbook = xlrd.open_workbook(filename)

    sheet1 = workbook.sheet_by_name(u"#用户数据")
    data_dict = {}
    # print sheet1.row_values(rowx=0)
    for i in xrange(1, sheet1.nrows):
        v = sheet1.row_values(rowx=i, start_colx=0, end_colx=sheet1.ncols)
        if not v[0]: break
        if data_dict.has_key(v[0]):
            raise Exception(u"duplicate user attr:"+v[0])
        data_dict[v[0]] = v
    # print len(data_dict)

    sheet2 = workbook.sheet_by_name(u"#公共事件属性")
    data_dict = {}
    # print sheet2.row_values(rowx=0)
    for i in xrange(1, sheet2.nrows):
        v = sheet2.row_values(rowx=i, start_colx=0, end_colx=sheet2.ncols)
        if not v[0]: break
        if data_dict.has_key(v[0]):
            raise Exception(u"duplicate public attr:"+v[0])
        data_dict[v[0]] = v
    # print len(data_dict)

    sheet3 = workbook.sheet_by_name(u"#事件数据")
    # print sheet1.row_values(rowx=0)
    event_dict = {}
    all_attr_dict = data_dict.copy()
    public_attr_dict = data_dict
    curr_name = None
    for i in xrange(1, sheet3.nrows):
        name = sheet3.cell_value(rowx=i, colx=0)
        if name :
            if event_dict.has_key(name):
                raise Exception(u"duplicate event name:"+curr_name)
            curr_name = name
            event_dict[curr_name] = sheet3.row_values(rowx=i, start_colx=0, end_colx=4)
            event_dict[curr_name].append({})
            attr_dict = event_dict[curr_name][-1]
            attr_info = sheet3.row_values(rowx=i, start_colx=4, end_colx=8)
            if public_attr_dict.has_key(attr_info[0]):
                if event_dict[curr_name][3] != u'客户端':
                    raise Exception(u"duplicate event attr on public:"+curr_name+"=>"+attr_info[0])
            if all_attr_dict.has_key(attr_info[0]):
                if all_attr_dict[attr_info[0]] != attr_info:
                    raise Exception(u"duplicate event attr desc:"+curr_name+"=>"+attr_info[0])
            else:
                all_attr_dict[attr_info[0]] = attr_info

            attr_dict[attr_info[0]] = attr_info
        else:
            attr_info = sheet3.row_values(rowx=i, start_colx=4, end_colx=8)
            if attr_info[0]:
                attr_dict = event_dict[curr_name][-1]
                if attr_dict.has_key(attr_info[0]):
                    raise Exception(u"duplicate event attr:"+curr_name+"=>"+attr_info[0])
                if public_attr_dict.has_key(attr_info[0]):
                    if event_dict[curr_name][3] != u'客户端':
                        raise Exception(u"duplicate event attr on public:"+curr_name+"=>"+attr_info[0])
                if all_attr_dict.has_key(attr_info[0]):
                    if all_attr_dict[attr_info[0]] != attr_info:
                        raise Exception(u"duplicate event attr desc:"+curr_name+"=>"+attr_info[0])
                else:
                    all_attr_dict[attr_info[0]] = attr_info
                attr_dict[attr_info[0]] = attr_info
            else:
                break

get_maidian_excel_data()