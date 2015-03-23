# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import psycopg2
from datetime import datetime
from wordcheck import Wordcheck
from dbconn import Dbconn

#The pipeline processes all items that are yielded by the spider. Each item contains relevant metadata for one publication.
class AtroPipeline(object):
    def process_item(self, item, spider):
        db = Dbconn()
        w1 = Wordcheck()
        publication_rank = 0
        doi = 0
        datecrawled = 0
        authorlist = []
        keywordlist = []
        journal = "null"
        title = "null"
        for t in item['title']:   
            if t.endswith('.'):
                t = t[:-1]
                title = t
                        
        for a in item['author']:
           authorlist.append(a)

           
        for p in item['otherinfo']:
                
            otherinfostr = str(p.encode('utf8'))
                
            otherinfolist = otherinfostr.split(" ")
                
            otherinfolist2 = otherinfostr.split(".")
                 
            publicationyearlist = otherinfolist2[1].split(' ')
            yearofpublication = publicationyearlist[1]
               
               
            try:    
                
                index = otherinfolist.index('doi:') + 1
              
                if otherinfolist[index].endswith('.'):
                    doi = otherinfolist[index][:-1]
                    
                else:
                    doi = otherinfolist[index]
                journal = otherinfolist2[0]
            except:
                print "nothing"
         


            
        ab = ''
        for b in item['abstract']:
                
            ab += str(b.encode('utf8'))+' '
         
        ab = ab[:-1]
        try:
            publication_rank = w1.check(ab)
                
        except:
            print "nothing"
       

        try:
            abstract = ab
        except:
            print "nothing"
           
        try:
            for k in item['keywords']:
                keywordstr = str(k.encode('utf8'))
                
                keywordlist = keywordstr.split("; ")
                   
                for key in keywordlist:
                    keywordlist.append(key)
                  
        except:
               print "nothing"
            
        datecrawled = str(datetime.now())
         

        db.insert_publication(title, datecrawled, yearofpublication, doi, abstract, journal, publication_rank, authorlist, keywordlist)
        
        return item
