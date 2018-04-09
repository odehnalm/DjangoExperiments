# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import logging
from random import choice

from django.apps import apps
from django.conf import settings

from fake_useragent import UserAgent
from scrapy import signals
from scrapy.exceptions import NotConfigured

log = logging.getLogger('scrapy_app.proxies')


class ScrapyAppSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyAppDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    # @classmethod
    # def from_crawler(cls, crawler):
    #     # This method is used by Scrapy to create your spiders.
    #     s = cls()
    #     crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
    #     return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        print("REQUEST HEADERS")
        print(request.headers)
        # return None

    # def process_response(self, request, response, spider):
    #     # Called with the response returned from the downloader.

    #     # Must either;
    #     # - return a Response object
    #     # - return a Request object
    #     # - or raise IgnoreRequest
    #     print("RESPONSE HEADERS")
    #     print(response.request.headers)
    #     return response

    # def process_exception(self, request, exception, spider):
    #     # Called when a download handler or a process_request()
    #     # (from other downloader middleware) raises an exception.

    #     # Must either:
    #     # - return None: continue processing this exception
    #     # - return a Response object: stops process_exception() chain
    #     # - return a Request object: stops process_exception() chain
    #     pass

    # def spider_opened(self, spider):
    #     spider.logger.info('Spider opened: %s' % spider.name)


class RotateUserAgentMiddleware(object):
    """Rotate user-agent for each request."""
    def __init__(self):
        self.enabled = False

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.enabled = getattr(spider, 'rotate_user_agent', self.enabled)

    def process_request(self, request, spider):
        if not self.enabled:
            return

        ua = UserAgent(path=settings.PATH_FAKE_USER_AGENT)
        request.headers['user-agent'] = ua.random


class Mode:
    RANDOMIZE_PROXY_EVERY_REQUESTS, RANDOMIZE_PROXY_ONCE = range(2)


class RandomProxyMiddleware(object):

    def __init__(self, settings):
        self.mode = settings.get('PROXY_MODE')
        self.proxies_app = settings.get('PROXIES_APP')
        self.proxies_model = settings.get('PROXIES_MODEL')
        self.websites_app = settings.get('WEBSITES_APP')
        self.websites_model = settings.get('WEBSITES_MODEL')
        self.chosen_proxy = ''
        self.query_proxies = None

        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or\
                self.mode == Mode.RANDOMIZE_PROXY_ONCE:

            self.proxies = {}

            model_proxies = apps.get_model(
                app_label=self.proxies_app,
                model_name=self.proxies_model)

            model_websites = apps.get_model(
                app_label=self.websites_app,
                model_name=self.websites_model)

            self.query_proxies = model_proxies.objects.all()
            self.query_websites = model_websites.objects.all()

    @classmethod
    def from_crawler(cls, crawler):
        c = cls(crawler.settings)
        crawler.signals.connect(c.spider_opened, signal=signals.spider_opened)
        return c

    def spider_opened(self, spider):

        store_id = getattr(spider, 'store_id', None)

        proxies_ok = self.query_proxies.filter(websites__store_id=store_id)

        self.proxies = dict.fromkeys(
            proxies_ok.values_list("ip_proxy", flat=True), '')

        if len(self.proxies) == 0:
            raise ValueError('All proxies are unusable, cannot proceed')

        if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
            self.chosen_proxy = choice(list(self.proxies.keys()))

    # overwrite process request
    def process_request(self, request, spider):

        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            if request.meta["exception"] is False:
                return
        request.meta["exception"] = False

        if len(self.proxies) == 0:
            raise ValueError('All proxies are unusable, cannot proceed')

        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS:
            proxy_address = choice(list(self.proxies.keys()))
        else:
            proxy_address = self.chosen_proxy

        proxy_user_pass = self.proxies[proxy_address]

        if proxy_user_pass:
            request.meta['proxy'] = proxy_address
            basic_auth = 'Basic ' + base64.b64encode(
                proxy_user_pass.encode()).decode()
            request.headers['Proxy-Authorization'] = basic_auth
        else:
            log.debug('Proxy user pass not found')
        log.debug('Using proxy <%s>, %d proxies left' % (
            proxy_address, len(self.proxies)))

    def process_exception(self, request, exception, spider):

        store_id = getattr(spider, 'store_id', None)

        if 'proxy' not in request.meta:
            return
        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or\
                self.mode == Mode.RANDOMIZE_PROXY_ONCE:
            proxy = request.meta['proxy']
            try:
                del self.proxies[proxy]
                p = self.query_proxies.get(ip_proxy=proxy)
                w = self.query_websites.get(store_id=store_id)
                p.websites.remove(w)
                if not p.websites.exists():
                    p.delete()
            except KeyError:
                pass
            request.meta["exception"] = True
            if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
                self.chosen_proxy = choice(list(self.proxies.keys()))
            log.info('Removing failed proxy <%s>, %d proxies left' % (
                proxy, len(self.proxies)))


class RandomProxyMiddleware2(object):

    def __init__(self, settings):
        self.mode = settings.get('PROXY_MODE')
        self.proxies_app = settings.get('PROXIES_APP')
        self.proxies_model = settings.get('PROXIES_MODEL')
        self.chosen_proxy = ''
        self.query_proxies = None

        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or\
                self.mode == Mode.RANDOMIZE_PROXY_ONCE:

            self.proxies = {}

            model_proxies = apps.get_model(
                app_label=self.proxies_app,
                model_name=self.proxies_model)

            self.query_proxies = model_proxies.objects.all()

    @classmethod
    def from_crawler(cls, crawler):
        c = cls(crawler.settings)
        crawler.signals.connect(c.spider_opened, signal=signals.spider_opened)
        return c

    def spider_opened(self, spider):

        self.proxies = dict.fromkeys(
            self.query_proxies.values_list("ip_proxy", flat=True), '')

        if len(self.proxies) == 0:
            raise ValueError('All proxies are unusable, cannot proceed')

        if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
            self.chosen_proxy = choice(list(self.proxies.keys()))

    # overwrite process request
    def process_request(self, request, spider):

        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            if request.meta["exception"] is False:
                return
        request.meta["exception"] = False

        if len(self.proxies) == 0:
            raise ValueError('All proxies are unusable, cannot proceed')

        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS:
            proxy_address = choice(list(self.proxies.keys()))
        else:
            proxy_address = self.chosen_proxy

        proxy_user_pass = self.proxies[proxy_address]

        if proxy_user_pass:
            request.meta['proxy'] = proxy_address
            basic_auth = 'Basic ' + base64.b64encode(
                proxy_user_pass.encode()).decode()
            request.headers['Proxy-Authorization'] = basic_auth
        else:
            log.debug('Proxy user pass not found')
        log.debug('Using proxy <%s>, %d proxies left' % (
            proxy_address, len(self.proxies)))


    # def process_exception(self, request, exception, spider):

    #     store_id = getattr(spider, 'store_id', None)

    #     if 'proxy' not in request.meta:
    #         return
    #     if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or\
    #             self.mode == Mode.RANDOMIZE_PROXY_ONCE:
    #         proxy = request.meta['proxy']
    #         try:
    #             del self.proxies[proxy]
    #             p = self.query_proxies.get(ip_proxy=proxy)
    #             w = self.query_websites.get(store_id=store_id)
    #             p.websites.remove(w)
    #             if not p.websites.exists():
    #                 p.delete()
    #         except KeyError:
    #             pass
    #         request.meta["exception"] = True
    #         if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
    #             self.chosen_proxy = choice(list(self.proxies.keys()))
    #         log.info('Removing failed proxy <%s>, %d proxies left' % (
    #             proxy, len(self.proxies)))
