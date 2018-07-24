# 说明

一个省 -> 多个市，一个市 -> 多个县

一个县 -> 多个市， 一个市 -> 多个省

备注：县级名称单位可能会重复， 返回所有查到的市级单位

来源：国家统计局 2017年统计用区划代码和城乡划分代码(截止2017年10月31日)

地址：http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html

范围：省 - 市 - 县/区

# 快速开始

    pip install chinaarea

# pypi地址
https://pypi.org/project/chinaarea/

# 项目结构
```
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
```

# 代码示例
```python
>>> from chinaarea import ChinaArea

>>> ca = ChinaArea()

# 获取所有省份
>>> ca.get_provinces()
['北京市', '天津市', '河北省', '山西省', '内蒙古自治区', '辽宁省', '吉林省', '黑龙江省', '上海市', '江苏省',, '河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省', '云南省'夏回族自治区', '新疆维吾尔自治区', '台湾省', '香港特别行政区', '澳门特别行政区']

# 查找省份名中含有 “山”
>>> ca.get_provinces("山")
['山西省', '山东省']

# 查找城市中含有 “大理”
>>> ca.get_cities("大理")
['大理白族自治州']

# 查找县/区中含有 "洛阳"
>>> ca.get_counties("洛阳")
['洛阳高新技术产业开发区']

# 通过省份中含有 “河南” 的城市
>>> ca.get_cities_by_province("河南")
['郑州市', '开封市', '洛阳市', '平顶山市', '安阳市', '鹤壁市', '新乡市', '焦作市', '濮阳市', '许昌市', '漯河'周口市', '驻马店市', '河南省直辖县']

# 判断是否是一个省份名称，必须是中国行政区域划分中的名称，每个字都要一样
>>> ca.is_province("北京")
False
>>> ca.is_province("北京市")
True

# 查找字符串中含有省，市，县/区
>>> ca.find_areas("深圳市腾讯计算机系统有限公司")
{'provinces': set(), 'cities': {'深圳市'}, 'counties': set()}


# 显示所有省份，城市，县/区
for province in ca.get_provinces():
    print("### %s ###" % province)
    for city in ca.get_cities(province):
        print("# %s" % city)
        for county in ca.get_counties(city):
            print("* %s" % county)
```
# 说明

- `get_*`，`find_*` 都是模糊查找
- `is_*` 都是绝对判断
