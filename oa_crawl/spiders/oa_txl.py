# -*- coding: utf-8 -*-
import json

import scrapy
from selenium import webdriver
from oa_crawl.items import OaCrawlItem


class OaTxlSpider(scrapy.Spider):
    target_domain = "http://your.domain/"
    target_domain_with_port = "http://your.domain:9080/"
    my_user_name = "chengzhikun"
    my_keys = "Czk10103"

    # 使用Selenium实现登录并获取Cookies
    # 开启Chrome模拟器
    driver = webdriver.Chrome()
    # 打开登录页面
    driver.get(target_domain + "eai/auth/eailogin.jsp")
    # 自动填写账号口令并登录
    driver.find_element_by_id("userName").send_keys(my_user_name)
    driver.find_element_by_id("userPass").send_keys(my_keys)
    driver.find_element_by_id("loginid").click()
    # 暂停3秒
    driver.implicitly_wait(3)
    # 打开即将爬取的页面
    driver.get(target_domain + "was2/HaPortalSso/inner_sso/addressbook.jsp")
    driver.get(target_domain_with_port + "AddressBook/user/getUserDynamicData.do?pageSize=100&pageNumber=1")
    # 获取cookies
    oa_cookies = driver.get_cookies()

    # 爬虫名，必选属性
    name = 'oa_txl'
    # 许可域名，必选属性
    allowed_domains = ['ha.cmcc']
    # 起始访问地址
    start_urls = [target_domain + 'eai/auth/eailogin.jsp', ]
    # 记录页号
    page_number = 1
    # 请求地址
    request_url = target_domain_with_port + "AddressBook/user/getUserDynamicData.do?pageSize=100&pageNumber="

    def start_requests(self):
        yield scrapy.Request(url=self.request_url + str(self.page_number),
                             cookies=self.oa_cookies, callback=self.parse)

    def parse(self, response):
        # 过滤其他请求
        if "getUserDynamicData.do" not in response.url:
            return
        data_list = json.loads(response.body)
        if len(data_list) == 0:
            return
        # 提取ITEM数据
        for data in data_list:
            item = OaCrawlItem()
            item["name"] = data["NAME"]
            item["user_id"] = data["USERID"]
            item["gender"] = data["GENDER"]
            item["title"] = data["POSTNAME"]
            item["department"] = data["DEPTFULLNAME"]
            item["mobile_phone"] = data["HANDSET"]
            item["email_add"] = data["EMAIL"]
            item["image_url"] = self.target_domain_with_port + "AddressBook/uploadedImg/" + str(data["PHOTO"])
            yield item
        # 发起下一页请求，迭代
        self.page_number += 1
        yield scrapy.Request(url=self.request_url + str(self.page_number),
                             cookies=self.oa_cookies, callback=self.parse)
