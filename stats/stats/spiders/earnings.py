# -*- coding: utf-8 -*-
import scrapy
import re
import time
from selenium import webdriver


class EarningsSpider(scrapy.Spider):
    name = 'earnings'
    allowed_domains = ['equibase.com/stats']
    start_urls = ['http://equibase.com/stats/']

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        # self.driver.get(response.url)
        # res = response.replace(body=self.driver.page_source)
        return self.data_parse(response)

    def data_parse(self, response):
        self.driver.get(response.url)
        res = response.replace(body=self.driver.page_source)
        current_year = int(
            ''.join(res.xpath("//select[@id='year']/option[1]/text()").extract()).strip())
        play = {}
        # get 4 years of data
        for k in range(4):
            year = current_year - k
            self.driver.find_element_by_xpath(
                "//select[@id='year']/option[@value='" + str(year) + "']").click()
            self.driver.find_element_by_xpath("//button[@id='filterButton']").click()
            time.sleep(60)
            # get the last page number to iterate to
            page_limit = int(
                ''.join(res.xpath('//a[@style="cursor:pointer;"][6]/text()').extract()).strip())
            # for j in range(page_limit):  # forward
            for j in range(page_limit, -1, -1):  # reverse
                # number = j + 2  # forward
                number = j  # reverse
                row = res.xpath(
                    '//div[@class="search-results"]/div[@id="printData"]/table[1]//tr')
                for i in row:
                    name = ''.join(i.xpath('td[@class="horse"]/a/text()').extract()).strip()
                    name = re.sub("\s\(\w+\)", '', name)
                    starts = ''.join(i.xpath('td[@class="starts"]/text()').extract()).strip()
                    win = ''.join(i.xpath('td[@class="win"]/text()').extract()).strip()
                    seconds = ''.join(i.xpath('td[@class="seconds"]/text()').extract()).strip()
                    thirds = ''.join(i.xpath('td[@class="thirds"]/text()').extract()).strip()
                    earnings = ''.join(i.xpath('td[@class="earnings"]/text()').extract()).strip()
                    earnings = re.sub(',', '', earnings)
                    earnings = re.sub('\$', '', earnings)
                    speed = ''.join(i.xpath('td[@class="speed"]/text()').extract()).strip()
                    play['starts'] = starts
                    play['name'] = name
                    play['win'] = win
                    play['seconds'] = seconds
                    play['thirds'] = thirds
                    play['earnings'] = earnings
                    play['speed'] = speed
                    play['year'] = year
                    yield play
                self.driver.find_element_by_xpath(
                    "//a[@onclick='javascript:app.events.pageNav(" + str(number) + ");']").click()
                time.sleep(10)
                res = response.replace(body=self.driver.page_source)

        self.driver.close()
