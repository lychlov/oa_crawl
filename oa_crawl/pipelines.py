# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import scrapy
from settings import IMAGES_STORE as images_store
# 将信息存储为JSON
import os

from scrapy.pipelines.images import ImagesPipeline


class OaCrawlJSONPipeline(object):
    def process_item(self, item, spider):
        # 将ITEM中信息输出JSON
        with open("txl.json", "a+") as f:
            content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            f.write(content.encode("utf-8"))
        return item


class OaCrawlImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_url = item["image_url"]
        if "None" not in image_url:
            # 将图片地址提交下载器下载
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        # 下载完成后实现对图片重命名
        image_path = [x['path'] for ok, x in results if ok]
        if len(image_path) > 0:
            os.rename(images_store + "\\" + image_path[0],
                      images_store + "\\" + item["name"] + "-" + item["department"].replace("/", "-") + ".jpg")
        return item
