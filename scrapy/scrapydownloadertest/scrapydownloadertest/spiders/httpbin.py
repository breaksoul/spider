import scrapy


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/get']#get获取页面的请求

    def parse(self, response):
        self.logger.debug(response.text)#日志信息
