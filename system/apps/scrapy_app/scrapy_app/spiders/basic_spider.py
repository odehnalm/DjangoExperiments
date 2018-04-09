import re
import importlib

from scrapy import Request as ScrapyRequest
import scrapy

from ..items import ScrapyAppItem


def cleanhtml(raw_html):

    cleanr = re.compile('<.*?>')

    if isinstance(raw_html, str):
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    if isinstance(raw_html, list):
        cleantext = [re.sub(cleanr, '', componente) for componente in raw_html]
        return cleantext


class BasicSpider(scrapy.Spider):
    name = "icrawler"
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(BasicSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get("url")]
        self.allowed_domains = [kwargs.get("allowed_domain")]
        self.max_items = kwargs.get("max_items", 5)
        self.rotate_user_agent = kwargs.get("rotate_user_agent", True)
        self.name_scraper = kwargs.get("name_scraper")
        module = importlib.import_module(self.name_scraper)
        self.get_data = getattr(module, "get_data")
        self.get_item_data = getattr(module, "get_item_data")
        try:
            self.init_requests = getattr(module, "init_requests")
        except AttributeError:
            self.init_requests = None
        self.item_category = kwargs.get("item_category")
        self.job_id = kwargs.get("job_id")
        self.store_id = kwargs.get("store_id")

    def start_requests(self):

        if self.init_requests is not None:
            return self.init_requests(
                url=self.start_urls[0],
                callback=self.parse
            )
        else:
            return super(BasicSpider, self).start_requests()

    def parse(self, response):
        item = ScrapyAppItem()
        item["job_id"] = self.job_id
        item["store_id"] = self.store_id
        item["category_id"] = self.item_category
        data = self.get_data(
            response,
            url=self.start_urls[0],
            item_category=self.item_category
        )
        n = len(data['nom_prod'])

        for i in range(n):

            if i >= self.max_items:
                return

            yield ScrapyRequest(
                data['url_base'] + data['url_prod'][i],
                callback=self.callback_parse,
                meta={'item': item, 'nom_prod': data['nom_prod'],
                      'detail_prod': data['detail_prod'], 'counter': i,
                      'url_tienda': data['url_prod'][i]
                      },
                dont_filter=True)

    def callback_parse(self, response):

        print("CALLBACK PARSE")

        yield self.get_item_data(response)
