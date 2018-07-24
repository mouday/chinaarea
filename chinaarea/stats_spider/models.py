# -*- coding: utf-8 -*-

# @File    : models.py
# @Date    : 2018-07-20
# @Author  : Peng Shiyu
# @program : 

# 保存到sqlite数据库

import os
from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField

DB_NAME = "china_area.sqlite"
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, DB_NAME)


DB = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = DB


class ChinaProvinceModel(BaseModel):
    name = CharField(default="")
    code = CharField(default="", unique=True)

    class Meta:
        db_table = 'china_province'


class ChinaCityModel(BaseModel):
    name = CharField(default="")
    code = CharField(default="", unique=True)
    province = ForeignKeyField(ChinaProvinceModel, field=ChinaProvinceModel.code, related_name='cities')

    class Meta:
        db_table = 'china_city'


class ChinaCountyModel(BaseModel):
    name = CharField(default="")
    code = CharField(default="", unique=True)
    city = ForeignKeyField(ChinaCityModel, field=ChinaCityModel.code, related_name='counties')

    class Meta:
        db_table = 'china_county'


# ======================
#  对数据库记录进行优化操作
# ======================

tables = [ChinaProvinceModel, ChinaCityModel, ChinaCountyModel]

for table in tables:
    if not table.table_exists():
        table.create_table()


def change_city():
    """
    将市级单位 直辖区 改为对应的 城市名称
    :return: None
    """
    cities = ChinaCityModel.filter(ChinaCityModel.name == "市辖区")
    for city in cities:
        print(city.province.name)


def change_city2():
    cities = ChinaCityModel.filter((ChinaCityModel.name == "省直辖县级行政区划") |
                                   (ChinaCityModel.name == "自治区直辖县级行政区划"))
    for city in cities:
        name = "{}{}".format(city.province.name, "直辖县")
        print(name)
        ChinaCityModel.update(name=name).where(ChinaCityModel.id == city.id).execute()


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
    # province = ChinaProvinceModel.filter(ChinaProvinceModel.name == "山西省").first()
    # for city in province.cities:
    #     print(city.name)
    change_city2()


