# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2

class AtroPipeline(object):
    def process_item(self, item, spider):
    	#with open('items', 'a') as f:
    		#f.write('title: {0}, author: {1}\n'.format(item['title'], item['author']))
    	try:
            conn = psycopg2.connect("dbname='jonitestdb' user='jussi' host='localhost' password='helevetti'")
        except:
            print "Failed to establish connection to database."
        cur = conn.cursor()

        for t in item['title']:
            #cur.execute("INSERT INTO publication (name) VALUES (%s);", (item['title'],))
            cur.execute("INSERT INTO publication (name) VALUES (%s);", (t,))
            conn.commit()
                #SELECT ID???

        for a in item['author']:
        #cur.execute("INSERT INTO author (name) VALUES (%s);", (item['author'],))
            cur.execute("INSERT INTO author (name) VALUES (%s);", (a,))
            #conn.commit()
                #cur.execute("INSERT INTO author_publication (author_id, pub_id) VALUES (%s, %s);", ())
            cur.execute("INSERT INTO author_publication (author_id, pub_id) SELECT author_id, pub_id FROM author, publication WHERE author.name = (%s) AND publication.name = (%s);", (a, t)
            conn.commit()
            #for j in journal:
             #   cur.execute("UPDATE testpublication SET journal = %s WHERE otsikko = %s;", (j, o)) 
              #  conn.commit()
            #for a in abstract:
             #   cur.execute("UPDATE testpublication SET abstract = %s WHERE otsikko = %s;", (a, o))
              #  conn.commit()

        cur.close()
        conn.close()	
        return item
