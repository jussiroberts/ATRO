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
    def process_item(self, item, spider):
        db = Dbconn()
        w1 = Wordcheck()
        publication_rank = 0
        doi = "NULL"
        date_crawled = "NULL"
        author_list = []
        keyword_list = []
        journal = "NULL"
        title = "NULL"
        for t in item['title']:   
            try:
                if t.endswith('.'):
                    t = t[:-1]
                    title = t
                else:
                    title = t
            except:
                print "title error"
                        
        for a in item['author']:
            if a not in author_list:
                try:
                    author_list.append(a)
                except:
                    print "author error"

           
        for p in item['otherinfo']:
            try:    
                otherinfostr = str(p.encode('utf8'))
                
                otherinfolist = otherinfostr.split(" ")
                
                otherinfolist2 = otherinfostr.split(".")

                year_of_publication = otherinfolist2[1][:5]
            #year_of_publication = year_of_publication[:] 
            #publication_year_list = otherinfolist2[1].split(' ')
            #year_of_publication = publication_year_list[1]
            
                journal = otherinfolist2[0]
            except:
                print "otherinfo error"
               
            try:    
                
                index = otherinfolist.index('doi:') + 1
              
                if otherinfolist[index].endswith('.'):
                    doi = otherinfolist[index][:-1]
                    
                else:
                    doi = otherinfolist[index]
                
            except:
                print "no DOI"
         


            
        ab = ''
        try:
            for b in item['abstract']:
                
                ab += str(b.encode('utf8'))+' '
         
            abstract = ab[:-1]
        except:
            abstract = "ERROR"
            print "abstract error"
        try:
            publication_rank = w1.check(ab)
                
        except:
            publication_rank = 999
            print "error in publication rank"
       

       
           
        try:
            for k in item['keywords']:
                keywordstr = str(k.encode('utf8'))
                
                keyword_list = keywordstr.split("; ")
                   
                for key in keyword_list:
                    keyword_list.append(key)
                  
        except:
               print "no keywords"
            
        date_crawled = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if publication_rank > 0:
            db.insert_publication(title, date_crawled, year_of_publication, doi, abstract, journal, publication_rank, author_list, keyword_list)
        
        return item
