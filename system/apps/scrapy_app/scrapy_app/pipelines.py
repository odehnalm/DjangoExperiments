# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from apps.tasks.models import Job


class ScrapyAppPipeline(object):

    def __init__(self, job_id, *args, **kwargs):
        self.job_id = job_id
        self.items = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            job_id=crawler.settings.get('job_id'),
        )

    def process_item(self, item, spider):
        spider.log('ITEM SAVE: ------', logging.INFO)
        job = Job.objects.get(pk=item["job_id"])

        if item["nombre"] and item["detalles"] and\
                item["tiendas"] and item["ficha_tecnica"]:

            job.substitution_similar_results.create(
                nombre=item["nombre"],
                ficha_tecnica=item["ficha_tecnica"],
                detalles=item["detalles"],
                tiendas=item["tiendas"],
                store_id=item["store_id"],
                category_id=item["category_id"]
            )
        return item


class BenchmarkScraperPipeline(object):
    def process_item(self, item, spider):
        return item
