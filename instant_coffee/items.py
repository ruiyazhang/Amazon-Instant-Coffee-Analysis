# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InstantCoffeeItem(scrapy.Item):
    amazon_choice = scrapy.Field()
    product_name = scrapy.Field()
    product_image = scrapy.Field()
    rating_avg = scrapy.Field()
    rating_num = scrapy.Field()
    answered_questions = scrapy.Field()
    price = scrapy.Field()
    unit_price = scrapy.Field()
    brand = scrapy.Field() 
    prime = scrapy.Field()
    prime_one_day = scrapy.Field()
    fresh = scrapy.Field() 
    item_weight = scrapy.Field()
    shipping_weight = scrapy.Field()
    product_description = scrapy.Field()
    ASIN = scrapy.Field()
    instant_coffee_seller_rank = scrapy.Field()
    grocery_gourmet_good_rank = scrapy.Field()
    five_star_pct = scrapy.Field()
    four_star_pct = scrapy.Field()
    three_star_pct = scrapy.Field()
    two_star_pct = scrapy.Field()
    on_star_pct = scrapy.Field()
