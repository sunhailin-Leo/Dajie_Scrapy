# -*- coding: utf-8 -*-

# 第三方库
import pymongo
from scrapy.conf import settings

# 项目内置库
from Dajie_Scrapy.logger.LoggerHandler import Logger

# 日志中心
logger = Logger(logger='pipelines.py').get_logger()


class DajieScrapyPipeline(object):
    def __init__(self):
        """
        MongoDB的配置
        """
        self._host = settings.get("MONGODB_HOST")
        self._port = settings.get("MONGODB_PORT")
        self._user = settings.get("MONGODB_USER")
        self._pass = settings.get("MONGODB_PASS")
        self._db_name = settings.get("MONGODB_DB_NAME")
        self._col_name = settings.get("MONGODB_COL_NAME")

        # 初始化
        self.client = None
        self.db = None
        self.collection = None

    def open_spider(self, spider):
        """
        启动爬虫之后的方法
        :param spider: 爬虫对象
        :return: 无返回值
        """
        if spider.name == "DaJie":
            self.client = pymongo.MongoClient(host=self._host, port=self._port)
            self.db = self.client[self._db_name]
            self.collection = self.db[self._col_name]

    def close_spider(self, spider):
        """
        关闭爬虫之后的方法
        :param spider: 爬虫对象
        :return: 无返回值
        """
        if spider.name == "DaJie":
            self.client.close()

    def process_item(self, item, spider):
        """
        写入数据库中
        :param item: 数据条目
        :param spider: 爬虫对象
        :return: 返回显示item
        """
        if spider.name == "DaJie":
            try:
                self.collection.insert(item)
                return item
            except Exception as err:
                logger.error(err)
