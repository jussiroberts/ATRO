import scrapy

from atro.items import AtroItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.selector import Selector
from scrapy.http     import Request
from selenium import webdriver
from pyvirtualdisplay import Display #only needed on the RaspberryPi
import lxml.html
from lxml import etree
import time
import psycopg2

class AtroSpider(scrapy.Spider):
    name = "atrobot"
    allowed_domains = ["www.ncbi.nlm.nih.gov"]
    
    start_urls = [
    "http://www.ncbi.nlm.nih.gov/pubmed?term=als"
    
    ]

    extractor = SgmlLinkExtractor()

    def __init__(self, **kwargs):
        print kwargs
        display = Display(visible=0, size=(800, 600)) #only needed on the RaspberryPi
        display.start() #only needed on the RaspberryPi
        self.driver = webdriver.Firefox()

    #def __del__(self):
        #self.driver.dispose()

    def parse(self, response):
        base_url = 'http://www.ncbi.nlm.nih.gov'
        wdr = self.driver
        wdr.get(response.url)

        #---PUBMED PAGE SETTINGS--- 
        #Sets the amount of results per page to 5 (for testing purposes), 'ps200' for 200 per page     

        dsettings = wdr.find_element_by_link_text('20 per page')
        dsettings.click()
        pagesetting = wdr.find_element_by_id('ps5')
        pagesetting.click()
        wdr.implicitly_wait(1)
        
        #---GET PUBLICATION LINKS, NUMBER OF PAGES AND CURRENT PAGE FOR THE FIRST PAGE---
        html = wdr.page_source
        root = lxml.html.fromstring(html)
        #links = root.xpath('//*[@class="title"]/a/@href')
        #pages = root.xpath('//*[@class="num"]/@last')[0]
        current = root.xpath('//*[@class="num"]/@value')[0]

        #---CREATE AN ARRAY FOR THE LINKS---#
        hrefs = []

        hxs = Selector(response) #
        links = hxs.xpath('//*[@class="title"]/a/@href').extract() #
        hrefs.extend(links)
        pages = hxs.xpath('//*[@class="num"]/@last').extract()[0] #

        #count = 0
        print ("Current page: {0}, Pages total: {1}".format(current, pages))
        print ("{} publication URLs saved".format(len(hrefs)))
#int(pages)

        #---LOOP THROUGH THE RESULT PAGES, GETTING THE LINKS OF THE PUBLICATIONS---
        #---CRAWLS ONLY TWO RESULT PAGES FOR NOW---
        
        while int(current) < 2:
            #count = count + 1
     

            #---GO TO THE NEXT PAGE AND GET ALL THE PUBLICATION LINKS FROM THERE
            try:
                next = wdr.find_element_by_link_text('Next >')
                next.click()
                wdr.implicitly_wait(0.5)
                html = wdr.page_source
                root = lxml.html.fromstring(html)
                links = root.xpath('//*[@class="title"]/a/@href')
                current = root.xpath('//*[@class="num"]/@value')[0]
                hrefs.extend(links)
                print '....\n'
                print ("Current page: {0}, Pages total: {1}".format(current, pages))
                print ("{} publication URLs saved".format(len(hrefs)))


            except Exception as ex:
                print ex

        for href in hrefs:
            url = base_url + href
            yield Request(url, self.parse_publication)
            time.sleep(0.5)

        wdr.quit()

        #---PARSE METADATA TO DB---
    def parse_publication(self, response):
        status = response.status
        url = response.url

        if status == 200:
            hxs = Selector(response)
            item = AtroItem()
            item['title'] = hxs.xpath('//div[@class="rprt abstract"]/h1/text()').extract()
            item['author'] = hxs.xpath('//div[@class="auths"]/a/text()').extract()
            yield item

        else:
            yield Request(url, self.parse_publication)

       


     
   
    
