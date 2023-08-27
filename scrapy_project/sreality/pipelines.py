# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy_project.db import PostgresDbConnector
from scrapy_project import db

class DatabasePipeline:
    local_db = PostgresDbConnector(db.DB_PARAMS, db.DB_CUSTOM_PARAMS)

    def open_spider(self, spider):
        print(f"Opening {spider.name} spider...")
        self.local_db.init()
        self.local_db.create_table()

    def close_spider(self, spider):
        print(f"Closing {spider.name} spider...")
        self.local_db.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        try:
            self.local_db.insert_data(dict(adapter))
            print(dict(adapter))
            return item
        except:
            raise DropItem()
        