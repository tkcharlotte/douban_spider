#coding:utf-8
import scrapy
from douban_spider.items import DoubanSpiderItem
from scrapy.http import Request
from scrapy.selector import Selector

class Top250(scrapy.Spider):
    name = 'douban'

    start_urls = ['https://movie.douban.com/top250']
    headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',} 

    def start_requests(self):
     url = 'https://movie.douban.com/top250'
     yield Request(url,headers=self.headers,callback=self.parse)

    def parse(self,response):
        item = DoubanSpiderItem()
        #selector = Selector(response)
        #all_movie = selector.xpath('//div[@class="info"]')
        for r in response.css('div.item'):
            item['rank'] = r.css('div.pic em::text').extract()
            item['name'] = r.css('div.info div.hd a span.title::text').extract_first()             
            item['score'] = r.css('div.info div.bd div.star span.rating_num::text').extract()
            yield item

        next_url = response.css('div.paginator span.next a::attr(href)').extract()
        if next_url:          
            next_url = "https://movie.douban.com/top250" + next_url[0] 
            print(next_url)
            yield scrapy.Request(next_url, headers=self.headers)





