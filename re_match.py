# encoding: utf8

import time
import re

'''
元字符 匹配内容
.       匹配除换行符以外的任意字符
\w      匹配所有普通字符(数字、字母或下划线)
\s      匹配任意的空白符(换行、制表、空格)
\d      匹配数字0-9
\n      匹配换行符
\t      匹配制表符
\b      匹配单词的结尾
^       匹配字符串的开始位置
$       匹配字符串的结尾位置
\W      匹配非字母或数字或下划线
\S      匹配非数字
\D      匹配非空白符
a|b     匹配字符 a 或字符 b
()      正则表达式分组所用符号，匹配括号内的表达式，表示一个组
[..]    匹配字符组中的字符
[^...]  匹配除了字符组中字符的所有字符

量词 用法
*       重复零次或者更多次
+       重复一次或者更多次
?      重复0次或者一次
{n}     重复n次
{n,}    重复n次或者更多次
{n,m}   重复n到m次

字符组
[0123456789]        在一个字符组里枚举所有字符，字符组里的任意一个字符和"待匹配字符"相同都视为可以匹配。
[0-9]               [0-9] 就和 [0123456789] 是一个意思
[a-z]               同样的如果要匹配所有的小写字母
[0-9a-fA-F]         以匹配数字，大小写形式的 a-f, 用来验证十六进制字符

贪婪模式非贪婪模式
正则表达式默认为贪婪匹配，也就是尽可能多的向后匹配字符，比如 {n,m} 表示匹配前面的内容出现 n 到 m 次(n 小于 m),
在贪婪模式下，首先以匹配 m 次为目标，而在非贪婪模式是尽可能少的向后匹配内容，也就是说匹配 n 次即可。
贪婪模式转换为非贪婪模式的方法很简单，在元字符后添加“?”即可实现
元字符(贪婪模式)	非贪婪模式
*       *?
+       +?
?      ??
{n,m}       {n,m}?

如果使用正则表达式匹配特殊字符时，则需要在字符前加\表示转意
* + ? ^ $ [] () {} | \

flags功能标志位
A	元字符只能匹配 ASCII码。
I	匹配忽略字母大小写。
S	使得.元字符可以匹配换行符。
M	使 ^ $ 可以匹配每一行的开头和结尾位置。

flags=re.I|re.S

'''
def test_re():
    pattern = "\d"
    string = "1abk23"

    # 将正则表达式模式编译为正则表达式对象，该对象可用于使用其match()和search()方法进行匹配
    prog = re.compile(pattern, flags=0) # 代表功能标志位，扩展正则表达式的匹配,默认0

    # match 和 search 都可以指定pos 和 end_pos
    # match 是从字符串起始位置开始匹配，如若不匹配就终止并返回None
    # search 是扫描整个字符串，寻找正则表达式模式产生匹配的第一个位置，并返回相应的MatchObject实例
    result = prog.match(string) # is equivalent to: result = re.match(pattern, string)
    result = prog.search(string) # is equivalent to: result = re.search(pattern, string)

    # 将字符串按pattern的出现次数拆分，并且字符串的其余部分作为列表的最后一个元素返回
    result = re.split('\W+', 'Words, words, words.')
    result = re.split('(\W+)', 'Words, words, words.') # 使用捕获会将分隔符也汇总入结果
    result = re.split('\W+', 'Words, words, words.', 1)
    result = re.split('[a-f]+', '0a3B9', flags=re.IGNORECASE) # 不区分大小写
    # print result

    # 匹配模式的所有出现，而不是像search()那样只匹配第一个
    result = re.findall(r"\w+ly", "He was carefully disguised but captured quickly by police.")
    # print result

    # 匹配模式的所有出现, 返回一个MatchObject的迭代器
    for m in re.finditer(r"\w+ly", "He was carefully disguised but captured quickly by police."):
        print '%02d-%02d: %s' % (m.start(), m.end(), m.group(0))

    # 将字符串的pattern替换成repl, 可以指定替换次数
    result = re.sub(r':', "=", "a:1, b:1", 1)
    print result

def math_obj():
    m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
    print m.group() # m.group(0), 获取整个匹配结果
    print m.group(1) # 获取匹配结果中的第1个捕获
    print m.group(2) # 获取匹配结果中的第2个捕获
    print m.group(1, 2) # 同时获取匹配结果中的第1，2个捕获，构成元组返回

    # (?P<...>)语法
    m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
    print m.group('first_name') # m.group(1)
    print m.group('last_name') # m.group(2)

    # 如果一个组多次匹配，则只有最后一次匹配是可访问的
    m = re.match(r"(..)+", "a1b2c3")  # Matches 3 times.
    m.group(1)

    # 返回一个包含匹配的所有子组的元组
    m = re.match(r"(\d+)\.(\d+)", "24.1632")
    print m.groups() # 可带默认值

    # 返回一个包含匹配的所有子组的字典
    m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
    print m.groupdict()

    # m.start, m.end 可以得到匹配结果的起始、终止位置
    email = "tony@tiremove_thisger.net"
    m = re.search("remove_this", email)
    print m.string[:m.start(0)] + email[m.end(0):]
    print m.span() # 返回元组(m.start, m.end)
    print m.pos, m.endpos # search()或match()的参数pos,end_pos
    print m.lastgroup # 最后匹配的捕获组的名称
    print m.re # 正则表达式对象
    print m.string  # 待匹配的字符串


def main():
    test_re()
    # math_obj()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print "[Finish {:.4f} s]".format(end_time-start_time)