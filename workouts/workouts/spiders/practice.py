# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime


class PracticeSpider(scrapy.Spider):
    # The name and start_url are required by scrapy
    name = 'practice'
    start_urls = ['https://www.equibase.com/static/workout/']

    # Go to main workout page and scrub all date hyperlinks for each track
    def parse(self, response):
        for href in response.xpath('//*[@class="dkbluesm"]/@href').extract():
            yield response.follow(href, self.parse_horses)

    # Go to individual track workout page and scrub the tables for horse workouts
    def parse_horses(self, response):
        topper = response.xpath('//*[@id="c-workouts-by-track"]')
        banner = ''.join(topper.xpath('h2//text()').extract()).strip().split()
        # second up to the date is the track name in the list
        track_name = ' '.join(banner[1:-3])
        # last 3 items in the list are the date (if the script is breaking, use %b for month abbreviations)
        date = banner[-3] + ' ' + banner[-2] + ' ' + banner[-1]
        date = datetime.strptime(date, '%B %d, %Y').date()
        header = topper.xpath('form')
        # get a list of track speeds, types, lengths for all of the tables to iterate from below
        track_type = header.xpath('div/table//tr[2]/td[2]/text()').extract()
        track_speed = header.xpath('div/table//tr[3]/td[2]/text()').extract()
        length = header.xpath('div/h3//text()').extract()
        # have to get zero time to use below
        zero = '00:00.00'
        zero = datetime.strptime(zero, '%M:%S.%f')
        # counter controls the table number on the page (starting at second table)
        counter = 1
        # iterate through all of the table headers
        for (j, k, l) in zip(length, track_type, track_speed):
            far = 0
            if j == 'Two Furlongs':
                far = 2
            if j == 'Three Furlongs':
                far = 3
            if j == 'Four Furlongs':
                far = 4
            if j == 'Five Furlongs':
                far = 5
            if j == 'Six Furlongs':
                far = 6
            if j == 'Seven Furlongs':
                far = 7
            if j == 'Eight Furlongs':
                far = 8
            # grab the data for the correct table number
            furlong = header.xpath('table['+str(counter)+']//tr')
            counter = counter+1
            # if far is 0, then it is race not measured in furlongs, so ignore
            if far != 0:
                # go through each row in the table
                for i in furlong:
                    # get the horse name and remove the state ex: (KY)
                    horse = ''.join(i.xpath('td[1]//text()[last()]').extract()).strip()
                    horse = re.sub("\s\(\w+\)", '', horse)
                    # get the time the horse ran the workout in seconds
                    speed = ''.join(i.xpath('td[5]//text()').extract()).strip()
                    # longer time with minutes
                    if len(speed) > 5:
                        # convert to full time
                        speed = datetime.strptime(speed, '%M:%S.%f')
                        # have to subract 0 in order to get seconds
                        speed = (speed-zero).total_seconds()
                    # empty string is empty still
                    elif len(speed) < 1:
                        speed = ''
                    # time with seconds
                    else:
                        speed = datetime.strptime(speed, '%S.%f')
                        speed = (speed-zero).total_seconds()
                    age = ''.join(i.xpath('td[@data-label="Age"]/text()').extract()).strip()
                    sex = ''.join(i.xpath('td[@data-label="Sex"]/text()').extract()).strip()
                    race = ''.join(
                        i.xpath('td[@data-label="Race Status"]/text()').extract()).strip()
                    notes = ''.join(i.xpath('td[@data-label="Notes"]/text()').extract()).strip()
                    play = {}
                    play['name'] = horse
                    play['distance'] = far
                    play['track'] = track_name
                    play['type'] = k
                    play['speed'] = l
                    play['date'] = date
                    play['time'] = speed
                    play['age'] = age
                    play['sex'] = sex
                    play['race'] = race
                    play['notes'] = notes
                    yield play
