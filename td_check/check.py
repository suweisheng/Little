# encoding: utf8

import re

def get_game_code_data():
    file_path = u"Y:/nova/server/service/agent/td_log.lua"
    content_lines = ""
    with open(file_path, 'r') as f:
        content_lines = f.readlines()
    
    user_prop_list = list()
    user_prop_flag = None
    event_prop_list = list()
    event_prop_flag = None

    for line in content_lines:
        if "local RoleUserProp" in line:
            user_prop_flag = True
        elif "local RoleEventProp" in line:
            event_prop_flag = True
        elif line == "}\n":
            user_prop_flag = None
            event_prop_flag = None
        elif user_prop_flag:
            ret = re.search(u'(\w+)\s*=\s*(\d+)', line)
            if not ret:
                raise Exception("user_prop match error:"+line)
            user_prop_list.append((ret.group(1), ret.group(2)))
        elif event_prop_flag:
            ret = re.search(u'(\w+)\s*=\s*{(.*)}', line)
            if not ret:
                raise Exception("event_prop match error:"+line)
            prop_list = re.findall(u'"(.+)"', ret.group(2))
            event_prop_list.append((ret.group(1), prop_list))

    print user_prop_list
    print event_prop_list




get_game_code_data()
