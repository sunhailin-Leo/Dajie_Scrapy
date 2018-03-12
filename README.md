# 大街网爬虫(Scrapy版)

---

* 使用中有问题的可以提个issue让我改进改进

---

<h3 id="Info">介绍</h3>

* 简单叙述：
    * 单纯用来爬取大街网的招聘职位信息(目前只有通过关键词搜索去爬取)
    * 这个爬虫的目的是用获取关键词有关的招聘信息, 用于做数据挖掘和数据分析的工作 

---

<h3 id="Env">环境和安装方式</h3>

* 开发环境: Win10 x64
* Python版本: Python3.4.4
* Python依赖:
    * Scrapy
    * requests
    * pymongo
    * twisted
    * PyDispatcher

* 安装方式:

```Bash
pip install -r requirements.txt
```

---

<h3 id="GuideForUse">使用帮助及启动方法</h3>

* 启动的时候会有个Warning(可以忽略): ScrapyDeprecationWarning: Module `scrapy.conf` is deprecated, use `crawler.settings` attribute instead


```bash
# 根目录下:
python start_spider.py -name 大数据
```

---


<h3 id="Future">未来进度</h3>

* (优先) 定时任务
* 进度监控
* 接入到Gerapy
