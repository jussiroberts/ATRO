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
        found_searchwords = []
        #Remove the dot in the end of the title
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

        #Get the year of publication, doi and journal info
        for p in item['otherinfo']:
            try:    
                otherinfostr = str(p.encode('utf8'))
                
                otherinfolist = otherinfostr.split(" ")
                
                otherinfolist2 = otherinfostr.split(".")

                year_of_publication = otherinfolist2[1][:5]

            
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
         


        #Append abstract groups together
        ab = ''
        try:
            for b in item['abstract']:
                
                ab += str(b.encode('utf8'))+' '
         
            abstract = ab[:-1].strip()
        except:
            abstract = "ERROR"
            print "abstract error"

        #Search for relevant keywords in the abstract
        try:
            publication_rank, found_searchwords = w1.check(abstract)
                
        except Exception, e:
            publication_rank = 999
            print "error in publication rank"
            print str(e)
       

       
        
        try:
            for k in item['keywords']:
                keywordstr = str(k.encode('utf8'))
                
                keyword_list = keywordstr.split("; ")
                   
                for key in keyword_list:
                    keyword_list.append(key)
                  
        except:
               print "no keywords"
            
        date_crawled = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        #If any searchwords were found in the abstract, insert the publication to the database
        if publication_rank > 0:
            db.insert_publication(title, date_crawled, year_of_publication, doi, abstract, journal, publication_rank, author_list, keyword_list, found_searchwords)
        
        return item
