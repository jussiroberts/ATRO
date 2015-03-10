# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
from datetime import datetime

class AtroPipeline(object):
    def process_item(self, item, spider):
        with open('atro1.txt', 'a') as f:
            for t in item['title']: 

                f.write('title: {0}\n'.format(t,))

            for a in item['author']:
                f.write('author: {0}\n'.format(a.encode('utf-8'),))

            for j in item['journal']:
                f.write('journal: {0}\n'.format(j.encode('utf-8'),))

            for p in item['otherinfo']:
                otherinfostr = str(p.encode('utf-8'))
                otherinfolist = otherinfostr.split(" ")
                f.write('publication year: {0}\n'.format(otherinfolist[1],))
                #for info in otherinfolist:
                 #   if info == 'doi:':
                  #      f.write('doi: {0}\n'.format(info,))
                try:    
                    index = otherinfolist.index('doi:') + 1
                    f.write('doi: {0}\n'.format(otherinfolist[index],))
                except:
                    print "No DOI for publication available"
                #f.write('publication year: {0}\n'.format(p.encode('utf-8'),))

            for b in item['abstract']:
                f.write('abstract: {0}\n'.format(b.encode('utf-8'),))

            for k in item['keywords']:
                keywordstr = str(k.encode('utf-8'))
                keywordlist = keywordstr.split("; ")
                 
                for key in keywordlist:
                    f.write('keywords: {0}\n'.format(key,))
            f.write('Date crawled: {0}\n'.format(str(datetime.now()),))
            f.write('...\n')

            """
        try:
            conn = psycopg2.connect("dbname='jonitestdb' user='jussi' host='localhost' password='helevetti'")
        except:
            print "Failed to establish connection to database."
        cur = conn.cursor()

        for t in item['title']:           
            cur.execute("INSERT INTO publication (title) SELECT %s WHERE NOT EXISTS (SELECT title FROM publication WHERE title = %s);", (t,t))
            conn.commit()

        for a in item['author']:
            #cur.execute("INSERT INTO author (name) VALUES (%s);", (a,))
            cur.execute("INSERT INTO author (name) SELECT %s WHERE NOT EXISTS (SELECT name FROM author WHERE name = %s);", (a,a))
            cur.execute("INSERT INTO author_publication (author_id, pub_id) SELECT author_id, pub_id FROM author, publication WHERE author.name = (%s) AND publication.title = (%s);", (a, t))
            conn.commit()

        for b in item['abstract']:
            #ab = str(b.encode('utf8'))
            #words = b.split(" ")
            #print(words[2])
            #cur.execute("UPDATE publication SET abstract = %s WHERE title = %s;", (words, t))
            cur.execute("UPDATE publication SET abstract = %s WHERE title = %s;", (b, t))
            conn.commit()

        #DATE
        #cur.execute("UPDATE publication SET datecrawled = %s WHERE title = %s;", (str(datetime.now()), t))
        #conn.commit()

        for k in item['keywords']:
            keywordstr = str(k.encode('utf-8'))
            keywordlist = keywordstr.split("; ")    
            for key in keywordlist:
                cur.execute("INSERT INTO keyword (keyword) values (%s);", (key,))
                conn.commit()


        cur.close()
        conn.close()
        """
        return item
