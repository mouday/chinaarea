说明
====

一个省 -> 多个市，一个市 -> 多个县

一个县 -> 一个市， 一个市 -> 一个省

备注：县级名称单位可能会重复， 返回第一个查到的市级单位

来源：国家统计局 2017年统计用区划代码和城乡划分代码(截止2017年10月31日)

地址：http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html

范围：省 - 市 - 县/区

快速开始
========

::

    pip install chinaarea

pypi地址
========

https://pypi.org/project/chinaarea/

项目结构
========

::

    chinaarea/
        │  chinaarea.py              # 项目主文件
        │  README.md                 # 说明文件
        │  scrapy.cfg                # scrapy配置文件
        │  __init__.py
        │
        └─stats_spider/             # 抓取数据的scrapy爬虫文件
            │  china_area.sqlite    # 数据保存的sqlite数据库文件
            │  items.py
            │  middlewares.py
            │  models.py
            │  pipelines.py
            │  settings.py
            │  __init__.py
            │
            ├─spiders/             # 抓取数据的爬虫
                   area_spider.py
                   __init__.py

代码示例
========

.. code:: python

    >>> from chinaarea import ChinaArea

    # 实例化
    >>> ca = ChinaArea()


    # 通过省获取市
    >>> ca.get_cities("山东省")
    ['济南市', '青岛市', '淄博市', '枣庄市', '东营市', '烟台市', '潍坊市',
     '泰安市', '威海市', '日照市', '莱芜市', '临沂市', '德州市', '聊城市',
     '菏泽市']

     # 通过市获取县/区
    >>> ca.get_counties("济南市")
    ['市辖区', '历下区', '市中区', '槐荫区', '天桥区', '历城区', '长清区',
     '平阴县', '济阳县', '商河县', '济南高新技术产业开发区']


    # 通过县获取市
    >>> ca.get_city("海淀区")
    '北京市'

    # 通过市获取省
    >>> ca.get_province("合肥市")
    '安徽省'


    # 判断是否是省名
    >>> ca.is_province("陕西省")
    >>> True

    # 判断是是否是市名
    >>> ca.is_city("陕西省")
    >>> False

    # 判断是是否是县/区名
    >>> ca.is_county("南开区")
    >>> True

    # 显示所有省份，城市，县/区
    for province in ca.get_provinces():
        print("### %s ###" % province)
        for city in ca.get_cities(province):
            print("# %s" % city)
            for county in ca.get_counties(city):
                print("* %s" % county)
