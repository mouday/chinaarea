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
    """
    获取中国行政区域划分
    """
    def get_province(self, city_name, default=None):
        """
        通过城市名获取所属省份
        :param city_name: {str} 城市名称
        :param default: 获取失败的默认值 None
        :return: {str} 省份名称 or default
        """
        city = (ChinaCityModel
                .filter(ChinaCityModel.name == city_name)
                .first())
        return city.province.name if city else default

    def get_city(self, county_name, default=None):
        """
        通过县/区名获取所属城市
        :param county_name: {str} 县/区名称
        :param default: 获取失败的默认值 None
        :return: {str} 城市名称 or default
        """
        county = (ChinaCountyModel
                  .filter(ChinaCountyModel.name == county_name)
                  .first())
        return county.city.name if county else default

    def get_provinces(self):
        """
        获取中国所有省份名称
        :return: {list} 省份列表
        """
        provinces = ChinaProvinceModel.select()
        return [province.name for province in provinces] if provinces else []

    def get_cities(self, province_name):
        """
        通过省份名称获取下面的所有城市
        :param province_name: {str} 省份名称
        :return: {list} 城市列表
        """
        province = (ChinaProvinceModel
                    .filter(ChinaProvinceModel.name == province_name)
                    .first())
        return [city.name for city in province.cities] if province else []

    def get_counties(self, city_name):
        """
        通过城市名称获取下面的所有县/区
        :param city_name: {str} 城市名称
        :return: {list} 所有县/区
        """
        city = (ChinaCityModel
                .filter(ChinaCityModel.name == city_name)
                .first())
        return [county.name for county in city.counties] if city else []

    def is_province(self, address):
        """
        判断字符串是否是一个省名
        :param address: {str} 字符串
        :return: {bool} 是省名 True, 不是省名 False
        """
        province = ChinaProvinceModel.filter(ChinaProvinceModel.name == address).first()
        return True if province else False

    def is_city(self, address):
        """
        判断字符串是否是一个城市名
        :param address: {str} 字符串
        :return: {bool} 是城市名 True, 不是城市名 False
        """
        city = ChinaCityModel.filter(ChinaCityModel.name == address).first()
        return True if city else False

    def is_county(self, address):
        """
        判断字符串是否是一个县/区名
        :param address: {str} 字符串
        :return: {bool} 是县/区名 True, 不是县/区名 False
        """
        county = ChinaCountyModel.filter(ChinaCountyModel.name == address).first()
        return True if county else False

    def _check_city(self):
        """
        检查城市名中重复名称
        :return: None
        """
        cities = ChinaCityModel.select()
        cities = [city.name for city in cities]
        print(len(cities))
        print(len(set(cities)))
        for city in set(cities):
            cities.remove(city)
        print(cities)

    def _check_county(self):
        """
        检查县/区名中重复名称
        :return: None
        """
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

    # 显示所有地市
    for province in chinaarea.get_provinces():
        print("### %s ###" % province)
        for city in chinaarea.get_cities(province):
            print("# %s" % city)
            for county in chinaarea.get_counties(city):
                print("* %s" % county)
