# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import smtplib
import csv


server = smtplib.SMTP_SSL("smtp.gmail.com", port=465)
server.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))

def sendmail(item):
    msg = """From: i@danmilon.me
To: i@danmilon.me
Subject: check out car ad {id}

{url}
""".format(id=item['id'], url=item['url'])
    server.sendmail('i@danmilon.me', ['i@danmilon.me'], msg)


class PersistencePipeline(object):
    def __init__(self):
        self.ads_idx = {}
        self.ads = []
        with open('./cars.csv', 'w+') as f:
            reader = csv.DictReader(f)
            for ad in reader:
                self.ads.append(ad)
                self.ads_idx[ad['id']] = ad

    def close_spider(self, spider):
        with open('./cars.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.ads[0].keys())
            writer.writeheader()
            for ad in self.ads:
                # todo sort by viewed status
                writer.writerow(ad)

    def process_item(self, item, spider):
        ad = self.ads_idx.get(item['id'], None)
        if ad:
            self.ads_idx[ad['id']].update(ad)
        else:
            self.ads_idx[ad['id']]
            self.ads.append(ad)

        if not os.getenv('NOMAIL'):
            sendmail(item)
