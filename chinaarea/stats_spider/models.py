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


if __name__ == '__main__':
    province = ChinaProvinceModel.filter(ChinaProvinceModel.name == "山西省").first()
    for city in province.cities:
        print(city.name)

