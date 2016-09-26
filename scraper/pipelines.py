# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import csv
import copy

CUR_DIR = os.path.dirname(os.path.realpath(__file__))


class PersistencePipeline(object):
    CSV_PATH = os.path.join(CUR_DIR, '..', 'cars.csv')
    def __init__(self):
        self.ads_idx = {}
        self.ads = []
        with open(self.CSV_PATH, 'r') as f:
            reader = csv.DictReader(f)
            for ad in reader:
                self.ads.append(ad)
                self.ads_idx[ad['id']] = ad

    def close_spider(self, spider):
        with open(self.CSV_PATH, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'id',
                'url',
                'seen'
            ])

            writer.writeheader()
            self.ads = sorted(self.ads, key=lambda ad: ad['seen'])
            for ad in self.ads:
                # todo sort by viewed status
                writer.writerow(ad)

    def process_item(self, item, spider):
        ad = self.ads_idx.get(item['id'], None)
        if ad:
            existing_ad = copy.copy(self.ads_idx[ad['id']])
            self.ads_idx[ad['id']].update(ad)
        else:
            existing_ad = None
            item['seen'] = 'no'
            self.ads_idx[item['id']] = item
            self.ads.append(item)
            ad = item

        if existing_ad and existing_ad != ad:
            ad['seen'] = 'no'
