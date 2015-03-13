import scrapy

from atro.items import AtroItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.selector import Selector
from scrapy.http     import Request
#from pyvirtualdisplay import Display #only needed on the RaspberryPi
import lxml.html
from lxml import etree
import time

#e.g >>> start_urls = ['http://www.a.com/%d_%d_%d' %(n,n+1,n+2) for n in range(0, 26)]

class AtroSpider(scrapy.Spider):
    name = "atrobot"
    allowed_domains = ["www.ncbi.nlm.nih.gov"]
    
   

    def __init__(self, searchterm=None, *args, **kwargs):
        super(AtroSpider, self).__init__(*args, **kwargs)
        print kwargs

        self.start_urls = [
        'http://www.ncbi.nlm.nih.gov/m/pubmed/?term=aa*[Author]&page=%d' %(n) for n in range(1, 2079)
        #'http://www.ncbi.nlm.nih.gov/m/pubmed/?term=aa[Author]'
        ]

    def parse(self, response):
        base_url = 'http://www.ncbi.nlm.nih.gov/m/pubmed'
        hrefs = []
        parsedhrefs = []
        hxs = Selector(response) 
        links = hxs.xpath('//*[@class="d"]//li/a/@href').extract()
        hrefs.extend(links)
        for link in hrefs:
            if link.startswith('.'):
                link = link[1:]
                parsedhrefs.append(link)
            with open('parsedURLS.txt', 'a') as f:
                f.write(link+'\n')
        
       


        for link in parsedhrefs:
            url = base_url + link

            yield Request(url, self.parse_publication)
        
        #---PARSE METADATA TO DB---
    def parse_publication(self, response):
        status = response.status
        url = response.url



        if status == 200:
            hxs = Selector(response)
            item = AtroItem()
            item['title'] = hxs.xpath('//div[@class="a"]/h2/text()').extract()
            item['author'] = hxs.xpath('//div[@class="auths"]/a/text()').extract()
            item['journal'] = hxs.xpath('//div[@class="cit"]/a/@title').extract()
            item['otherinfo'] = hxs.xpath('//div[@class="cit"]/text()').extract()


            item['abstract'] = hxs.xpath('//div[@class="ab"]/p/text()').extract()

            #item['abstract'] = hxs.xpath('//div[@class="abstr"]/text()').extract()
            #item['abstract'] = hxs.xpath('//div[@class="abstr"]//text()').extract()
            #copyright info
            #item['abstract'] = str(hxs.xpath('//div[@class="abstr"]/div[1]/p/text()').extract())

            item['keywords'] = hxs.xpath('//div[@class="keywords"]/p/text()').extract()
            yield item

        else:
            with open('fails.txt', 'a') as f:
                f.write('fail\n')
            yield Request(url, self.parse_publication)

