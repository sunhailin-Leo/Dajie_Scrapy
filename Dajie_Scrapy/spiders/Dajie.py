# -*- coding: utf-8 -*-
"""
Created on 2018年2月22日
@author: Leo
@file: Dajie.py
"""
# Python内置库
import json

# 第三方库
import scrapy
from scrapy.conf import settings

# 项目内部库
from Dajie_Scrapy.items import DajieScrapyItem
from Dajie_Scrapy.utils.util import *
from Dajie_Scrapy.logger.LoggerHandler import Logger

# 日志中心
logger = Logger(logger='Dajie.py').get_logger()


class DaJie(scrapy.Spider):

    name = "DaJie"

    def __init__(self, **kwargs):

        # 爬取字段 set到REFERER_NAME中
        if len(kwargs) != 0:
            self._search_name = kwargs['search_name']
            settings.set("REFERER_NAME", self._search_name)
        else:
            self._search_name = settings.get("REFERER_NAME")

        # 请求json的url
        self._cookie_url = "https://so.dajie.com/job/search?keyword={}&from=job&clicktype=blank"
        self._url = 'https://so.dajie.com/job/ajax/search/filter?keyword={' \
                    '}&order=0&city&recruitType&salary&experience&page={}&positionFunction&_CSRFToken&ajax=1'

        super().__init__(**kwargs)

    @staticmethod
    def set_cookie(response):
        """
        保存cookie
        :param response: Scrapy的返回对象
        """
        cookie = "".join([i.decode("UTF-8")
                          for i in response.headers.getlist('Set-Cookie')])
        settings.set("DAJIE_COOKIE", cookie)

    @staticmethod
    def parse_data(response):
        """
        解析数据
        :param response: Scrapy的返回对象
        :return: 解析后的数据
        """
        json_data = response.body.decode(response.encoding)
        data = json.loads(json_data, encoding="GB2312")
        return data

    def start_requests(self):
        url = self._cookie_url.format(self._search_name)
        yield scrapy.Request(url=url, method="GET", callback=self.parse_cookie)

    def parse_cookie(self, response):
        """
        解析cookie
        :param response: 返回的对象
        """
        # set cookie
        self.set_cookie(response)

        url = self._url.format(self._search_name, 1)
        yield scrapy.Request(url=url, method="GET", callback=self.parse_max_page_num)

    def parse_max_page_num(self, response):
        """
        解析总页数
        :param response: 返回对象
        """
        data = self.parse_data(response)
        # 总页数
        total_page = data['data']['totalPage']
        for page in range(1, total_page + 1):
            url = self._url.format(self._search_name, page)
            yield scrapy.Request(url=url, method="GET", callback=self.parse)

    def parse(self, response):
        """
        解析获取数据
        :param response: Response对象
        """
        data = self.parse_data(response)
        data_list = data['data']['list']
        for each_data in data_list:
            # 初始化一个Item
            item = DajieScrapyItem()
            # ID
            # logger.info("JobID: %s, CorpID: %s" % (each_data['jobseq'], each_data['corpId']))
            item['_id'] = string_to_md5(str(each_data['jobseq']) + str(each_data['corpId']))
            # 数据来源
            item['from_website'] = "大街网"
            # 职位信息页面
            job_url = "http:" + each_data['jobHref']
            # 解析
            yield scrapy.Request(url=job_url,
                                 method="GET",
                                 callback=self.parse_job_info,
                                 meta={"dajie_data": item})

    @staticmethod
    def parse_job_info(response):
        """
        解析职位信息
        :param response: Response对象
        :return: 无返回对象
        """
        # Item
        item = response.meta['dajie_data']

        # 最低和最高工资
        salary = response.xpath(
            'string(//span[@class="job-money"])').extract()[0].replace("元/月", "").split("-")
        if salary[0] != "面议":
            if len(salary) != 1:
                item['min_salary'] = salary[0]
                item['max_salary'] = salary[1]
            else:
                item['min_salary'] = salary[0]
                item['max_salary'] = ""
        else:
            item['min_salary'] = item['max_salary'] = salary[0]
        # 工作地点
        item['location'] = response.xpath(
            'string(//div[@class="job-msg-center"]/ul/li[@class="ads"]/span)').extract()[0]
        # 发布时间
        publish_data = \
            response.xpath(
                'string(//div[@class="job-msg-bottom"]/span[@class="date"])'
            ).extract()[0].replace("发布于", "")
        item['publish_date'] = int(time_to_timestamp(time_str=publish_data, time_format_model="%Y-%m-%d"))
        # 工作类型
        work_type = response.xpath(
            'string(//div[@class="job-msg-top-text"]/span[2])').extract()[0]
        item['work_type'] = re.findall(r'[^（）]+', work_type)[0]
        # 工作经验
        item['work_experience'] = response.xpath(
            'string(//div[@class="job-msg-center"]/ul/li[@class="exp"]/span)').extract()[0]
        # 学历要求
        item['limit_degree'] = response.xpath(
            'string(//div[@class="job-msg-center"]/ul/li[@class="edu"]/span)').extract()[0]
        # 人数要求
        item['people_count'] = \
            response.xpath(
                'string(//div[@class="job-msg-center"]/ul/li[@class="recruiting"]/span)'
        ).extract()[0].replace("\xa0人", "")
        # 工作名称
        item['work_name'] = response.xpath(
            'string(//div[@class="job-msg-top-text"]/span[@class="job-name"])').extract()[0]
        # 工作职责
        item['work_duty'] = ""
        # 工作需求
        item['work_need'] = ""
        # 工作内容
        content = \
            response.xpath('string(//div[@id="jp_maskit"]/pre[2])').extract()[0].strip().replace("\n", "")
        content = re.sub('\r|\n|\u3000|\xa0|\t', "", content)
        item['work_content'] = "".join(content)
        # 招聘信息链接
        item['work_info_url'] = response.url
        # 公司名称
        item['business_name'] = response.xpath(
            'string(//div[@class="i-corp-base-info"]/p[@class="title"]/a)').extract()[0]
        # 公司类型
        item['business_type'] = ""
        # 公司规模
        business_count = response.xpath(
            'string(//div[@class="i-corp-base-info"]/ul[@class="info"]/li[1]/span)').extract()[0]
        if business_count == "————":
            item['business_count'] = ""
        else:
            item['business_count'] = ""
        # 公司官网
        business_website = response.xpath(
            'string(//div[@class="i-corp-base-info"]/ul[@class="info"]/li[4]/span)').extract()[0]
        if business_website == "————":
            item['business_website'] = ""
        else:
            item['business_website'] = business_website
        # 公司行业类型
        business_industry = response.xpath(
            'string(//div[@class="i-corp-base-info"]/ul[@class="info"]/li[2]/span)').extract()[0]
        if business_industry == "————":
            item['business_industry'] = ""
        else:
            item['business_industry'] = business_industry
        # 公司地址
        item['business_location'] = ""
        # 公司介绍信息
        info = \
            response.xpath(
                'string(//div[@class="i-corp-desc"]/p)'
            ).extract()[0].strip().replace("\xa0", "").replace("\n", "").replace("\r", "")
        item['business_info'] = "".join(info)

        # 测试输出
        # print(item)
        yield item
