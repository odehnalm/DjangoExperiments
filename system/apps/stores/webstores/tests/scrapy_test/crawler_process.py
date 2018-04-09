from os.path import abspath, dirname, join, normpath
from sys import path

import shutil
from lxml import html
from urllib.parse import urlparse
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
# from MAscraper.spiders.auchan import AuchanSpider
from MAscraper.spiders.boulanger import BoulangerSpider
from MAscraper.spiders.amazon import AmazonSpider
from MAscraper.spiders.productscompare import ProductsCompareSpider
# from .MAscraper.spiders.but import ButSpider
# from .MAscraper.spiders.carrefour import CarrefourSpider
# from .MAscraper.spiders.cdiscount import CdiscountSpider
# from .MAscraper.spiders.conforama import ConforamaSpider
# from .MAscraper.spiders.darty import DartySpider
from MAscraper.spiders.groupdigital import GroupDigitalSpider
# from .MAscraper.spiders.electrodepot import ElectrodepotSpider
# from .MAscraper.spiders.fnac import FnacSpider
# from .MAscraper.spiders.kelkoo import KelkooSpider
from MAscraper.spiders.pricerunner import PricerunnerSpider
# from .MAscraper.spiders.reglomobile import ReglomobileSpider
# from .MAscraper.spiders.lcdcompare import LCDCompareSpider

path.append(dirname(abspath(__file__)))
path.append(dirname(dirname(abspath(__file__))))


@defer.inlineCallbacks
def crawl(runners, urls_list):
    runner = runners['runner_punk']


    if 'amazon' in urls_list[0]:
        yield runner.crawl(
            AmazonSpider,
            urls=urls_list
        )

    if 'electromenager-compare' in urls_list[0]:
        yield runner.crawl(
            ProductsCompareSpider,
            urls=urls_list
        )

    if 'group-digital' in urls_list[0]:
        yield runner.crawl(
            GroupDigitalSpider,
            urls=urls_list
        )                    

    if 'pricerunner' in urls_list[0]:
        yield runner.crawl(
            PricerunnerSpider,
            urls=urls_list
        )   

    reactor.stop()


def MAscraperCrawler(urls_list):

    # Lectura del archivo .html
    # urls_f = open(urls_html_file, "r", encoding='utf-8')
    # urls_html = html.fromstring(urls_f.read())
    # urls_f.close()

    # Creamos una lista con cada uno de los URL
    # url_items = [item.get('href') for item in urls_html.getchildren()[0].getchildren()[0].getchildren()]
    url_items = urls_list

    # SITIOS WEB A SCRAPEAR (nombre del dominio)
    # webs2scrap = [urlparse(url).netloc.split('.')[1] for url in url_items]

    #  Limpieza de outputs por cada scraping
    # try:
    #     shutil.rmtree('scrapy_outputs')
    # except:
    #     pass

    runners = {}
    # Random interval between 0.5 * DOWNLOAD_DELAY and
    # 1.5 * DOWNLOAD_DELAY.
    RANDOMIZE_DOWNLOAD_DELAY = True
    DOWNLOAD_DELAY = 1.0

    # Retry many times since proxies often fail
    RETRY_TIMES = 30

    PROXY_MODE = 0

    # Retry on most error codes since proxies fail for different reasons
    RETRY_HTTP_CODES = [503, 504, 400, 403, 408, 429]

    SPIDER_MIDDLEWARES = {
       # 'MAscraper.middlewares.MascraperSpiderMiddleware': 543,
       'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,    
    }

    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        # 'scrapy_proxies.RandomProxy': 100,
        'scrapy_test.MAscraper.middlewares.RandomProxy': 100,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        'scrapy_test.MAscraper.middlewares.RotateUserAgentMiddleware': 120,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 300,
        # SPLASH middlewares
        # !!! HttpCompressionMiddleware priority should be changed in order to allow advanced response processing; see https://github.com/scrapy/scrapy/issues/1895 for details.
        'scrapy_splash.SplashCookiesMiddleware': 723,
        'scrapy_splash.SplashMiddleware': 725,
        'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,    
    }

    ITEM_PIPELINES = {
        'scrapy_test.MAscraper.pipelines.MascraperPipeline': 400,
    }


    # SPLASH SETTINGS

    # '''
    #
    #                         ##         .
    #                   ## ## ##        ==
    #                ## ## ## ## ##    ===
    #            /"""""""""""""""""\___/ ===
    #       ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
    #            \______ o           __/
    #              \    \         __/
    #               \____\_______/
    #
    # docker is configured to use the default machine with IP 192.168.99.100
    # For help getting started, check out the docs at https://docs.docker.com

    SPLASH_URL = 'http://0.0.0.0:8050'

    DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

    HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

    # IMPORTACION DE CONFIGURACION
    # settings = get_project_settings()
    # Import config
    settings_scrapy = Settings()

    # EDICION DE CONFIGURACION DESDE ESTE MISMO SCRIPT
    settings_scrapy.overrides['FEED_FORMAT'] = 'json'
    settings_scrapy.overrides['FEED_EXPORT_INDENT'] = 3
    settings_scrapy.overrides['FEED_EXPORT_ENCODING'] = 'utf-8'
    settings_scrapy.overrides['FEED_URI'] = 'scrapy_outputs/result_%(name)s.json'

    settings_scrapy.set(
        'DOWNLOADER_MIDDLEWARES', DOWNLOADER_MIDDLEWARES, priority='cmdline')

    settings_scrapy.set(
        'SPLASH_URL', SPLASH_URL, priority='cmdline')
    settings_scrapy.set(
        'DUPEFILTER_CLASS', DUPEFILTER_CLASS, priority='cmdline')
    settings_scrapy.set(
        'HTTPCACHE_STORAGE', HTTPCACHE_STORAGE, priority='cmdline')                  

    settings_scrapy.set('RETRY_TIMES', RETRY_TIMES, priority='cmdline')
    settings_scrapy.set('RETRY_HTTP_CODES', RETRY_HTTP_CODES, priority='cmdline')
    settings_scrapy.set('PROXY_MODE', PROXY_MODE, priority='cmdline')
    settings_scrapy.set('FEED_EXPORT_ENCODING', 'utf-8', priority='cmdline')
    settings_scrapy.set('DOWNLOAD_DELAY', DOWNLOAD_DELAY, priority='cmdline')
    settings_scrapy.set(
        'RANDOMIZE_DOWNLOAD_DELAY',
        RANDOMIZE_DOWNLOAD_DELAY,
        priority='cmdline'
    )
    settings_scrapy.set('ITEM_PIPELINES', ITEM_PIPELINES, priority='cmdline')
    settings_scrapy.set('ROBOTSTXT_OBEY', False, priority='cmdline')

    # Separamos los scrapers a sitios abiertos y los más privados
    # Sitios abiertos a nuestros robots
    runner_punk = CrawlerRunner(settings_scrapy)
    runners['runner_punk'] = runner_punk

    configure_logging()

    crawl(runners, urls_list)
    reactor.run()

    # # Sitios cerrados a nuestros robots
    # settings_punk = get_project_settings()
    # settings_punk.overrides['FEED_FORMAT'] = 'json'
    # settings_punk.overrides['FEED_EXPORT_INDENT'] = 3
    # settings_punk.overrides['FEED_EXPORT_ENCODING'] = 'utf-8'
    # settings_punk.overrides['FEED_URI'] = 'scrapy_outputs/result_%(name)s.json'
    # settings_punk.overrides['ROBOTSTXT_OBEY'] = False
    # runner_punk = CrawlerRunner(settings_punk)

    

    # @defer.inlineCallbacks
    # def crawl():
    #     # OBEY ROBOTS
    #     if 'auchan' in webs2scrap:
    #         yield runner_obey.crawl(AuchanSpider,urls=[url_items[webs2scrap.index('auchan')]])
    #     if 'boulanger' in webs2scrap:
    #         yield runner_obey.crawl(BoulangerSpider,urls=[url_items[webs2scrap.index('boulanger')]])
    #     if 'but' in webs2scrap:
    #        yield runner_obey.crawl(ButSpider,urls=[url_items[webs2scrap.index('but')]])
    #     if 'cdiscount' in webs2scrap:
    #        yield runner_obey.crawl(CdiscountSpider,urls=[url_items[webs2scrap.index('cdiscount')]])
    #     if 'conforama' in webs2scrap:
    #         yield runner_obey.crawl(ConforamaSpider,urls=[url_items[webs2scrap.index('conforama')]])
    #     if 'electrodepot' in webs2scrap:
    #         yield runner_obey.crawl(ElectrodepotSpider,urls=[url_items[webs2scrap.index('electrodepot')]])
    #     if 'fnac' in webs2scrap:
    #         yield runner_obey.crawl(FnacSpider,urls=[url_items[webs2scrap.index('fnac')]])
    #     if 'kelkoo' in webs2scrap:
    #         yield runner_obey.crawl(KelkooSpider,urls=[url_items[webs2scrap.index('kelkoo')]])
    #     if 'pricerunner' in webs2scrap:
    #         yield runner_obey.crawl(PricerunnerSpider,urls=[url_items[webs2scrap.index('pricerunner')]])
    #     if 'reglomobile' in webs2scrap:
    #         yield runner_obey.crawl(ReglomobileSpider,urls=[url_items[webs2scrap.index('reglomobile')]])
    #     if 'darty' in webs2scrap:
    #        yield runner_obey.crawl(DartySpider,urls=[url_items[webs2scrap.index('darty')]])

    #     # DISOBEY ROBOTS
    #     if 'group-digital' in webs2scrap:
    #         yield runner_punk.crawl(GroupDigitalSpider,urls=[url_items[webs2scrap.index('group-digital')]])
    #     if 'rueducommerce' in webs2scrap:
    #       yield runner_punk.crawl(CarrefourSpider,urls=[url_items[webs2scrap.index('rueducommerce')]])
    #     if 'lcd-compare' in webs2scrap:
    #       yield runner_punk.crawl(LCDCompareSpider,urls=[url_items[webs2scrap.index('lcd-compare')]])

    #     reactor.stop()

    # crawl()
    # reactor.run() # the script will block here until the last crawl call is finished
    #,urls=['https://www.auchan.fr/soldes/soldes-electromenager/soldes-gros-electromenager/soldes-froid/c-888017126']

# urls_list = [
#     'https://www.boulanger.com/c/nav-filtre/smartphone-telephone-portable?brand~apple|facettes_gsm_____taille_de_l_ecran~22c42220soit2062c120cm;42c72220soit20112c920cm;22c32220soit2052c820cm;12c772220soit2042c4920cm;42220soit20102c120cm;42c52220soit20112c420cm;42c82220soit20122c220cm;12c72220soit2042c320cm;12c82220soit2042c620cm;42c62220soit20112c720cm;22c82220soit2072c120cm;32c52220soit2082c920cm;22c22220soit2052c620cm;22220soit20520cm;22c62220soit2062c620cm|facettes_gsm_____memoire_interne~3220go|facettes_gsm_____memoire_interne~6420go;12820go;25620go|memoire_____memoire_ram~220go;320go|memoire_____memoire_ram~420go;320go;620go|facettes_communes_____coloris~noir&amp;sorting_price=asc',
# ]

urls_list = [
    "http://www.pricerunner.fr/cl/27/Ordinateurs-portables?man_id=310#attr_60382335=60382369&sort=3",
]

MAscraperCrawler(urls_list)

