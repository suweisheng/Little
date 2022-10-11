# encoding: utf8

import csv
# 所谓的CSV(逗号分隔值)格式是电子表格和数据库最常用的导入和导出格式

def test_w_csv():
    # delimiter 指定分隔符，默认为逗号，这里指定为空格
    # quotechar 表示引用符
    # 其中，quotechar 是引用符，当一段话中出现分隔符的时候，用引用符将这句话括起来，以能排除歧义。
    # writerow 单行写入，列表格式传入数据
    # 'wb' 可以逐行写入，用'w'否则会出现空行现象
    with open('eggs.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    with open('aggs.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        # 注意传入数据的格式为列表元组格式
        writer.writerows([('hello','world'), ('I','love','you')])

    with open('names.csv', 'wb') as csvfile:
        # 写入字段名，当做表头
        writer = csv.DictWriter(csvfile, fieldnames=['first_name', 'last_name'])
        writer.writeheader()
        # 多行写入
        writer.writerows([{'first_name': 'Baked', 'last_name': 'Beans'},{'first_name': 'Lovely', 'last_name': 'Spam'}])
        # 单行写入
        writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

def test_r_csv():
    with open('eggs.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))

    with open('names.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['first_name'], row['last_name'])

def main():
    test_w_csv()
    test_r_csv()

if __name__ == "__main__":
    main()