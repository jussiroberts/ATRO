import scrapy

from atro.items import AtroItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.selector import Selector
from scrapy.http     import Request
from selenium import webdriver
from pyvirtualdisplay import Display#only needed on the RaspberryPi
import lxml.html
from lxml import etree
from selenium.webdriver.common.by import By
import time
import psycopg2

#jonitest
#testcomment
#jokujuttunen
class AtroSpider(scrapy.Spider):
    name = "atrobot"
    allowed_domains = ["www.ncbi.nlm.nih.gov"]
    
    start_urls = [
    "http://www.ncbi.nlm.nih.gov/pubmed?term=als"
    ]

    extractor = SgmlLinkExtractor()

    def __init__(self, **kwargs):
        print kwargs
        display = Display(visible=0, size=(800, 600))#only needed on the RaspberryPi
        display.start()#only needed on the RaspberryPi
        self.driver = webdriver.Firefox()

    def parse(self, response):
        #filename = "atro_urls1.txt"
        
        base_url = 'http://www.ncbi.nlm.nih.gov'

        wdr = self.driver
        wdr.get(response.url)


        #---PUBMED PAGE SETTINGS---            
        #dsettings = wdr.find_element_by_link_text('Display Settings')
        #dsettings.click()
        #wdr.click("link=Display Settings:")
        #wdr.click("id=ps100")
        #wdr.click("//div[@id='display_settings_menu']/fieldset[2]/u1/li[5]/label")
        #wdr.click("name=EntrezSystem2.PEntrez.Pmc.Pmc_ResultsPanel.Pmc_DisplayBar.SetDisplay")
        #wdr.wait_for_page_to_load("30000")

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

        count = 0
        print count, current, pages
        print len(hrefs)
#int(pages)

        #---LOOP THROUGH THE RESULT PAGES, GETTING THE LINKS OF THE PUBLICATIONS---
        #---CRAWLS ONLY TWO RESULT PAGES FOR NOW---
        while int(current) < 2:
            count = count + 1
            print '....\n'
            print count, current, pages

            #---GO TO THE NEXT PAGE AND GET ALL THE PUBLICATION LINKS FROM THERE
            try:
                next = wdr.find_element_by_link_text('Next >')
                next.click()
                wdr.implicitly_wait(3)
                html = wdr.page_source
                root = lxml.html.fromstring(html)
                links = root.xpath('//*[@class="title"]/a/@href')
                current = root.xpath('//*[@class="num"]/@value')[0]
                hrefs.extend(links)
                print len(hrefs)

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
        #filename = "atro1.txt"

        if status == 200:
            hxs = Selector(response)
            #otsikko = hxs.select('//*[@class="content-title"]/text()').extract()
            otsikko = hxs.xpath('//div[@class="rprt abstract"]/h1/text()').extract()
            author = hxs.xpath('//div[@class="auths"]/a/text()').extract()
            journal = hxs.xpath('//div[@class="cit"]/a/@title').extract()
            abstract = hxs.xpath('//div[@class="abstr"]//p/abstracttext/text()').extract()
			
            try:
                conn = psycopg2.connect("dbname='newdb' user='jussi' host='localhost' password='helevetti'")
            except:
                print "Failed to establish connection to database."
            cur = conn.cursor()

            for o in otsikko:
                SQL = "INSERT INTO testpublication (otsikko, author, journal, abstract) VALUES (%s, %s, %s, %s);"
                data = (o, "1","1","1")
                cur.execute(SQL, data)
                conn.commit()
            #for a in author:
            cur.execute("UPDATE testpublication SET author = %s WHERE otsikko = %s;", (author, o))
            conn.commit()
            for j in journal:
                cur.execute("UPDATE testpublication SET journal = %s WHERE otsikko = %s;", (j, o)) 
                conn.commit()
            for a in abstract:
                cur.execute("UPDATE testpublication SET abstract = %s WHERE otsikko = %s;", (a, o))
                conn.commit()

            cur.close()
            conn.close()

        else:
            yield Request(url, self.parse_publication)


     
   
    
