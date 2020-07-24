# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InstantCoffeeItem(scrapy.Item):
        product_image_urls = scrapy.Field()
        product_name = scrapy.Field()
        rating_avg = scrapy.Field()
        rating_nums = scrapy.Field()
        ASIN = scrapy.Field()
        brand = scrapy.Field()
        price = scrapy.Field()
        amazon_choice = scrapy.Field()
        unit_price = scrapy.Field()
        top_sales_rank = scrapy.Field()
        productDescription = scrapy.Field()
        FBA = scrapy.Field()
        answered_questions = scrapy.Field()
        subscribe = scrapy.Field()
        subscribe_price_5per = scrapy.Field()
        subscribe_price_15per = scrapy.Field()
        shipping_weight = scrapy.Field()
        rating_5_star = scrapy.Field()
        rating_4_star = scrapy.Field()
        rating_3_star = scrapy.Field()
        rating_2_star = scrapy.Field()
        rating_1_star = scrapy.Field()
        product_url = scrapy.Field()
