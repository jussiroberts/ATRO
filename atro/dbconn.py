import psycopg2

class Dbconn(object):

    def insert_publication(self, item, spider):
    
        try:
            conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='helevetti'")
        except:
            print "Failed to establish connection to database."
        cur = conn.cursor()
        for t in item['title']: #TITLE
            if t.endswith('.'):
                t = t[:-1]
                try:
                    cur.execute("INSERT INTO publication (title) SELECT %s WHERE NOT EXISTS (SELECT title FROM publication WHERE title = %s);", (t,t))
                    conn.commit()
                except:
                    fb.write('No title available\n')
            else:   
                cur.execute("INSERT INTO publication (title) SELECT %s WHERE NOT EXISTS (SELECT title FROM publication WHERE title = %s);", (t,t))
                conn.commit()
				
        for a in item['author']: #AUTHOR
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
        for j in item ['journal']:
            cur.execute("INSERT INTO publication (journal) SELECT %s WHERE NOT EXISTS (SELECT title FROM publication WHERE journal = %s);", (j,j))
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
    return item
