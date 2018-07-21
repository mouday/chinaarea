# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from models import ChinaAreaModel
from scrapy.exceptions import DropItem


class StatsSpiderPipeline(object):
    def process_item(self, item, spider):
        model = item["model"]

        ret = ChinaAreaModel.filter(ChinaAreaModel.code == model.code).first()

        logging.debug("*" * 40)
        for k, v in model.__data__.items():
            logging.debug(">>> {}: {}".format(k, v))

        if not ret:
            model.save()
            logging.debug("save successful name: %s" % model.name)
        else:
            logging.debug("save fail name: %s" % model.name)

        raise DropItem
