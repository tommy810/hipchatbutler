import logging
import re
from email.mime import text
from urllib.parse import urlparse
from urllib.parse import urljoin
import requests
import bs4
from bs4 import BeautifulSoup

from shopcrawler import GoogleApiError

BASE_URL = "https://www.googleapis.com/customsearch/v1"
CLIENT_KEY = "AIzaSyD5PAc637mA23-5OJqu9pRBxxGlB7y13kU"
CX = "018209491584321571118:n50ec5di2ow"


def shop_search(shop_name, keywords=[]):
    print("------------------------------------------------------------------------------------------")
    print("店舗HPを検索: 店舗名=%s, 検索キーワード=%s" % (shop_name, " ".join(keywords)))

    params = {
        "key": CLIENT_KEY,
        "cx": CX,
        "q" : "%s %s" % (shop_name, " ".join(keywords)),
        "hl": "ja",
        "count": 100
    }
    r = requests.get(BASE_URL,params)

    if r.status_code != 200:
        logging.error("\tGoogle Custom Search API でエラーが発生しました。 %d %s" % (r.status_code, r.reason))
        raise GoogleApiError

        # for item in r.json()["items"]:
        #     shops.append({
        #         "title": item["title"],
        #         "link": item["link"]
        #     })
        #     print("\t DETECTED SHOP URL: TITLE = %s, LINK = %s" % (item["title"], item["link"]))

        # print("************************************************")
        # # print(item.keys())
        # print(item["title"])
        # print(item["snippet"])
        # print(item["displayLink"])
        # print(item["link"])
        # print("- pagemap")
        # if "metatags" in item["pagemap"]:
        #     print(item["pagemap"]["metatags"])
        # if "breadcrumb" in item["pagemap"]:
        #     print(item["pagemap"]["breadcrumb"])


    return r.json()["items"]
#
# def shop_url(shop_name, tel=None, address=None):
#     print("DETECTING SHOP URL: SHOP_NAME=%s, SHOP_TEL=%s, SHOP_ADDRESS=%s" % (shop_name, tel, address))
#     # shops = []
#     r = search(shop_name)
#     logging.info(r.status_code)
#     if r.status_code != 200:
#         logging.error("Google Custom Search API でエラーが発生しました。 %d %s" % (r.status_code, r.reason))
#         raise GoogleApiError
#
#         # for item in r.json()["items"]:
#         #     shops.append({
#         #         "title": item["title"],
#         #         "link": item["link"]
#         #     })
#         #     print("\t DETECTED SHOP URL: TITLE = %s, LINK = %s" % (item["title"], item["link"]))
#
#             # print("************************************************")
#             # # print(item.keys())
#             # print(item["title"])
#             # print(item["snippet"])
#             # print(item["displayLink"])
#             # print(item["link"])
#             # print("- pagemap")
#             # if "metatags" in item["pagemap"]:
#             #     print(item["pagemap"]["metatags"])
#             # if "breadcrumb" in item["pagemap"]:
#             #     print(item["pagemap"]["breadcrumb"])
#
#     return r.json()["items"]

# def get_assoiated_links(url):
#     print("RETRIEVING ASSOCIATED URL: BASE_URL=%s" % url)
#     associated_links = []
#     base_url = urlparse(url)
#
#     r = requests.get(url)
#     d = bs4.BeautifulSoup(r.content, "html.parser")
#
#     links = d.find_all('a')
#     for link in links:
#         if "href" in link:
#             urls = urlparse(link["href"])
#             if urls.netloc == "":
#                 associated_links.append(base_url.scheme + "://" + base_url.netloc + "/" + urls.path)
#             if urls.netloc == base_url.netloc:
#                 associated_links.append(base_url.scheme + "://" + urls.netloc + "/" + urls.path)
#
#     associated_links = list(set(associated_links))
#     for link in associated_links:
#         print("\tASSOCIATED URL: LINK=%s" % link)
#
#     return associated_links
#
# if __name__ == '__main__':
#
#     for shop in shop_url("ルチル六本木"):
#         for link in get_assoiated_links(shop["link"]):
#             print("GET PAGE [ %s ]" % link)
#             r = requests.get(link)
#             bs = BeautifulSoup(r.content, "html.parser")
#             for keyword in DETECTION_KEYWORDS:
#                 found = bs(text=re.compile(keyword))
#                 if found:
#                     print("\tKEYWORD MATCHES: KEY = %s, LINE = %s" % (keyword, found ))
