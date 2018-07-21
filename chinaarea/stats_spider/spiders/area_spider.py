# -*- coding: utf-8 -*-

# @File    : stats_spider1.py
# @Date    : 2018-07-20
# @Author  : Peng Shiyu
# @program : 中国 省 市 县 行政区域爬虫

"""
来源：国家统计局 2017年统计用区划代码和城乡划分代码(截止2017年10月31日)
地址：http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html
"""
import os
import sys

import re

from china_area.stats_spider.models import ChinaProvinceModel, ChinaCityModel, ChinaCountyModel

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from scrapy import Spider, Selector, Request
from items import StatsSpiderItem
from models import ChinaAreaModel


class AreaSpider(Spider):
    """
    解析出省份列表
    """
    name = 'area_spider'
    # download_delay = 1
    allowed_domains = ['stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html']

    def parse(self, response):
        provinces = response.css(".provincetr td")
        for province in provinces:
            href = province.css("a::attr(href)").extract_first("")
            name = province.css("a::text").extract_first("")
            url = response.urljoin(href)
            if href == "":
                continue

            code = re.findall("\d+", href)[0]

            model = ChinaProvinceModel()
            model.name = name
            model.code = code
            try:
                model.save()
                self.log("save success name: %s" % name)
            except Exception as e:
                self.log("save fail : %s" % e)

            yield Request(url, meta={"province": model}, callback=self.parse_city)

    def parse_city(self, response):
        province = response.meta.get("province")

        # 城市
        citys = response.css(".citytr")
        for city in citys:
            code = city.xpath("./td[1]").xpath("string(.)").extract_first("")
            name = city.xpath("./td[2]").xpath("string(.)").extract_first("")
            href = city.xpath("./td[2]/a/@href").extract_first("")

            url = response.urljoin(href)

            model = ChinaCityModel()
            model.name = name
            model.code = code
            model.province = province
            try:
                model.save()
                self.log("save success name: %s" % name)
            except Exception as e:
                self.log("save fail : %s" % e)

            yield Request(url, meta={"city": model}, callback=self.parse_county)

    def parse_county(self, response):
        city = response.meta.get("city")

        # 县
        counties = response.css(".countytr")
        for county in counties:
            code = county.xpath("./td[1]").xpath("string(.)").extract_first("")
            name = county.xpath("./td[2]").xpath("string(.)").extract_first("")

            model = ChinaCountyModel()
            model.name = name
            model.code = code
            model.city = city

            try:
                model.save()
                self.log("save success name: %s" % name)
            except Exception as e:
                self.log("save fail : %s" % e)


if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute("scrapy crawl area_spider".split())

