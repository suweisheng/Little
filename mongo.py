# encoding: utf-8

import pymongo

def mongo_test():
    # connect db
    mongo_conn = "mongodb://haojisheng:wpx_Hjs45963@192.168.170.5:27017"
    client = pymongo.MongoClient(mongo_conn)
    
    # db = client["nova_vs50012"]
    # collection = db["t_VServerData"]
    # all_data = collection.find()
    # for data in all_data:
    #     print data

    print client.drop_database("nova_vs50012")
    print client.drop_database("nova_game10012")
    db = client["nova_login"]
    collection = db["t_LoginRolesInfo"]
    filter = {u"game_id":10012}
    collection.delete_many(filter)
    # all_data = collection.find()
    # for data in all_data:
    #     print data["game_id"], data["server_id"], data["name"]


def mongo_test2():
    client = pymongo.MongoClient("mongodb://haojisheng:wpx_Hjs45963@192.168.170.5:27017")
    # client = pymongo.MongoClient('192.168.170.5:27017', username='haojisheng', password='wpx_Hjs45963',)
    # client.close()

    # print client.address
    # print client.list_database_names()
    # print client.server_info()
    # client.drop_database("sws_test") # 谨慎使用

    # 创建新数据库, 数据库创建后要创建集合(数据表)并插入一个文档(记录),数据库才会真正创建
    # db = client.get_database("sws_test")
    # collection = db["test"]
    # data = {"name":"sws", 'score':20}
    # collection.insert_one(data)

    db = client.sws_test
    # db = db = client["sws_test"]
    # db = client.get_database("sws_test")
    # print db.list_collection_names()
    # print db.name


    collection = db.test
    # collection = db["test"]
    # collection = db.get_collection("test")
    print collection.name
    print collection.full_name
    collection.database



    # data = {"_id":1, "name":"a", 'score':20}
    # data_list = [{"_id":3, "name":"a", 'score':20}, {"_id":5, "name":"b", 'score':30}]
    # collection.insert_one(data)
    # collection.insert_many(data_list)


    # query_one_data = collection.find_one() # {} or nil
    # query_one_data = collection.find_one({"name":"a"}, {"_id":1})
    # print query_one_data

    # query_many_data = collection.find({}) # {} or nil
    # query_many_data = collection.find({"name":"a"})
    # query_many_data = collection.find({"name":"a"}).limit(1) # 对查询结果设置指定条数的记录可以使用 limit() 方法
    # query_many_data = collection.find({"name":"a"}, {"_id":0, "score":1}) # 第1个参数是条件,第2个是过滤字段
    # 除了 _id，你不能在一个对象中同时指定 0 和 1，如果你设置了一个字段为 0，则其他都为 1，反之亦然
    # for x in query_many_data: print x

    # find_one_and_replace({'x': 1}, {'y': 1})
    # find_one_and_update({'_id': 665}, {'$inc': {'count': 1}, '$set': {'done': True}})

    # MongoDB中条件操作符有：
    # (>) 大于 - $gt
    # (<) 小于 - $lt
    # (>=) 大于等于 - $gte
    # (<= ) 小于等于 - $lte
    # query_many_data = collection.find({"score":{"$gt":25}})
    # for x in query_many_data: print x

    # $regex为模糊查询的字符串提供正则表达式功能
    # query_many_data = collection.find({"name":{"$regex":"^a"}}).limit(1)
    # for x in query_many_data: print x


    # 第一个参数为查询的条件，第二个参数为要修改的字段, 可用于新增字段
    # collection.update_one({"name":"b"}, {"$set":{"score2":100}})
    # x = collection.update_many({"name":"a"}, {"$set":{"score2":50}})
    # print x.modified_count

    # collection.delete_one({"name":"b"})
    # collection.delete_many({"name":{"$regex":"^a"}})
    # collection.delete_many({}) # 删除所有

    # collection.drop()





    


    # collection = db.t_Role # or: collection = db["t_Role"]
    

mongo_test()