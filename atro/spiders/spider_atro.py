import scrapy

from atro.items import AtroItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.selector import Selector
from scrapy.http     import Request
from .. dbconn import Dbconn
import lxml.html
from lxml import etree
import time
import re
import math
import os


class AtroSpider(scrapy.Spider):
    name = "atrobot"
    allowed_domains = ["www.ncbi.nlm.nih.gov"]
   
    #Algorithm for crawling PubMed author by author
    def start_requests(self):
        alphabet = 'a'
   
        for alpha in alphabet:
            searchterm = alpha
            searchterm = "http://www.ncbi.nlm.nih.gov/m/pubmed?term="+alpha+'[Author]&page=1'
            yield Request(searchterm, self.parse)

        for alpha in alphabet:
            for beta in alphabet:
                searchterm = alpha+beta
                searchterm = "http://www.ncbi.nlm.nih.gov/m/pubmed?term="+alpha+beta+'[Author]&page=1'
                yield Request(searchterm, self.parse)

        for alpha in alphabet:
            for beta in alphabet:
                for gamma in alphabet:
                    searchterm = alpha+beta+gamma
                    searchterm = "http://www.ncbi.nlm.nih.gov/m/pubmed?term="+alpha+beta+gamma+'[Author]&page=1'
                    yield Request(searchterm, self.parse)
                    
        for alpha in alphabet:
            for beta in alphabet:
                for gamma in alphabet:
                    for delta in alphabet:
                        searchterm = alpha+beta+gamma+delta
                        searchterm = "http://www.ncbi.nlm.nih.gov/m/pubmed?term="+alpha+beta+gamma+delta+'*[Author]&page=1'
                        yield Request(searchterm, self.parse)
                     

    def __init__(self, searchterm=None, *args, **kwargs):
        super(AtroSpider, self).__init__(*args, **kwargs)
        db = Dbconn()
        db.insert_searchwords()
        print kwargs

    def parse(self, response):
        numbers = 0
        counter = 0
        base_url = 'http://www.ncbi.nlm.nih.gov/m/pubmed'
        db = Dbconn()
        hrefs = []
        parsedhrefs = []
        hxs = Selector(response) 
        links = hxs.xpath('//*[@class="d"]//li/a/@href').extract()
        hrefs.extend(links)
        for link in hrefs:
            if link.startswith('.'):
                link = link[1:]
                parsedhrefs.append(link)
 

        
             
        pages = hxs.xpath('//div[@class="h"]/h2/text()').extract()
        numbers = int(re.search(r'\d+', pages[0]).group())
        intpages = str(int(math.ceil(float(numbers)/10)))
        current = hxs.xpath('normalize-space(//div[@class="pag"]/span/text())').extract()
        currentpage = current[0].split(" ")
        nextpage = str(int(currentpage[1])+1)
              
        searcht = hxs.xpath('//div[@class="h"]/input/@value').extract()
        currentsearchterm = searcht[0]
        
        for link in parsedhrefs:
            searchtermi = ""
            url = base_url + link
            urli = str(url)
            searchtermi = re.search('from=(.*)]', urli)
            searchtermi = searchtermi.group(1)
            searchtermi = searchtermi[:-7]

            success = db.check_visited_urls(searchtermi, url)
            
            if success == 1:
                yield Request(url, self.parse_publication)
            
            elif success == 0:
                counter += 1
                print counter
                print "-----------------------------------------------------------------------------"

      
        
        if int(currentpage[1])<int(intpages):
            next_url = base_url+'/?term='+currentsearchterm+'&page='+nextpage
        
            
        
            yield Request(next_url, self.parse)

    #Parse publication metadata
    def parse_publication(self, response):
        status = response.status
        url = response.url

        if status == 200:
            hxs = Selector(response)
            item = AtroItem()
            item['title'] = hxs.xpath('//div[@class="a"]/h2/text()').extract()
            item['author'] = hxs.xpath('//div[@class="auths"]/a/text()').extract()
            item['otherinfo'] = hxs.xpath('normalize-space(//div[@class="meta"]/p/text())').extract()
            item['abstract'] = hxs.xpath('//div[@class="ab"]/p//text()').extract()
            item['keywords'] = hxs.xpath('//div[@class="keywords"]/p/text()').extract()


            yield item

        else:
            yield Request(url, self.parse_publication)

