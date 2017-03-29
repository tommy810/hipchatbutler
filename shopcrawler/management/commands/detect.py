import json
import logging
import pymongo
from django.core.management.base import BaseCommand, CommandError

from shopcrawler.crawlhelper import shop_search

client = pymongo.MongoClient('localhost', 27017)
db = client.shopcrawlerdb
entry = db.target
searchresult = db.searchresult

class Command(BaseCommand):
  def handle(self, *args, **options):
    for shop in entry.find():
        keywords=[]
        if shop["area"] is not None:
            keywords.append(shop["area"])

        results = shop_search(shop["shop_name"], keywords=keywords)
        for result in results:
            r = remove_dots(result)
            logging.info("\t検出: %s (%s)" % (r["title"], r["link"]))
            exist = searchresult.find({"link": r["link"]})
            searchresult.update({"link": r["link"]}, r, upsert=True)


def remove_dots(data):
    for key in data.keys():
        if type(data[key]) is dict: data[key] = remove_dots(data[key])
        if type(data[key]) is list:
            for i, v in enumerate(data[key]):
                if type(v) is dict:
                    v = remove_dots(v)
                    data[key][i] = v

        if '.' in key:
            data[key.replace('.', '_')] = data[key]
            del data[key]
        if '$' in key:
            data[key.replace('$', '@dollar@')] = data[key]
            del data[key]
    return data