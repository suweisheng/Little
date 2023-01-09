# encoding: utf8

import xlrd
import xlwt
import xlsxwriter
import datetime
import re
import csv
import codecs
import os
import sys
import json

ENCODING = 'utf8'
if sys.platform == 'win32':
    ENCODING = 'gbk'
reload(sys)
sys.setdefaultencoding(ENCODING)

def get_file_path(file_name, is_keyword=None, is_full_path=None):
    root_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_path = None
    if is_keyword:
        for dirpath, dirnames, filenames in os.walk(root_path):
            for name in filenames:
                if file_name in name.decode("gbk"):
                    file_path = os.path.join(root_path, name)
    else:
        file_path = os.path.join(root_path, file_name)
    return file_path

def get_td_excel_data():
    filename = get_file_path(u"K1埋点.xlsx", None, True)
    workbook = xlrd.open_workbook(filename)

    sheet = workbook.sheet_by_name(u"#用户数据")
    user_attr_dict = {}
    for i in xrange(1, sheet.nrows):
        v = sheet.row_values(rowx=i, start_colx=0, end_colx=sheet.ncols)
        if not v[0]: break
        if user_attr_dict.has_key(v[0]):
            raise Exception(u"duplicate user attr: "+v[0])
        user_attr_dict[v[0]] = v
    # print sheet.row_values(rowx=0)
    # print len(user_attr_dict)

    sheet = workbook.sheet_by_name(u"#公共事件属性")
    event_pub_attr_dict = {}
    for i in xrange(1, sheet.nrows):
        v = sheet.row_values(rowx=i, start_colx=0, end_colx=sheet.ncols)
        if not v[0]: break
        if event_pub_attr_dict.has_key(v[0]):
            raise Exception(u"event public attr duplicate: "+v[0])
        event_pub_attr_dict[v[0]] = v
    # print sheet.row_values(rowx=0)
    # print len(event_pub_attr_dict)

    sheet = workbook.sheet_by_name(u"#事件数据")
    event_dict = {}
    curr_name = None
    for i in xrange(1, sheet.nrows):
        name = sheet.cell_value(rowx=i, colx=0)
        if name:
            if event_dict.has_key(name):
                raise Exception(u"event name duplicate: "+curr_name)
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
                    raise Exception(u"event private attr duplicate: "+curr_name+", "+attr_info[0])
                attr_dict[attr_info[0]] = attr_info
            else:
                break
    # print sheet.row_values(rowx=0)
    # print len(event_dict)


    event_pri_attr_dict = {}
    for event_name, event_data in event_dict.items():
        for attr_name, attr_data in event_data[-1].items():
            if event_pub_attr_dict.has_key(attr_name):
                if event_data[3] != u'客户端' and event_data[3] != u'虚拟账号“00000”上报':
                    raise Exception(u"event private attr in public_attr_pool:"+event_name+", "+attr_name)
            if event_pri_attr_dict.has_key(attr_name):
                if event_pri_attr_dict[attr_name] != attr_data:
                    err_msg = u"========>\n{}\n{}".format(
                        json.dumps(attr_data).decode('unicode_escape'),
                        json.dumps(event_pri_attr_dict[attr_name]).decode('unicode_escape')
                    )
                    raise Exception(u"event private attr describe in conflict:\n"+err_msg)
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
            err_msg = u"{}; {}; {}".format(attr_data[1], event_all_attr_name_dict[attr_data[1]], attr_name)
            raise Exception(u"event private attr show_name in duplicate: "+err_msg)
        else:
            event_all_attr_name_dict[attr_data[1]] = attr_name

    excel_data = dict(
        event_dict = event_dict,
        user_attr_dict = user_attr_dict,
        event_pub_attr_dict = event_pub_attr_dict,
        event_all_attr_dict = event_all_attr_dict,
    )

    return excel_data


def build_csv_file(excel_data):
    user_attr_dict = excel_data["user_attr_dict"]
    with open(get_file_path(u'user_attr_show_name.csv'), 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile)
        writer.writerow(["用户属性", "显示名", "属性说明"])
        for attr_name, attr_data in user_attr_dict.items():
            writer.writerow([attr_name, attr_data[1].encode("utf8"), attr_data[4].encode("utf8")])

    event_dict = excel_data["event_dict"]
    with open(get_file_path(u'event_show_name.csv'), 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile)
        writer.writerow(["事件名", "显示名", "事件说明"])
        for attr_name, attr_data in event_dict.items():
            writer.writerow([attr_name, attr_data[1].encode("utf8"), attr_data[2].encode("utf8")])

    event_all_attr_dict = excel_data["event_all_attr_dict"]
    with open(get_file_path(u'event_attr_show_name.csv'), 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile)
        writer.writerow(["事件属性", "显示名", "属性说明"])
        for attr_name, attr_data in event_all_attr_dict.items():
            writer.writerow([attr_name, attr_data[1].encode("utf8"), attr_data[3].encode("utf8")])

def get_td_lua_data():
    filename = "Y:/nova/server/service/agent/td_log.lua"
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    event_dict = {"openid_register":[], "device_register":[],}
    user_attr_dict = {}
    event_pub_attr_dict = {}
    start_flag = None
    for i in xrange(len(lines)):
        text = lines[i]
        line_num = str(i + 1)
        if text.startswith("local RoleEventProp"):
            start_flag = "event"
        elif text.startswith("local RoleUserProp"):
            start_flag = "user_attr"
        elif text.startswith("    properties[\"#ip\"]"):
            start_flag = "event_public_attr"
        elif start_flag:
            if text.startswith("}") or text.startswith("\n"):
                start_flag = None; continue
            if start_flag == "event":
                event_name = re.match("\s*(\w+)\s*=", text).group(1)
                if event_dict.has_key(event_name):
                    raise Exception("lua event name duplicate: "+line_num+", "+event_name)
                event_dict[event_name] = re.findall('\"(\w+)\"', text)
                event_dict[event_name].sort()
            elif start_flag == "user_attr":
                attr_list = re.findall('(\w+)\s*=\s*([01])', text)
                for attr in attr_list:
                    name = attr[0]
                    if user_attr_dict.has_key(name):
                        raise Exception("lua user attr duplicate: "+line_num+", "+name)
                    user_attr_dict[name] = attr[1]
            elif start_flag == "event_public_attr":
                name = re.search('\[\"(\w+)\"\]', text).group(1)
                if event_pub_attr_dict.has_key(name):
                    raise Exception("lua event public attr duplicate: "+line_num+", "+name)
                event_pub_attr_dict[name] = 1

    lua_data = dict(
        event_dict = event_dict,
        user_attr_dict = user_attr_dict,
        event_pub_attr_dict = event_pub_attr_dict,
    )

    return lua_data

def compaire_excel_lua(excel_data, lua_data):
    excel_srv_event_dict = {}
    for event_name, event_data in excel_data["event_dict"].items():
        if event_data[3] != u'客户端' and event_data[3] != u'虚拟账号“00000”上报':
            attr_list = []
            for name in event_data[-1]:
                if "." not in name:
                    attr_list.append(str(name))
            attr_list.sort()
            excel_srv_event_dict[str(event_name)] = attr_list
    lua_srv_event_dict = lua_data["event_dict"]
    miss_list, surplus_list = [], []
    for event_name, event_data in excel_srv_event_dict.items():
        if not lua_srv_event_dict.has_key(event_name):
            miss_list.append(event_name)
    for event_name, event_data in lua_srv_event_dict.items():
        if not excel_srv_event_dict.has_key(event_name):
            surplus_list.append(event_name)
    if miss_list or surplus_list:
        err_msg = u"========>\nmiss_list:{}\nsurplus_list:{}".format(
            json.dumps(miss_list).decode('unicode_escape'),
            json.dumps(surplus_list).decode('unicode_escape')
        )
        raise Exception("lua_event_num and maidian_event_num do not match:\n"+err_msg)
    for event_name, event_data in excel_srv_event_dict.items():
        if lua_srv_event_dict[event_name] != event_data:
            err_msg = u"========>\n{}\n{}\n{}".format(
                event_name,
                json.dumps(lua_srv_event_dict[event_name]).decode('unicode_escape'),
                json.dumps(event_data).decode('unicode_escape')
            )
            raise Exception("lua event and maidian event conflict:\n"+err_msg)

    temp = excel_data["user_attr_dict"]
    excel_user_attr_dict = {}
    update_type = {"user_setOnce":"0", "user_set":"1"}
    for attr_name, attr_data in temp.items():
        if "." not in attr_name:
            excel_user_attr_dict[str(attr_name)] = update_type.get(attr_data[3] ,"NOne")
    lua_user_attr_dict = lua_data["user_attr_dict"]
    miss_list, surplus_list = [], []
    for attr_name, _ in excel_user_attr_dict.items():
        if not lua_user_attr_dict.has_key(attr_name):
            miss_list.append(attr_name)
    for attr_name, _ in lua_user_attr_dict.items():
        if not excel_user_attr_dict.has_key(attr_name):
            surplus_list.append(attr_name)
    if miss_list or surplus_list:
        err_msg = u"========>\nmiss_list:{}\nsurplus_list:{}".format(
            json.dumps(miss_list).decode('unicode_escape'),
            json.dumps(surplus_list).decode('unicode_escape')
        )
        raise Exception("lua_user_attr_num and maidian_user_attr_num do not match:\n"+err_msg)
    type_err_list = []
    for attr_name, update_type in lua_user_attr_dict.items():
        if excel_user_attr_dict[attr_name] != update_type:
            type_err_list.append(attr_name)
    if type_err_list:
        err_msg = u"========>\n{}".format(json.dumps(type_err_list).decode('unicode_escape'))
        raise Exception("lua_user_attr and maidian_user_attr update_type do not match:\n"+err_msg)

    temp = excel_data["event_pub_attr_dict"]
    excel_event_pub_attr_dict = {}
    for name in temp:
        if "." not in name:
            excel_event_pub_attr_dict[name] = 1
    lua_event_pub_attr_dict = lua_data["event_pub_attr_dict"]
    miss_list, surplus_list = [], []
    for event_name, _ in excel_event_pub_attr_dict.items():
        if not lua_event_pub_attr_dict.has_key(event_name):
            miss_list.append(event_name)
    for event_name, _ in lua_event_pub_attr_dict.items():
        if not excel_event_pub_attr_dict.has_key(event_name):
            surplus_list.append(event_name)
    if miss_list or surplus_list:
        err_msg = u"========>\nmiss_list:{}\nsurplus_list:{}".format(
            json.dumps(miss_list).decode('unicode_escape'),
            json.dumps(surplus_list).decode('unicode_escape')
        )
        raise Exception("lua_event_pub_attr_num and maidian_event_pub_attr_num do not match\n"+err_msg)

def check_meta_data(excel_data):
    filename = get_file_path(u"猎码计划_埋点方案", True)
    if not filename:
        return

    workbook = xlrd.open_workbook(filename)

    sheet = workbook.sheet_by_name(u"#事件数据")
    event_name_list = []
    event_attr_name_dict = {}
    for i in xrange(1, sheet.nrows):
        event_name = sheet.cell_value(rowx=i, colx=0)
        event_attr_name = sheet.cell_value(rowx=i, colx=4)
        if event_name:
            event_name_list.append(event_name)
        if not event_attr_name_dict.has_key(event_attr_name):
            event_attr_name_dict[event_attr_name] = 1
        
    sheet = workbook.sheet_by_name(u"#用户数据")
    user_name_list = sheet.col_values(colx=0, start_rowx=1, end_rowx=sheet.nrows)


    miss_list = []
    for event_name, event_data in excel_data["event_dict"].items():
        if event_name not in event_name_list:
            miss_list.append((event_name, event_data[1]))
    if miss_list:
        err_msg = "=======> not trigger event log:\n"
        for i in xrange(len(miss_list)):
            err_msg = err_msg + u"{}.{} ({})\n".format(i, miss_list[i][0], miss_list[i][1])
        print err_msg

    miss_list = []
    for attr_name, attr_data in excel_data["user_attr_dict"].items():
        if attr_name not in user_name_list:
            miss_list.append((attr_name, attr_data[1]))
    if miss_list:
        err_msg =  "=======> not trigger user attr log:\n"
        for i in xrange(len(miss_list)):
            err_msg = err_msg +  u"{}.{} ({})\n".format(i, miss_list[i][0], miss_list[i][1])
        print err_msg

    miss_list = []
    for attr_name, attr_data in excel_data["event_all_attr_dict"].items():
        if not event_attr_name_dict.has_key(attr_name):
            miss_list.append((attr_name, attr_data[1]))
    if miss_list:
        err_msg =  "=======> not trigger event attr log:\n"
        for i in xrange(len(miss_list)):
            err_msg = err_msg +  u"{}.{} ({})\n".format(i, miss_list[i][0], miss_list[i][1])
        print err_msg


excel_data = get_td_excel_data()
build_csv_file(excel_data)

lua_data = get_td_lua_data()
compaire_excel_lua(excel_data, lua_data)

check_meta_data(excel_data)