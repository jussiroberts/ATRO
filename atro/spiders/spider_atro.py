import scrapy

from atro.items import AtroItem
from scrapy.selector import Selector
from scrapy.http     import Request
from .. dbconn import Dbconn
import lxml.html
from lxml import etree
import re
import math


class AtroSpider(scrapy.Spider):
    name = "atro"
    allowed_domains = ["www.ncbi.nlm.nih.gov"]
   
    #Algorithm for crawling PubMed author by author
    def start_requests(self):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
 
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
                     
    #Class constructor                    
    def __init__(self, new_searchwords=False, *args, **kwargs):
        super(AtroSpider, self).__init__(*args, **kwargs)
        db = Dbconn()
        if(new_searchwords == "True"):
            db.insert_searchwords()
        print kwargs

    #Function to parse result pages
    def parse(self, response):
        has_pages = 0
        numbers = 0
        counter = 0
        base_url = 'http://www.ncbi.nlm.nih.gov/m/pubmed'
        db = Dbconn()
        hrefs = []
        parsedhrefs = []
        hxs = Selector(response) 

        #Get publication links from the first page
        links = hxs.xpath('//*[@class="d"]//li/a/@href').extract()
        hrefs.extend(links)

        #Clean up the hrefs
        for link in hrefs:
            if link.startswith('.'):
                link = link[1:]
                parsedhrefs.append(link)
 
        #Get the amount of pages for the new version of pubmed mobile (8.4.2015)
        pages = hxs.xpath('normalize-space(//span[@class="light_narrow_text"]/text()[last()])').extract()
        try:
            numbers = int(re.search(r'\d+', pages[0]).group())
        except Exception, e:
            print e
        else: 
        #If there are multiple result pages
            has_pages = 1

        if(has_pages == 1):
            intpages = str(int(math.ceil(float(numbers)/10)))

            #Get the current page number
            current = hxs.xpath('normalize-space(//div[@class="pag"]/span/text())').extract()
            currentpage = current[0].split(" ")

            #Get the next page number
            nextpage = str(int(currentpage[1])+1)
        else:
            currentpage = [1,1]
            nextpage = 1  
            intpages = 1

        #Get the current searchterm
        searcht = hxs.xpath('//div[@class="h"]/input/@value').extract()
        currentsearchterm = searcht[0]
        
        #Construct a full URL from the hrefs and base_url and check whether they have been visited before or not
        for link in parsedhrefs:
            searchtermi = ""
            url = base_url + link
            urli = str(url)
            searchtermi = re.search('from=(.*)]', urli)
            try:
                searchtermi = searchtermi.group(1)
                searchtermi = searchtermi[:-7]
            except Exception, e:
                searchtermi = "null"
                print e

            success = db.check_visited_urls(searchtermi, url)            
            if success == 1:
                yield Request(url, self.parse_publication)
        
        #Check if it's the last page
        if int(currentpage[1])<int(intpages):
            next_url = base_url+'/?term='+currentsearchterm+'&page='+nextpage
            yield Request(next_url, self.parse)

    #Parse publication metadata, create an item for each publication
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
            yield item

        else:
            yield Request(url, self.parse_publication)

