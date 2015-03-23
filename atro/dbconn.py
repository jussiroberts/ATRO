import psycopg2


class Dbconn():
    @staticmethod
    def insert_publication(title, datecrawled, yearofpublication, doi, abstract, journal, publicationrank, authorlist, keywordlist):
    
        try:
            conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='helevetti'")
        except:
            print "Failed to establish connection to database."
        cur = conn.cursor()
       
        try:
            cur.execute("INSERT INTO publication (title) SELECT %s WHERE NOT EXISTS (SELECT title FROM publication WHERE title = %s);", (title,title))
            conn.commit()
        except:
            print "nothing"
        		
        for a in authorlist: #AUTHOR
            #cur.execute("INSERT INTO author (name) VALUES (%s);", (a,))
            cur.execute("INSERT INTO author (name) SELECT %s WHERE NOT EXISTS (SELECT name FROM author WHERE name = %s);", (a,a))
            cur.execute("INSERT INTO author_publication (author_id, pub_id) SELECT author_id, pub_id FROM author, publication WHERE author.name = (%s) AND publication.title = (%s);", (a, title))
            conn.commit()
        
        cur.execute("UPDATE publication SET abstract = %s WHERE title = %s;", (abstract, title))
        conn.commit()

        cur.execute("UPDATE publication SET publicationrank = %s WHERE title = %s;", (publicationrank, title))
        conn.commit()

       
        cur.execute("INSERT INTO publication (journal) SELECT %s WHERE NOT EXISTS (SELECT title FROM publication WHERE journal = %s);", (journal,journal))
        conn.commit()
        for k in keywordlist:
            cur.execute("INSERT INTO keyword (keyword) values (%s);", (k,))
            conn.commit()
        cur.close()
        conn.close()
    
