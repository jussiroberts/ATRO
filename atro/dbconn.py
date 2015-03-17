import psycopg2

class Dbconn():

    def insert_publication(title, author, abstract, journal):
    
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
