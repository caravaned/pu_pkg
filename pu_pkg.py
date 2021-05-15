import time

import requests
from lxml import etree
cookie = "PHPSESSID=3dcafe60609f1e0f9b6f1; Hm_lvt_dd3ea352543392a029ccf9da1be54a50=1619411738,1621005230,1621040655; TS_LOGGED_USER=mNlQnzJAsO7hvNWQNO4K5RARa; Hm_lpvt_dd3ea352543392a029ccf9da1be54a50=1621043995"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "cookie": cookie,
    'Content-Type': 'application/json'
}

def main():
    after = []
    is_new = False
    try:
        with open("a.txt", "r", newline='') as f2:
            l = f2.readlines()
            for i in l:
                new = i.strip()
                after.append(new)
    except Exception:
        print("捕获到文件异常 执行覆盖写入操作")
        is_new = True
    titles = download1("https://ayit.pocketuni.net/index.php?app=event&mod=School&act=board")
    # titles = download1("http://127.0.0.1")
    for title in titles:
        if title.text in after:
            pass
        else:
            new_url = title.xpath("./@href")[0]
            rpt_title = title.text
            download2(new_url,rpt_title)
            is_new = True

    if is_new:
        with open("a.txt", "w") as f3:
            print("数据已更新")
            for title in titles:
                f3.write(title.text)
                f3.write("\n")
                print(title.text)

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
    for i in range(len(keys)):
        value = values[i].strip()
        value = " ".join(value.split())
        data[keys[i].text.strip()] = value
    report(rpt_title,data)
    print(data)

def report(rpt_title,data):
    College = data["活动院系："]
    # 计算机科学与信息工程学院
    if "全部" == College or "计算机科学与信息工程学院" == College:
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
        prt_url = "https://oapi.dingtalk.com/robot/send?access_token=8cbb333c41299e6abe3b9957e00600e7b9b2eaaeb8165ad0e19bc9b59179bbe6"
        requests.post(url=prt_url, headers=header, json=json1)
        requests.post(url=prt_url, headers=header, json=json2)

    else:
        json = {
            "text": {
                "content": "收到一条"+College+"新活动"
            },
            "msgtype": "text"
        }
        prt_url = "https://oapi.dingtalk.com/robot/send?access_token=8cbb333c41299e6abe3b9957e00600e7b9b2eaaeb8165ad0e19bc9b59179bbe6"
        requests.post(url=prt_url, headers=header, json=json)

while True:
    time.sleep(5)
    main()