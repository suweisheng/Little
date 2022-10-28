# encoding: utf8

import urllib2
from sys import stdout, argv
from time import time

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'sec-ch-ua': '"Chromium";v="106", "Not;A=Brand";v="99", "Google Chrome";v="106.0.5249.119"',
    'host': 'translate.googleapis.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

def check_ip(ip):
    url = 'http://{ip}/translate_a/single?client=gtx&sl=en&tl=fr&q=a'.format(ip=ip)
    try:
        start_time = time()
        request = urllib2.Request(url=url, data=None, headers=HEADERS)
        response = urllib2.urlopen(url=request, timeout=3)
        end_time = time()
        response.close()
    except Exception as e:
        return str(e)
    return end_time - start_time

if len(argv) == 1:
    ips = ["142.250.4.90", "142.250.107.90", "142.250.28.90", "172.217.195.90", "142.250.126.90"]
else:
    try:
        with open(argv[1], 'r') as file:
            ips = list(set(map(str.strip, file)))
    except Exception as e:
        print 'Failed to open file {}. Reason: {}'.format(argv[1], e)
    

avaliable = []
total = len(ips)
count = 1
for ip in ips:
    # print 'Checking {ip} ...'.format(ip=ip),
    result = check_ip(ip)
    if isinstance(result, str):
        # print 'Error:', result
        pass
    else:
        ms = round(result * 1000)
        # print '{ms}ms'.format(ms=ms)
        avaliable.append((ms, ip))
    print "{}/{}\r".format(count, total),
    count += 1
print ""

avaliable.sort()
top5 = avaliable[:5]

print('\nTop5 Fast IPs:')
for ms, ip in top5:
    print '{ip}:\t{ms}ms'.format(ms=ms, ip=ip)