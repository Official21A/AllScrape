import scrapy


class GoogleSearch(scrapy.Spider):
    name = "google"

    start_urls = ['https://www.google.com/']

    def parse(self, response):
        