import scrapy

from atro.items import AtroItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class AtroSpider(scrapy.Spider):
    name = "atrobot"
    allowed_domains = ["ncbi.nlm.nih.gov/pubmed?term=als"]
    #["oulu.fi/yliopisto/"]
    
    start_urls = [
    "http://www.ncbi.nlm.nih.gov/pubmed?term=als"
        #"http://www.oulu.fi/yliopisto/"
    ]

    rules = (
        Rule(SgmlLinkExtractor( 
            #restrict_xpaths=('//div[@class="active page_link next"]/a',)), follow=True),  
            #restrict_xpaths=('//a[@id="EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Entrez_Pager.Page"]/@href')), follow=True), 
        restrict_xpaths=('//a[@title="Next page of results"]/a/@href',)), follow= True),
        )
#response.xpath("//a[@id='pnnext']/@href")

    def parse(self, response):
        #filename = response.url.split("/")[-2]
        filename = "atro9.txt"
        titles = response.xpath('//div[@class="rslt"]/p//text()').extract()
        #titles = response.xpath('//div[@class="item-list"]//text()').extract()
        with open(filename, 'a') as f:
            for t in titles:
                f.write(t.encode("utf8"))
                f.write('\n')
            #f.writelines(titles)
            #print titles
    