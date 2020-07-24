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

        for url in url_list:
            yield Request(url=url, callback=self.parse_results_page)
    
    def parse_results_page(self, response):
        product_image_urls = response.xpath('//div[@class="s-main-slot s-result-list s-search-results sg-row"]/div[not(contains(@class, "AdHolder"))]//div[@class="a-section aok-relative s-image-square-aspect"]/img/@src').extract()
        product_name = response.xpath('//div[@class="s-main-slot s-result-list s-search-results sg-row"]/div[not(contains(@class, "AdHolder"))]//h2/a/span/text()').extract()
        product_urls = response.xpath('//div[@class="s-main-slot s-result-list s-search-results sg-row"]/div[not(contains(@class, "AdHolder"))]//h2/a/@href').extract()

        product_urls = [f'https://www.amazon.com{url}&psc=1' for url in product_urls]

        for index in range(len(product_urls)):
            url = product_urls[index]

            meta = {
                'product_image_url': product_image_urls[index],
                'product_name': product_name[index],
                'product_url': product_urls[index]
            }
    
            yield Request(url=url, callback=self.parse_product_page, meta=meta)

    def parse_product_page(self, response):
        
        index_of_dp=response.url.find('/dp/')
        url_1 = response.url[index_of_dp+4:]
        index_of_ref =url_1.find('/ref=')
        ASIN = url_1[:index_of_ref]

        brand_1_try = response.xpath('//div[@id="bylineInfo_feature_div"]/div/a/text()').extract_first()
        brand_2_try = response.xpath('//div[@id="bylineInfoUS_feature_div"]/div[@class="a-section a-spacing-none"]/text()').extract_first()
        brand = brand_1_try or brand_2_try
        
        try:
            brand=str.strip(brand)
        except:
            None
            

        price_first_try= response.xpath('//div[@id="price"]//span[@id="priceblock_ourprice"]/text()').extract_first()
        price_second_try= response.xpath('//tr[@id="almDetailPagePrice_buying_price"]//span[@id="priceblock_ourprice"]/text()').extract_first()
        price_third_try = response.xpath('//span[@class="a-color-price"]/text()').extract_first()
        price = price_first_try or price_second_try or price_third_try
                
        choice = response.xpath('//div[@id="acBadge_feature_div"]/div[1]//span[@class="a-size-small aok-float-left ac-badge-rectangle"]/span/text()').extract()
        l = ''
        for a in choice:
            l += a
        amazon_choice=(l=='Amazon\'s Choice')

        unit_price_first_try = response.xpath('//div[@id="unifiedPrice_feature_div"]//tr[@id="priceblock_ourprice_row"]//span[@class="a-size-small a-color-price"]/text()').extract_first()
        unit_price_first_try_2=response.xpath('//tr[@id="almDetailPagePrice_buying_price"]//span[@class="a-size-small a-color-price"]/text()').extract_first()
        unit_price_second_try = response.xpath('//tr[@id="almDetailPagePrice_buying_price"]//tr[@id="priceblock_ourprice_row"]//td[@class="a-span12"]/span[@class="a-size-small a-color-price"]/text()').extract_first()
        unit_price_third_try = response.xpath('//div[@id="detail-bullets"]/table//div[@class="content"]/ul/li[1]/text()').extract_first()
        unit_price_fourth_try = response.xpath('//table[@id="productDetails_detailBullets_sections1"]//tr[2]/td[@class="a-size-base"]/text()').extract_first()
        unit_price_fifth_try = response.xpath('//div[@id="detail-bullets"]/table//div[@class="disclaim"]/strong[last()]/text()').extract_first()

        unit_price = unit_price_first_try or unit_price_first_try_2 or unit_price_second_try or unit_price_third_try or unit_price_fourth_try or unit_price_fifth_try

        try:
            unit_price = str.strip(unit_price)
        except:
            None

        top_sales_rank = response.xpath('//li[@class="zg_hrsr_item"][last()]/span[@class="zg_hrsr_rank"]/text()').extract_first()
        top_sales_rank = top_sales_rank or response.xpath('//table[@id="productDetails_detailBullets_sections1"]//tr[9]/td/span/span[2]/text()').extract_first()
        
        try:
            top_sales_rank = int((re.findall('#(\d+)',top_sales_rank))[0])
        except:
            None

        rating_avg = response.xpath('//div[@id="reviewsMedley"]//div[@class="a-fixed-left-grid AverageCustomerReviews a-spacing-small"]//span[@class="a-icon-alt"]/text()').extract_first()
        try:
            rating_avg = float((re.findall('\d+\.\d+',rating_avg))[0])
        except:
            None

        rating_nums = response.xpath('//div[@id="reviewsMedley"]//div[@class="a-row a-spacing-medium averageStarRatingNumerical"]//span[@class="a-size-base a-color-secondary"]/text()').extract_first()
        try:
            rating_nums = int("".join(re.findall('\d+', rating_nums)))
        except:
            None

        productDescription = response.xpath('//div[@id="productDescription"]//p/text()').extract_first()
        try:
            productDescription=str.strip(productDescription)
        except:
            None

        FBA_1_try= response.xpath('//div[@class="a-section a-spacing-none a-spacing-top-base"]/span/text()').extract_first()
        FBA_2_try= ''.join(response.xpath('//div[@id="merchant-info"]//text()').extract())
        FBA_3_try= response.xpath('//div[@id="fresh-merchant-info"]/text()').extract_first()
        
        FBA = FBA_1_try or FBA_2_try or FBA_3_try
        
        try:
            FBA = str.strip(FBA)
        except:
            None

        answered_questions = response.xpath('//a[@id="askATFLink"]/span[@class="a-size-base"]/text()').extract_first()
        try:
            answered_questions=re.findall('(\d+) answered questions',str.strip(answered_questions))
            answered_questions=int(str.strip(answered_questions[0]))
        except:
            None

        subscribe=response.xpath('//div[@class="a-section a-spacing-none a-padding-none"]/span[@class="a-text-bold"]/text()').extract_first()
        try:
            subscribe  = str.strip(subscribe)
        except:
            None

        subscribe_price = response.xpath('//span[@id="subscriptionPrice"]//text()').extract()
        try:
            subscribe_price=list(map(str.strip,subscribe_price))
            subscribe_price=[i for i in subscribe_price if i]
        except:
            None
        
        subscribe_price_5per=None
        subscribe_price_15per=None
        try:
            subscribe_price_5per,subscribe_price_15per=subscribe_price
        except:
            None


        shipping_weight = None
        for i in range(5):
            shipping_weight_label=response.xpath(f'//div[@id="detail-bullets"]/table//div[@class="content"]/ul/li[{i}]/b/text()').extract_first()
            if shipping_weight_label == 'Shipping Weight:':
                shipping_weight=response.xpath(f'//div[@id="detail-bullets"]/table//div[@class="content"]/ul/li[{i}]/text()').extract_first()
        
        ratings = response.xpath('//table[@id="histogramTable"]//tr/td[@class="a-text-right a-nowrap"]/span[last()]//text()').extract()
        try:
            ratings=list(map(str.strip,ratings))
            ratings=[i for i in ratings if i]
        except:
            None
        
        rating_5_star, rating_4_star,rating_3_star,rating_2_star,rating_1_star = ratings

        item = InstantCoffeeItem()
        item['product_image_urls'] = response.meta['product_image_url']
        item['product_name'] = response.meta['product_name']
        item['product_url'] = response.meta['product_url']
        item['rating_avg'] = rating_avg
        item['rating_nums'] = rating_nums
        item['ASIN'] = ASIN
        item['brand'] = brand
        item['price'] = price
        item['amazon_choice'] = amazon_choice
        item['unit_price'] = unit_price
        item['top_sales_rank'] = top_sales_rank
        item['productDescription'] = productDescription
        item['FBA'] = FBA
        item['answered_questions'] = answered_questions
        item['subscribe'] = subscribe
        item['subscribe_price_5per'] = subscribe_price_5per
        item['subscribe_price_15per'] = subscribe_price_15per
        item['shipping_weight'] = shipping_weight
        item['rating_5_star'] = rating_5_star
        item['rating_4_star'] = rating_4_star
        item['rating_3_star'] = rating_3_star
        item['rating_2_star'] = rating_2_star
        item['rating_1_star'] = rating_1_star

        yield item
        