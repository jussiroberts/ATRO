import psycopg2
#testi

class Dbconn():
    @staticmethod
    def insert_publication(title, date_crawled, year_of_publication, doi, abstract, journal, publication_rank, author_list, keyword_list):
    
        try:
            conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='helevetti'")
        except:
            print "Failed to establish connection to database."
        cur = conn.cursor()
        #title
        try: 
            cur.execute("INSERT INTO publication (title) SELECT %s WHERE NOT EXISTS (SELECT title FROM publication WHERE title = %s);", (title,title))
            conn.commit()
        except:
            print "nothing"
        		
		#author
        for a in author_list:
            cur.execute("INSERT INTO author (name) SELECT %s WHERE NOT EXISTS (SELECT name FROM author WHERE name = %s);", (a,a))
            cur.execute("INSERT INTO author_publication (author_id, pub_id) SELECT author_id, pub_id FROM author, publication WHERE author.name = (%s) AND publication.title = (%s);", (a, title))
            conn.commit()
        
		#abstract
        cur.execute("UPDATE publication SET abstract = %s WHERE title = %s;", (abstract, title))
        conn.commit()
		
		#Publication rank
        cur.execute("UPDATE publication SET publicationrank = %s WHERE title = %s;", (publication_rank, title))
        conn.commit()

        #journal name (ei toimi)
        #cur.execute("INSERT INTO publication (journal) SELECT %s WHERE NOT EXISTS (SELECT title FROM publication WHERE journal = %s);", (journal,journal))
        cur.execute("UPDATE publication SET journal = %s WHERE title = %s;", (journal, title))
        conn.commit()
        for k in keyword_list:
            cur.execute("INSERT INTO keyword (keyword) values (%s);", (k,))
            conn.commit()

        #doi
        cur.execute("UPDATE publication SET doi = %s WHERE title = %s;", (doi, title))
        conn.commit()
		
        #datecrawled
        cur.execute("UPDATE publication SET datecrawled = %s WHERE title = %s;", (date_crawled, title))
        conn.commit()
		
        #datecrawled
        cur.execute("UPDATE publication SET yearofpublication = %s WHERE title = %s;", (year_of_publication, title))
        conn.commit()
		
        cur.close()
        conn.close()