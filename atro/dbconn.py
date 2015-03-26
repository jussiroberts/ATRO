 #######################################
# A class for implementing database I/O #
 #######################################
 
import psycopg2

class Dbconn():
    @staticmethod
    def insert_publication(title, date_crawled, year_of_publication, doi, abstract, journal, publication_rank, author_list, keyword_list, found_searchwords):
    
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
            print "Title error in dbconn"
        		
		#author
        try:
            for a in author_list:
                cur.execute("INSERT INTO author (name) SELECT %s WHERE NOT EXISTS (SELECT name FROM author WHERE name = %s);", (a,a))
                cur.execute("INSERT INTO author_publication (author_id, pub_id) SELECT author_id, pub_id FROM author, publication WHERE author.name = (%s) AND publication.title = (%s);", (a, title))
                conn.commit()
        except: 
            print "Author error in dbconn"

                
		#abstract
        try:
            cur.execute("UPDATE publication SET abstract = %s WHERE title = %s;", (abstract, title))
            conn.commit()
        except:
            print "Abstract error in dbconn"

		#Publication rank
        try:
            cur.execute("UPDATE publication SET publicationrank = %s WHERE title = %s;", (publication_rank, title))
            conn.commit()
        except:
            print "Publication rank error in dbconn"
        
        
        try:
            cur.execute("UPDATE publication SET journal = %s WHERE title = %s;", (journal, title))
            conn.commit()
        except:
            print "Journal error in dbconn"

        try:
            for k in keyword_list:
                cur.execute("INSERT INTO keyword (keyword) values (%s);", (k,))
                conn.commit()
        except: 
            print "Keyword error in dbconn"
        #doi
        try:
            cur.execute("UPDATE publication SET doi = %s WHERE title = %s;", (doi, title))
            conn.commit()
        except:
            print "DOI error in dbconn"

        #datecrawled
        try:
            cur.execute("UPDATE publication SET datecrawled = %s WHERE title = %s;", (date_crawled, title))
            conn.commit()
        except: 
            print "Datecrawled error in dbconn"

        #yearofpublication
        try:
            cur.execute("UPDATE publication SET yearofpublication = %s WHERE title = %s;", (year_of_publication, title))
            conn.commit()
        except:
            print "Yearofpublication error in dbconn"

        #found_searchwords
        try:
            for found in found_searchwords:
                cur.execute("INSERT INTO searchword_publication (searchword_id, pub_id) SELECT searchword_id, pub_id FROM searchwords, publication WHERE searchwords.searchword = (%s) AND publication.title = (%s);", (found, title))
                conn.commit()
        except Exception, e:
            print "Found_searchwords error", e
        cur.close()
        conn.close()
        
    @staticmethod
    def retrieve_searchwords():
    
        searchwords = []

        try:
            conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='helevetti'")
        except:
            print "Failed to establish connection to database"
        
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT searchword FROM searchwords;")
            temp_searchwords = cur.fetchall()
            for s in temp_searchwords:
                searchwords.append(s[0])
                
        except:
            print "Could not retrieve searchwords from database"
        
        cur.close()
        conn.close()
        
        return searchwords
        
    @staticmethod
    def check_visited_urls(searcht, url):
    
        try:
            conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='helevetti'")
        except:
            print "Failed to establish connection to database"
            
        cur = conn.cursor()
        
        #Check if current URL already exists and save it to the database accordingly. Yield 'item' if successful.
        try:
            cur.execute("SELECT EXISTS(SELECT * FROM visitedurls WHERE searchterm = %s AND url = %s);", (searcht, url))
            urlexists = cur.fetchone()[0]
            
            if urlexists == False:
                cur.execute("INSERT INTO visitedurls (searchterm, url) VALUES (%s, %s);", (searcht, url))
                conn.commit()
                success = 1
                print "URL has not been visited"
                
            else:
                success = 0
                print "URL has been previously visited"

        except:
            print "could not retrieve searchwords from database"
            
        cur.close()
        conn.close()
        
        return success

    @staticmethod
    def insert_searchwords():
        try:
            conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='helevetti'")
        except:
            print "Failed to establish connection to database"

        cur = conn.cursor()

        
        with open("searchwords_list.txt", "r") as wordinput, open('inserted_searchwords.txt', 'a') as wordoutput:
            for line in wordinput:
                line = line.strip()
                try:
                    #cur.execute("INSERT INTO searchwords (searchword) VALUES (%s);", (line,))
                    cur.execute("INSERT INTO searchwords (searchword) SELECT %s WHERE NOT EXISTS (SELECT searchword FROM searchwords WHERE searchword = %s);", (line,line))
                    conn.commit()
                except Exception, e:
                    wordoutput.write(str(e))
                wordoutput.write(line+'\n')
      
        cur.close()
        conn.close()
