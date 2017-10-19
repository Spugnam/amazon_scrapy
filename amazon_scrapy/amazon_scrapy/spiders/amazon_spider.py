#! /usr/local/bin/python2

from scrapy import Spider
from scrapy import Request
from scrapy.selector import Selector
from amazon_scrapy.items import AmazonScrapyItem
from datetime import datetime
from scrapy_proxies import *

class AmazonSpider(Spider):
    name = "amazon_spider"
    allowed_urls = ['https://www.amazon.com']
    start_urls = ['https://www.amazon.com/Networking-Computer-Add-Ons-Computers/b/ref=nav_shopall_networking?ie=UTF8&node=172504']

    def parse(self, response):
        category_url_list = response.xpath('//*[@class="a-link-normal acs_tile__title-image aok-block a-text-normal"]/@href').extract() # returns url list: u'/b?_encoding=UTF8&node=300189'
        category_url_list = ['https://www.amazon.com' + url for url in category_url_list] # leads to 'Routers' page

        for url in category_url_list:
            print("***Category url***: ", url)
            yield Request(url, callback=self.parse_category)

    def parse_category(self, response):

        # TO DO: get category 'Routers'
        category = response.xpath('//li[@class="s-ref-indent-one"]//h4/text()').extract_first() # u'Routers'

        product_node = response.xpath('//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@href').extract()
        products_url_list = response.xpath('//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@href').extract()
        # returns list of product urls:  u'https://www.amazon.com/Google-Wifi-system-set-replacement/dp/B01MAW2294'

        # Call parse product
        for url in products_url_list:
            #print("***Product url***: ", url)
            if ('picassoRedirect' not in url):  # filter out sponsored products -links break and they are duplicates
                print("=" * 20)
                print("Going to Product Page: ", url)
                yield Request(url, callback=self.parse_product, meta={'category': category})

        # if possible click link to next page and call parse_category recursively
        next_page_url = response.xpath('//a[@id="pagnNextLink"]/@href').extract_first()  # u'/Routers-Networking-Products/s?ie=UTF8&page=2&rh=n%3A300189'

        try: # to catch empty url if no next page
            if (len(next_page_url)>0):
                next_page_url = "https://www.amazon.com" + next_page_url
                print("="*20)
                print("Clicking Next: ", next_page_url)
                yield Request(next_page_url, self.parse_category)  # recursive call
        except:
            pass

    def parse_product(self, response):

        company = response.xpath('//a[@id="bylineInfo"]/text()').extract_first()
        category = response.meta['category']

        product_desc = response.xpath('//span[@id="productTitle"]/text()').extract_first() # u'Google Wifi system (set of 3) - Router replacement for whole home coverage'
        if product_desc is not None:
            product_desc = product_desc.replace('\n','').strip()

        ASIN = response.xpath('//input[@id="ASIN"]/@value').extract_first()  # 'B075XLWML4'
        # num_review = scrapy.Field()
        num_review = response.xpath('//span[@data-hook="total-review-count"]/text()').extract_first()  # u'2,402'
        #num_review = int(num_review.replace(',',''))  keep as string for now
        # rating = scrapy.Field()
        rating = response.xpath('//span[@data-hook="rating-out-of-text"]/text()').extract_first()  # u'4.4 out of 5 stars'
        if rating is not None:
            rating = float(rating.split(' ')[0]) # throws Nonetype error

        # click on 'see all xx reviews' link
        all_reviews_url = response.xpath('//a[@id="dp-summary-see-all-reviews"]/@href').extract_first()
        # '/Linksys-AC3200-Dual-Band-Prioritization-WRT32X/product-reviews/B072LQZFHM/ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=all_reviews'

        try:  # to catch products without reviews
            if (len(all_reviews_url)>0):
                all_reviews_url = "https://www.amazon.com" + all_reviews_url
                print("=" * 20)
                print("Going to all reviews: ", all_reviews_url)
                yield Request(all_reviews_url, callback=self.parse_reviews, meta={'company': company,
                                                                                  'category': category,
                                                                                  'product_desc': product_desc,
                                                                                  'ASIN': ASIN,
                                                                                  'num_review': num_review,
                                                                                  'rating': rating})
        except:
            pass

    def parse_reviews(self, response):

        company = response.meta['company']
        category = response.meta['category']
        product_desc = response.meta['product_desc']
        ASIN = response.meta['ASIN']
        num_review = response.meta['num_review']
        rating = response.meta['rating']

        reviews = response.xpath('//div[@data-hook="review"]')  # top node to use for all review elements

        # TO DO: add next page on reviews

        for review in reviews:
            # review_rating = scrapy.Field()
            review_rating = review.xpath('.//i[@data-hook="review-star-rating"]//text()').extract_first()  # u'4.4 out of 5 stars'
            review_rating = float(review_rating.split(' ')[0])
            # review_date = scrapy.Field()
            review_date = review.xpath('.//span[@data-hook="review-date"]//text()').extract_first()  # u'on December 7, 2016'
            review_date = ' '.join(review_date.split(' ')[1:]) # 'December 7, 2016'
            review_date = datetime.strptime(review_date, '%B %d, %Y').strftime('%x')  # convert to locale 08/16/1988 (en_US)
            # review_body = scrapy.Field()
            review_body = review.xpath('.//span[@data-hook="review-body"]//text()').extract()
            review_body = review_body[0]

            item = AmazonScrapyItem()
            item['category'] = category
            item['company'] = company
            item['product_desc'] = product_desc
            item['ASIN'] = ASIN
            item['num_review'] = num_review
            item['rating'] = rating
            item['review_rating'] = review_rating
            item['review_date'] = review_date
            item['review_body'] = review_body

            yield item

        # Click next on reviews page
        next_page_reviews = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        # '/All-New-Fire-TV-Stick-With-Alexa-Voice-Remote-Streaming-Media-Player/product-reviews/B00ZV9RDKK/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&pageNumber=2&reviewerType=all_reviews'


        try: # to catch empty url if no next page
            if (len(next_page_reviews)>0):
                next_page_reviews = "https://www.amazon.com" + next_page_reviews
                print("="*30)
                print("Clicking Next (Reviews): ", next_page_reviews)
                yield Request(next_page_reviews,
                              callback=self.parse_reviews,
                              meta={'company': company,
                                    'category': category,
                                    'product_desc': product_desc,
                                    'ASIN': ASIN,
                                    'num_review': num_review,
                                    'rating': rating})  # recursive call
        except:
            pass