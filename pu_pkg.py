import time

import requests
from lxml import etree
cookie = "这里放你的cookie"
prt_url = "这里放你的钉钉机器人API"
# 参考文档：https://developers.dingtalk.com/document/app/custom-robot-access
my_collage = "这里放你的学院名称"
# eg: 计算机科学与信息工程学院


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "cookie": cookie,
    'Content-Type': 'application/json'
}

def main():
    after = []
    try:
        with open("a.txt", "r", newline='') as f2:
            l = f2.readlines()
            for i in l:
                new = i.strip()
                after.append(new)
    except Exception:
        print("捕获到文件异常")


    titles = download1("https://ayit.pocketuni.net/index.php?app=event&mod=School&act=board")
    for title in titles:
        if title.text in after:
            pass
        else:
            new_url = title.xpath("./@href")[0]
            rpt_title = title.text
            download2(new_url, rpt_title)
            is_new(rpt_title)

def is_new(new_title):
    with open("a.txt", "a") as f3:
        print("数据已更新")
        f3.write(new_title)
        f3.write("\n")


def download1(url):
    res = requests.get(url=url, headers=header)
    res.encoding="utf-8"
    root = etree.HTML(res.text)
    titles = root.xpath("//div[@class='hd_c_left_title b']/a")
    return titles

def download2(url,rpt_title):
    res = requests.get(url=url, headers=header)
    res.encoding = "utf-8"
    root = etree.HTML(res.text)
    # print(res.text)
    keys = root.xpath("//span[contains(@class,'b1')]")
    values = root.xpath("//span[contains(@class,'b1')]/following::text()[1]")
    data = {}
    data["活动院系："] = "无院系要求"
    for i in range(len(keys)):
        value = values[i].strip()
        value = " ".join(value.split())
        data[keys[i].text.strip()] = value
    report(rpt_title,data)
    # print(data)

def report(rpt_title,data):
    College = data["活动院系："]
    # 计算机科学与信息工程学院
    if "全部" == College or my_collage == College or "无院系要求" == College:
        json1 = {
        "at": {
            "isAtAll": "True"
        },
        "text": {
            "content":"新活动----"+rpt_title
        },
        "msgtype":"text"
        }
        msg = ""
        for key, value in data.items():
            msg = msg +"#### "+key+" "+value+"\n"
        json2 = {
            "msgtype": "markdown",
            "markdown": {
                "title":"活动更新",
                "text": "## "+College+"可参加的活动来了！\n "+msg,
            },

        }
        # print(json1)
        # print(json2)
        requests.post(url=prt_url, headers=header, json=json1)
        requests.post(url=prt_url, headers=header, json=json2)

    else:
        json = {
            "text": {
                "content": "收到一条 "+College+" 新活动"
            },
            "msgtype": "text"
        }
        # print(json)
        requests.post(url=prt_url, headers=header, json=json)
while True:
    localtime = time.asctime(time.localtime(time.time()))
    time.sleep(100)
    # print("check "+localtime)
    main()
