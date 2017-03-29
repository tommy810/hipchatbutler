import json
import logging

import array
import pymongo
from django.core.management.base import BaseCommand, CommandError

from shopcrawler.crawlhelper import shop_search

client = pymongo.MongoClient('localhost', 27017)
db = client.shopcrawlerdb
entry = db.target
searchresult = db.searchresult

class Command(BaseCommand):
  def handle(self, *args, **options):
    # for result in searchresult.find()[0]:

        # logging.info(searchresult.find()[0])
    # item = searchresult.find()[0]

    # for item in searchresult.find(): # {}, { 'title': 1,
                                    #    'displayLink': 1,
                                    #    'snippet': 1,
                                    #    'pagemap.metatags.og:title': 1,
                                    #    'pagemap.metatags.og:description': 1,
                                    #    'pagemap.metatags.twitter:url': 1}):
        # print("****************************************************************")
        # print_keys(item, with_value=True)
    for shop in entry.find():
        logging.info("---------------------------------------------")
        logging.info("%s - %s" % (shop["shop_name"], shop["area"]))
        links = searchresult.find({"title": {"$regex": ".*%s.*" % shop["shop_name"]}})
        if links.count() == 0:
            logging.info("\t見つかりませんでした")
        else:
            for link in links:
                logging.info("\t%s %s" % (link["title"], link["link"]))


def print_keys(item, level=0, with_value=False):
    leveled_space = " " * level * 3
    for key in item.keys():
        if with_value:
            if isinstance(item[key], dict) or isinstance(item[key], list):
                logging.info("%(space)s %(key)s" % {"space": leveled_space, "key": key})
            else:
                logging.info("%(space)s %(key)s             => %(value)s" % {"space": leveled_space, "key": key, "value" : item[key]})
        else:
            logging.info("%(space)s %(key)s" % {"space": leveled_space, "key": key})

        if isinstance(item[key], dict):
            print_keys(item[key], level + 1, with_value)
        elif isinstance(item[key], list):
            for item2 in item[key]:
                print_keys(item2, level + 1, with_value)