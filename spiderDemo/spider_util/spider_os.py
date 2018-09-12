import time
import os

while True:
    find_crawl_all = False
    ss = os.popen("ps -aux | grep crawlall")
    for s in ss:
        print(s)
        if "scrapy crawlall" in s:
            find_crawl_all = True

    if find_crawl_all:
        print("YES")
    else:
        print("NULL")
        os.system("scrapy crawlall")
    time.sleep(10)
