import json
import logging
import pymongo
from django.core.management.base import BaseCommand, CommandError

client = pymongo.MongoClient('localhost', 27017)
db = client.shopcrawlerdb
co = db.target
co.target.delete_many({})

class Command(BaseCommand):
  args = '<shop_name> <area> <shop_tel> '

  def add_arguments(self, parser):
    parser.add_argument('shop_name', type=str)
    parser.add_argument('-area', type=str)
    parser.add_argument('-shop_tel', type=str)


  def handle(self, *args, **options):
    name = options["shop_name"]
    tel = options["shop_tel"]
    area = options["area"]

    if co.find({"shop_name": name, "shop_tel": tel, "area": area}).count() > 0:
      logging.info("'%s' already exist" % name)
    else:
      co.insert({"shop_name": name, "shop_tel": tel, "area": area})
      logging.info("entried")