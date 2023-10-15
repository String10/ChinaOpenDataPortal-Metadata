import argparse
import json
import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor

from common.constants import (
    METADATA_SAVE_PATH,
    REQUEST_MAX_TIME,
)
from common.util import log_error
from crawler.crawler import Crawler

PROVINCE_CURL_JSON_PATH = os.path.join(os.path.dirname(__file__), "data/curl.json")

parser = argparse.ArgumentParser()
parser.add_argument("--all", action="store_true")
parser.add_argument("--province", type=str)
parser.add_argument("--city", type=str)

parser.add_argument("--workers", type=int, default=0)

parser.add_argument("--resource", type=str, default=PROVINCE_CURL_JSON_PATH)
parser.add_argument("--metadata-output", type=str, default=METADATA_SAVE_PATH)

parser.add_argument("--debug", action="store_true")

args = parser.parse_args()
DEBUG = args.debug

requests.packages.urllib3.disable_warnings()

with open(args.resource, "r", encoding="utf-8") as curlFile:
    curls = json.load(curlFile)


def crawl_then_save(province, city):
    crawler = Crawler(province, city, args.metadata_output, curls)
    for _ in range(REQUEST_MAX_TIME):
        try:
            crawler.crawl()
            break
        except Exception as e:
            log_error("global: error at %s - %s", province, city)
            if DEBUG:
                log_error("%s", str(e.args))
                break
            time.sleep(50)
    crawler.save_metadata_as_json(args.metadata_output)


if args.all:
    workers = args.workers
    if workers > 0:
        pool = ThreadPoolExecutor(max_workers=workers)
        for province in curls:
            for city in curls[province]:
                pool.submit(crawl_then_save, province, city)
        pool.shutdown()
    else:
        for province in curls:
            for city in curls[province]:
                crawl_then_save(province, city)
elif args.province and args.city:
    crawl_then_save(args.province, args.city)
