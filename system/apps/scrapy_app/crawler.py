import os
import shutil

from django.conf import settings

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from twisted.internet import defer, reactor

from .scrapy_app.spiders.basic_spider import BasicSpider
from .scrapy_app.spiders.cpubenchmark import CPUBenchmarkSpider
from .scrapy_app.spiders.gpubenchmark import GPUBenchmarkSpider


@defer.inlineCallbacks
def crawl(runners, dict_data_stores):
    job_id = dict_data_stores.pop("job_id")
    item_category = dict_data_stores.pop("item_category")
    country = dict_data_stores.pop("country")
    for name_scraper, data_scraper in dict_data_stores.items():
        if data_scraper['robots_OK']:
            runner = runners['runner_obey']
        else:
            runner = runners['runner_punk']

        if item_category == "COMPU_000":
            max_items = settings.BIG_NUM_ITEMS
        else:
            max_items = settings.DEFAULT_NUM_ITEMS

        if country == "es" and item_category == "TV_000":
            max_items = 10

        yield runner.crawl(
            BasicSpider,
            allowed_domain=data_scraper['allowed_domain'],
            url=data_scraper['url'],
            name_scraper=name_scraper,
            job_id=job_id,
            item_category=item_category,
            store_id=data_scraper['store_id'],
            max_items=max_items
        )
    reactor.stop()


def crawler_process(dict_data_stores):
    # try:
    #     TMP_FOLDER = settings.TMP_FOLDER
    # except AttributeError:
    #     raise AttributeError(
    #         "Debe definir en el archivo "
    #         "settings la variable TMP_FOLDER")

    runners = {}

    # Import config
    settings_obey = Settings()


    # Random interval between 0.5 * DOWNLOAD_DELAY and
    # 1.5 * DOWNLOAD_DELAY.
    RANDOMIZE_DOWNLOAD_DELAY = True
    DOWNLOAD_DELAY = 1
    CONCURRENT_REQUESTS = 1

    # Retry many times since proxies often fail
    RETRY_TIMES = 20

    # Retry on most error codes since proxies fail for different reasons
    RETRY_HTTP_CODES = [503, 504, 400, 403, 408, 429]

    PROXIES_APP = settings.PROXIES_APP
    PROXIES_MODEL = settings.PROXIES_MODEL
    WEBSITES_APP = settings.WEBSITES_APP
    WEBSITES_MODEL = settings.WEBSITES_MODEL
    PROXY_MODE = 0

    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        # 'scrapy_proxies.RandomProxy': 100,
        'apps.scrapy_app.scrapy_app.middlewares.RandomProxyMiddleware': 100,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        'apps.scrapy_app.scrapy_app.middlewares.RotateUserAgentMiddleware': 120,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 300,
        'apps.scrapy_app.scrapy_app.middlewares.ScrapyAppDownloaderMiddleware': 543,
    }

    ITEM_PIPELINES = {
        'apps.scrapy_app.scrapy_app.pipelines.ScrapyAppPipeline': 400,
    }

    # EDICION DE CONFIGURACION DESDE ESTE MISMO SCRIPT
    settings_obey.set(
        'DOWNLOADER_MIDDLEWARES', DOWNLOADER_MIDDLEWARES, priority='cmdline')
    settings_obey.set('RETRY_TIMES', RETRY_TIMES, priority='cmdline')
    settings_obey.set('RETRY_HTTP_CODES', RETRY_HTTP_CODES, priority='cmdline')
    settings_obey.set('PROXIES_APP', PROXIES_APP, priority='cmdline')
    settings_obey.set('PROXIES_MODEL', PROXIES_MODEL, priority='cmdline')
    settings_obey.set('WEBSITES_APP', WEBSITES_APP, priority='cmdline')
    settings_obey.set('WEBSITES_MODEL', WEBSITES_MODEL, priority='cmdline')
    settings_obey.set('PROXY_MODE', PROXY_MODE, priority='cmdline')
    settings_obey.set('FEED_EXPORT_ENCODING', 'utf-8', priority='cmdline')
    settings_obey.set('DOWNLOAD_DELAY', DOWNLOAD_DELAY, priority='cmdline')
    settings_obey.set(
        'RANDOMIZE_DOWNLOAD_DELAY',
        RANDOMIZE_DOWNLOAD_DELAY,
        priority='cmdline')
    settings_obey.set(
        'CONCURRENT_REQUESTS',
        CONCURRENT_REQUESTS,
        priority='cmdline')
    settings_obey.set('ITEM_PIPELINES', ITEM_PIPELINES, priority='cmdline')

    # Separamos los scrapers a sitios abiertos y los más privados
    # Sitios abiertos a nuestros robots
    runner_obey = CrawlerRunner(settings_obey)
    runners['runner_obey'] = runner_obey

    # Sitios cerrados a nuestros robots
    settings_punk = Settings()

    # EDICION DE CONFIGURACION DESDE ESTE MISMO SCRIPT
    settings_punk.set(
        'DOWNLOADER_MIDDLEWARES', DOWNLOADER_MIDDLEWARES, priority='cmdline')
    settings_punk.set('RETRY_TIMES', RETRY_TIMES, priority='cmdline')
    settings_punk.set('RETRY_HTTP_CODES', RETRY_HTTP_CODES, priority='cmdline')
    settings_punk.set('PROXIES_APP', PROXIES_APP, priority='cmdline')
    settings_punk.set('PROXIES_MODEL', PROXIES_MODEL, priority='cmdline')
    settings_punk.set('WEBSITES_APP', WEBSITES_APP, priority='cmdline')
    settings_punk.set('WEBSITES_MODEL', WEBSITES_MODEL, priority='cmdline')
    settings_punk.set('PROXY_MODE', PROXY_MODE, priority='cmdline')
    settings_punk.set('FEED_EXPORT_ENCODING', 'utf-8', priority='cmdline')
    settings_punk.set('DOWNLOAD_DELAY', DOWNLOAD_DELAY, priority='cmdline')
    settings_punk.set(
        'RANDOMIZE_DOWNLOAD_DELAY',
        RANDOMIZE_DOWNLOAD_DELAY,
        priority='cmdline'
    )
    settings_punk.set(
        'CONCURRENT_REQUESTS',
        CONCURRENT_REQUESTS,
        priority='cmdline')
    settings_punk.set('ITEM_PIPELINES', ITEM_PIPELINES, priority='cmdline')
    settings_punk.set('ROBOTSTXT_OBEY', False, priority='cmdline')

    runner_punk = CrawlerRunner(settings_punk)
    runners['runner_punk'] = runner_punk

    configure_logging()

    crawl(runners, dict_data_stores)
    reactor.run()


def benchmarks_crawler():

    #  Limpieza de outputs por cada scraping
    try:
        os.remove(settings.BASE_DIR + '/system/data/CPU_Benchmark.json')
        os.remove(settings.BASE_DIR + '/system/data/GPU_Benchmark.json')
    except:
        pass

    # Random interval between 0.5 * DOWNLOAD_DELAY and
    # 1.5 * DOWNLOAD_DELAY.
    RANDOMIZE_DOWNLOAD_DELAY = True
    DOWNLOAD_DELAY = 0.5

    # Retry many times since proxies often fail
    RETRY_TIMES = 100

    # Retry on most error codes since proxies fail for different reasons
    RETRY_HTTP_CODES = [503, 504, 400, 403, 408, 429]

    PROXIES_APP = settings.PROXIES_APP
    PROXIES_MODEL = settings.PROXIES_MODEL
    PROXY_MODE = 0

    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        # 'scrapy_proxies.RandomProxy': 100,
        'apps.scrapy_app.scrapy_app.middlewares.RandomProxyMiddleware2': 100,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        'apps.scrapy_app.scrapy_app.middlewares.RotateUserAgentMiddleware': 120,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 300,
    }

    ITEM_PIPELINES = {
        'apps.scrapy_app.scrapy_app.pipelines.BenchmarkScraperPipeline': 400,
    }

    # Sitios cerrados a nuestros robots
    settings_obey = Settings()

    # EDICION DE CONFIGURACION DESDE ESTE MISMO SCRIPT
    settings_obey.set(
        'DOWNLOADER_MIDDLEWARES', DOWNLOADER_MIDDLEWARES, priority='cmdline')
    settings_obey.set('RETRY_TIMES', RETRY_TIMES, priority='cmdline')
    settings_obey.set('RETRY_HTTP_CODES', RETRY_HTTP_CODES, priority='cmdline')
    settings_obey.set('PROXIES_APP', PROXIES_APP, priority='cmdline')
    settings_obey.set('PROXIES_MODEL', PROXIES_MODEL, priority='cmdline')
    settings_obey.set('PROXY_MODE', PROXY_MODE, priority='cmdline')
    settings_obey.set('FEED_FORMAT', 'json', priority='cmdline')
    settings_obey.set('FEED_EXPORT_INDENT', 3, priority='cmdline')
    settings_obey.set('FEED_EXPORT_ENCODING', 'utf-8', priority='cmdline')
    settings_obey.set('FEED_URI', settings.BASE_DIR + '/system/data/%(name)s.json', priority='cmdline')
    settings_obey.set('DOWNLOAD_DELAY', DOWNLOAD_DELAY, priority='cmdline')
    settings_obey.set(
        'RANDOMIZE_DOWNLOAD_DELAY',
        RANDOMIZE_DOWNLOAD_DELAY,
        priority='cmdline'
    )
    settings_obey.set('ITEM_PIPELINES', ITEM_PIPELINES, priority='cmdline')
    settings_obey.set('ROBOTSTXT_OBEY', False, priority='cmdline')

    # Separamos los scrapers a sitios abiertos y los más privados
    # Sitios abiertos a nuestros robots
    runner_obey = CrawlerRunner(settings_obey)

    configure_logging()

    @defer.inlineCallbacks
    def crawl():
        # OBEY ROBOTS
        yield runner_obey.crawl(CPUBenchmarkSpider,urls=["https://www.cpubenchmark.net/CPU_mega_page.html"])
        yield runner_obey.crawl(GPUBenchmarkSpider,urls=["https://www.videocardbenchmark.net/GPU_mega_page.html"])

        reactor.stop()

    crawl()
    reactor.run() # the script will block here until the last crawl call is finished
    #,urls=['https://www.auchan.fr/soldes/soldes-electromenager/soldes-gros-electromenager/soldes-froid/c-888017126']
