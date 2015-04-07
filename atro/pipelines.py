# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import psycopg2
from datetime import datetime
from datetime import time
from wordcheck import Wordcheck
from dbconn import Dbconn


#The pipeline processes all items that are yielded by the spider. Each item contains relevant metadata for one publication.
class AtroPipeline(object):

    def process_title(self, title):
        #Remove the dot in the end of the title   
        try:
            if title.endswith('.'):
                title = title[:-1]
        except:
            print "title error"
        return title

    def process_otherinfo(self, otherinfo):
        #Get the year of publication, doi, pii and journal info
        doi = "NULL"
        pii = "NULL"
        year_of_publication = "NULL"
        journal = "NULL"
        try:    
            otherinfolist = otherinfo.split(" ")
            otherinfolist2 = otherinfo.split(".")
            year_of_publication = otherinfolist2[1][:5]
            year_of_publication = year_of_publication[1:]
            journal = otherinfolist2[0]
        except:
            print "otherinfo error"
           
        #Check whether the publication has a doi or not
        try:      
            index = otherinfolist.index('doi:') + 1
            if otherinfolist[index].endswith('.'):
                doi = otherinfolist[index][:-1]   
            else:
                doi = otherinfolist[index]  
        except:
            print "no DOI"

        #Check whether the publication has a pii or not
        try:
            index = otherinfolist.index('pii:') + 1
            if otherinfolist[index].endswith('.'):
                pii = otherinfolist[index][:-1]
            elif otherinfolist[index].endswith('doi:'):
                pii = otherinfolist[index][:-1]
            else:
                pii = otherinfolist[index]
        except:
            print "no PII"

        return year_of_publication, journal, doi, pii
        
        
    def process_abstract(self, abstractlist): 
        #Append abstract groups together
        ab = ''
        try:
            for b in abstractlist:       
                ab += str(b.encode('utf8'))+' ' 
            abstract = ab[:-1].strip()
        except:
            abstract = "ERROR"
            print "abstract error"
        return abstract

    def process_item(self, item, spider):
        db = Dbconn()
        w1 = Wordcheck()
        publication_rank = 0
        date_crawled = "NULL"
        author_list = []
        title = "NULL"
        found_searchwords = []

        title = self.process_title(item['title'][0])
        abstract = self.process_abstract(item['abstract'])
        year_of_publication, journal, doi, pii = self.process_otherinfo(item['otherinfo'][0])
          #Search for relevant keywords in the abstract
        try:

            publication_rank, found_searchwords = w1.check(abstract)        
        except Exception, e:
            publication_rank = 999
            print "error in publication rank"
            print str(e)
            
        date_crawled = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        metadata = dict(title = title, date_crawled = date_crawled, year_of_publication = year_of_publication, doi = doi, pii = pii, abstract = abstract, journal = journal, publication_rank = publication_rank, author_list = item['author'], found_searchwords = found_searchwords)
        
        #If any searchwords were found in the abstract, insert the publication to the database
        if publication_rank > 0:
            db.insert_publication(metadata)
        return item

    

      
