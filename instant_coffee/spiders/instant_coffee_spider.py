from scrapy import Spider, Request
from instant_coffee.items import InstantCoffeeItem
import re
import math

class InstantCoffeeSpider(Spider):
    name = 'instant_coffee_spider'
    allowed_urls = ['https://www.amazon.com/']
    start_urls = ['https://www.amazon.com/s?k=Instant+Coffee&i=grocery&rh=n%3A2251594011&page=1&_encoding=UTF8&c=ts&qid=1594936799&ts_id=2251594011&ref=sr_pg_1']

    def parse(self, response):
        
        url_list = [f'https://www.amazon.com/s?k=Instant+Coffee&i=grocery&rh=n%3A2251594011&page={i}&_encoding=UTF8&c=ts&qid=1594936799&ts_id=2251594011&ref=sr_pg_{i}' for i in range(1,192)]

        # print(len(url_list))

        for url in url_list[:1]:
            yield Request(url=url, callback=self.parse_results_page)
    
    def parse_results_page(self, response):
        product_image_urls = response.xpath('//div[@class="s-main-slot s-result-list s-search-results sg-row"]/div[not(contains(@class, "AdHolder"))]//div[@class="a-section aok-relative s-image-square-aspect"]/img/@src').extract()
        product_name = response.xpath('//div[@class="s-main-slot s-result-list s-search-results sg-row"]/div[not(contains(@class, "AdHolder"))]//h2/a/span/text()').extract()
        product_urls = response.xpath('//div[@class="s-main-slot s-result-list s-search-results sg-row"]/div[not(contains(@class, "AdHolder"))]//h2/a/@href').extract()
        # print('='*50)
        # print(len(product_urls))
        # print(len(product_name))
        # print(len(product_image_urls))
        # print('='*50)
        product_urls = [f'https://www.amazon.com{url}' for url in product_urls]
        for url in product_urls[:8]:
            yield Request(url=url, callback=self.parse_product_page)

    def parse_product_page(self, response):
        brand = response.xpath('//div[@id="bylineInfo_feature_div"]/div/a/text()').extract_first()
        price = response.xpath('//div[@id="price"]//span[@id="priceblock_ourprice"]/text()').extract_first() 

        choice = response.xpath('//div[@id="acBadge_feature_div"]/div[1]//span[@class="a-size-small aok-float-left ac-badge-rectangle"]/span/text()').extract()
        l = ''
        for a in choice:
            l += a
        amazon_choice=(l=='Amazon\'s Choice')
        # print('='*50)
        # print(brand)
        # print(price)
        # print(amazon_choice)
        # print('='*50)
        