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
import logging
import os
import sys

import jieba

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from stats_spider.models import ChinaProvinceModel, ChinaCityModel, ChinaCountyModel

__all__ = ["ChinaArea"]


class ChinaArea(object):
    """
    获取中国行政区域划分
    """
    def get_provinces(self, province_name=None):
        """
        获取中国所有省份名称
        :return: {list} 省份名称
        """
        if province_name is None:
            provinces = ChinaProvinceModel.select()
        else:
            provinces = ChinaProvinceModel.filter(ChinaProvinceModel.name.contains(province_name))
        return [province.name for province in provinces]

    def get_provinces_by_city(self, city_name):
        """
        通过城市名获取所属省份
        :param city_name: {str} 城市名称
        :return: {list} 省份名称
        """
        cities = ChinaCityModel.filter(ChinaCityModel.name.contains(city_name))
        return [city.province.name for city in cities]

    def get_cities(self, city_name=None):
        """
        获取所有城市名称
        :return: {list} 城市名称
        """
        if city_name is None:
            cities = ChinaCityModel.select()
        else:
            cities = ChinaCityModel.filter(ChinaCityModel.name.contains(city_name))
        return [city.name for city in cities]

    def get_cities_by_province(self, province_name):
        """
        通过省份名称获取下面的所有城市
        :param province_name: {str} 省份名称
        :return: {list} 城市名称
        """
        provinces = ChinaProvinceModel.filter(ChinaProvinceModel.name.contains(province_name))

        city_list = []

        for province in provinces:
            for city in province.cities:
                city_list.append(city.name)

        return city_list

    def get_cities_by_county(self, county_name):
        """
        通过县/区名获取所属城市
        :param county_name: {str} 县/区名称
        :return: {list} 城市名称
        """
        counties = ChinaCountyModel.filter(ChinaCountyModel.name.contains(county_name))
        return [county.city.name for county in counties]

    def get_counties(self, county_name=None):
        """
        获取的所有县/区
        :return: {list} 县/区名称
        """
        if county_name is None:
            counties = ChinaCountyModel.select()
        else:
            counties = ChinaCountyModel.filter(ChinaCountyModel.name.contains(county_name))
        return [county.name for county in counties]

    def get_counties_by_city(self, city_name):
        """
        通过城市名称获取下面的所有县/区
        :param city_name: {str} 城市名称
        :return: {list} 县/区名称
        """
        cities = ChinaCityModel.filter(ChinaCityModel.name.contains(city_name))

        county_list = []
        for city in cities:
            for county in city.counties:
                county_list.append(county.name)

        return county_list

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

    def find_areas(self, address):
        """
        查找语句中的省份，地市，县/区名称
        :param address: {str} 字符串
        :return: {dict}
            {
                "provinces": set(),  省
                "cities": set(),     市
                "counties": set()    县/区
            }
        """
        jieba.setLogLevel(logging.INFO)
        words = jieba.lcut(address)
        areas = {
            "provinces": set(),
            "cities": set(),
            "counties": set()
        }
        for word in words:
            if len(word) < 2:
                continue
            provinces = self.get_provinces(word)
            if provinces:
                areas["provinces"].update(provinces)
            cities = self.get_cities(word)
            if cities:
                areas["cities"].update(cities)
            counties = self.get_counties(word)
            if counties:
                areas["counties"].update(counties)

        return areas


if __name__ == '__main__':
    ca = ChinaArea()
    company = "武汉市蔡甸区战略性新兴产业发展引导基金"
    ret = ca.find_areas(company)
    for k, v in ret.items():
        print("{}: {}".format(k, v))
