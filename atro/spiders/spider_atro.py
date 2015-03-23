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
import re
import math
import os
#e.g >>> start_urls = ['http://www.a.com/%d_%d_%d' %(n,n+1,n+2) for n in range(0, 26)]

class AtroSpider(scrapy.Spider):
    name = "atrobot"
    allowed_domains = ["www.ncbi.nlm.nih.gov"]
    #rules = (
       
    #    Rule(SgmlLinkExtractor(allow=[r'.*',], restrict_xpaths=('//div[@class="pag"]/a/@href')), follow=True),
    #)
    
    def start_requests(self):
        alphabet = 'a'
        fname = 'latesturl.txt'

    #Check last crawled URL from text-file and make it the starting url
        if os.path.isfile(fname):
            f = open('latesturl.txt', 'r')
            lasturl = f.readline()
            lastsearchterm = re.search('term=(.*)5BAuthor', lasturl)
            lastsearchterm = lastsearchterm.group(1)
            lastsearchterm = lastsearchterm[:-1]

            if 'page=' in lasturl:
                lastpage = str(lasturl.index('page=') + 1)
            #    with open('latesturl.txt', 'a') as f:
            #        f.write(lastsearchterm+lastpage)
            else:
                lastpage = str(1)

            tempsearchterm = 'b'
            alphabetlocater = alphabet.index(tempsearchterm) + 1
            newalphabet = alphabet[alphabetlocater:]
    #      with open('newalphalist.txt', 'a') as f:
    #          f.write(lastpage)

    #TODO: check if first crawl during runtime and crawl with 'lastsearchterm' + 'lastpage'
    #    if firstcrawl == True:
    #       searchterm = "http://www.ncbi.nlm.nih.gov/m/pubmed?term="+lastsearchterm+'[Author]&page='+lastpage
    #       firstcrawl = False
    #       yield Request(searchterm, self.parse)

    #TODO: only move to next for-loop once previous is finished. 
    #      use 'newalphabet' instead of 'alphabet' if previous crawls exist.
        for alpha in alphabet:
            searchterm = alpha
            searchterm = "http://www.ncbi.nlm.nih.gov/m/pubmed?term="+alpha+'[Author]&page=1'
            yield Request(searchterm, self.parse)
            time.sleep(0.5)

        for alpha in alphabet:
            for beta in alphabet:
                searchterm = alpha+beta
                searchterm = "http://www.ncbi.nlm.nih.gov/m/pubmed?term="+alpha+beta+'[Author]&page=1'
                yield Request(searchterm, self.parse)
                time.sleep(0.5)

        for alpha in alphabet:
            for beta in alphabet:
                for gamma in alphabet:
                    searchterm = alpha+beta+gamma
                    searchterm = "http://www.ncbi.nlm.nih.gov/m/pubmed?term="+alpha+beta+gamma+'*[Author]&page=1'
                    yield Request(searchterm, self.parse)
                    time.sleep(0.5)

    def __init__(self, searchterm=None, *args, **kwargs):
        super(AtroSpider, self).__init__(*args, **kwargs)
        print kwargs

        #self.start_urls = [
        #'http://www.ncbi.nlm.nih.gov/m/pubmed/?term=aa*[Author]&page=%d' %(n) for n in range(1, 2)
        #'http://www.ncbi.nlm.nih.gov/m/pubmed/?term=aa[Author]&page=10'
        #]
      
    #def get_next_page(self, response):
    #    pages = hxs.xpath('//div[@class="h"]/h2/text()').extract()
    #    numbers = int(re.search(r'\d+', pages[0]).group())
    #    intpages = str(int(math.ceil(float(numbers)/10)))
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

            with open('latesturl.txt', 'w') as f:
                f.write(response.url)

        with open('pages.txt', 'a') as f:  
             
            pages = hxs.xpath('//div[@class="h"]/h2/text()').extract()
            
            numbers = int(re.search(r'\d+', pages[0]).group())
            intpages = str(int(math.ceil(float(numbers)/10)))
            #f.write(intpages+'\n')

            #currentpage[1] = current page
            current = hxs.xpath('normalize-space(//div[@class="pag"]/span/text())').extract()
            currentpage = current[0].split(" ")
            f.write("Current page:")
            f.write(currentpage[1].encode('utf-8')+'\n')
            nextpage = str(int(currentpage[1])+1)

            #f.write(nextpage+'\n')

            searcht = hxs.xpath('//div[@class="h"]/input/@value').extract()
            currentsearchterm = searcht[0]
            f.write("Current searchterm:")
            f.write(currentsearchterm+'\n')  
            f.write("...\n")
            #f.write('Value= {}'.format(searcht[0]))
            #for c in current:
                #f.write(c.encode('utf-8')+'\n')
        #intpages = int(re.match(r'\d+', pages).group())
        #print intpages

        for link in parsedhrefs:
            url = base_url + link

            yield Request(url, self.parse_publication)

        #next_url = self.get_next_url()
        #if next_url:
        #    yield Request(next_url, self.parse, dont_filter=True)
        if int(currentpage[1])<int(intpages):
            next_url = base_url+'/?term='+currentsearchterm+'&page='+nextpage

        #next_url = base_url+'&page='+nextpage
            yield Request(next_url, self.parse)
        #---PARSE METADATA TO DB---
    def parse_publication(self, response):
        status = response.status
        url = response.url

        if status == 200:
            hxs = Selector(response)
            item = AtroItem()
            item['title'] = hxs.xpath('//div[@class="a"]/h2/text()').extract()
            item['author'] = hxs.xpath('//div[@class="auths"]/a/text()').extract()
            #item['journal'] = hxs.xpath('//div[@class="cit"]/a/@title').extract()
            item['otherinfo'] = hxs.xpath('normalize-space(//div[@class="meta"]/p/text())').extract()
            item['abstract'] = hxs.xpath('//div[@class="ab"]/p//text()').extract()
            
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

