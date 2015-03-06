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
            cur.execute("INSERT INTO publication (title) SELECT %s WHERE NOT EXISTS (SELECT title FROM publication WHERE title = %s);", (t,t))
            conn.commit()

        for a in item['author']:
            #cur.execute("INSERT INTO author (name) VALUES (%s);", (a,))
            cur.execute("INSERT INTO author (name) SELECT %s WHERE NOT EXISTS (SELECT name FROM author WHERE name = %s);", (a,a))
            cur.execute("INSERT INTO author_publication (author_id, pub_id) SELECT author_id, pub_id FROM author, publication WHERE author.name = (%s) AND publication.title = (%s);", (a, t))
            conn.commit()

        for b in item['abstract']:
            cur.execute("UPDATE publication SET abstract = %s WHERE title = %s;", (b, t))
            conn.commit()

        cur.close()
        conn.close()
        return item
