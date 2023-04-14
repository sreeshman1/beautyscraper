# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import os


class BeautyscraperPipeline:
    file = None
    csv_writer = None

    def open_spider(self, spider):
        self.file = open("ulta_products.csv", "w",
                         newline="", encoding="utf-8")
        self.csv_writer = csv.DictWriter(
            self.file,
            fieldnames=["name", "brand", "price", "ingredients", "images"],
        )
        self.csv_writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.csv_writer.writerow(item)
        return item
