# -*- coding: utf-8 -*-

# @File    : chinaarea.py
# @Date    : 2018-07-21
# @Author  : Peng Shiyu

"""
#################### 说明 #########################
一个省 -> 多个市，一个市 -> 多个县
一个县 -> 一个市， 一个市 -> 一个省

备注：县级名称单位可能会重复， 返回第一个查到的市级单位
来源：国家统计局 2017年统计用区划代码和城乡划分代码(截止2017年10月31日)
地址：http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html
"""

import os
import sys
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from stats_spider.models import ChinaProvinceModel, ChinaCityModel, ChinaCountyModel

__all__ = ["ChinaArea"]


class ChinaArea(object):
    def get_province(self, city_name, default=None):
        city = (ChinaCityModel
                .filter(ChinaCityModel.name == city_name)
                .first())
        return city.province.name if city else default

    def get_city(self, county_name, default=None):
        county = (ChinaCountyModel
                  .filter(ChinaCountyModel.name == county_name)
                  .first())
        return county.city.name if county else default

    def get_cities(self, province_name):
        province = (ChinaProvinceModel
                    .filter(ChinaProvinceModel.name == province_name)
                    .first())
        return [city.name for city in province.cities] if province else []

    def get_counties(self, city_name):
        city = (ChinaCityModel
                .filter(ChinaCityModel.name == city_name)
                .first())
        return [county.name for county in city.counties] if city else []

    def is_province(self, address):
        province = ChinaProvinceModel.filter(ChinaProvinceModel.name == address).first()
        return True if province else False

    def is_city(self, address):
        city = ChinaCityModel.filter(ChinaCityModel.name == address).first()
        return True if city else False

    def is_county(self, address):
        county = ChinaCountyModel.filter(ChinaCountyModel.name == address).first()
        return True if county else False

    def _check_city(self):
        cities = ChinaCityModel.select()
        cities = [city.name for city in cities]
        print(len(cities))
        print(len(set(cities)))
        for city in set(cities):
            cities.remove(city)
        print(cities)

    def _check_county(self):
        counties = ChinaCountyModel.select()
        counties = [county.name for county in counties]
        print(len(counties))
        print(len(set(counties)))
        for county in set(counties):
            counties.remove(county)
        print(counties)


if __name__ == '__main__':
    chinaarea = ChinaArea()
    city = chinaarea.get_counties("天津市")
    print(city)

    ret = chinaarea.is_county("南开区")
    print(ret)
