import json
import logging
import pymongo
from django.core.management.base import BaseCommand, CommandError

client = pymongo.MongoClient('localhost', 27017)
db = client.shopcrawlerdb
co = db.searchresult

class Command(BaseCommand):
  args = '<shop_name>'

  def add_arguments(self, parser):
    parser.add_argument('shop_name', type=str)

  def handle(self, *args, **options):
    shop_name = options["shop_name"]
    for result in co.find({"title": { "$regex" : ".*%s.*" % shop_name}}):
        print(result["title"], result["link"])