# -*- coding: utf-8 -*-
import scrapy
from django.http import HttpResponse
from scrapy.crawler import CrawlerProcess

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    start_urls = [
        'https://www.amazon.com/s?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A193870011%2Cn%3A17923671011%2Cn%3A284822&page=2&qid=1573925377&ref=lp_284822_pg_2'
    ]

    def parse(self, response):
        # div_class = 'sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28'
        # containers = response.css("div.{}".format(div_class))
        product = response.css('.a-color-base.a-text-normal::text').extract()
        price = response.css('.a-offscreen::text').extract()
        shipping = response.css('.s-align-children-center .s-align-children-center+ .a-row span::text').extract()
        with open('GPU_Data_Amazon.csv', 'w') as f:
            f.write("product,brand,price,shipping\n")
            for i in range(len(product)):
                curr_product = product[i].replace(","," ")
                brand = curr_product[0:curr_product.find(" ")]
                curr_price = price[i].replace(",","")
                cur_ship = shipping[0]

                if cur_ship != "FREE Shipping by Amazon":
                    cur_ship = "prime"

                f.write("{},{},{},{}\n".format(curr_product, brand, curr_price, cur_ship))
            f.close()
        yield {
                "product":product,
                "price":price
            }

process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
})


def call_scraper(request):
    process.crawl(AmazonSpiderSpider)
    process.start()
    with open('GPU_Data_Amazon.csv') as myfile:
            response = HttpResponse(myfile, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=GPU_Data_Amazon.csv'
            return response


