 #######################################
# A class for implementing database I/O #
 #######################################
 
import psycopg2

class Dbconn():

    #Insert publication metadata to database
    @staticmethod
    def insert_publication(metadata):

        try:
            conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='<atro>'")
        except:
            print "Failed to establish connection to database."
        cur = conn.cursor()
        #title
        try: 
            cur.execute("INSERT INTO publication (title) SELECT %s WHERE NOT EXISTS (SELECT title FROM publication WHERE title = %s);", (metadata['title'], metadata['title']))
            conn.commit()
        except:
            print "Title error in dbconn"
        		
		#authors
        try:
            for a in metadata['author_list']:
                cur.execute("INSERT INTO author (name) SELECT %s WHERE NOT EXISTS (SELECT name FROM author WHERE name = %s);", (a,a))
                cur.execute("INSERT INTO author_publication (author_id, pub_id) SELECT author_id, pub_id FROM author, publication WHERE author.name = (%s) AND publication.title = (%s);", (a, metadata['title']))
                conn.commit()
        except: 
            print "Author error in dbconn"

                
		#abstract
        try:
            cur.execute("UPDATE publication SET abstract = %s WHERE title = %s;", (metadata['abstract'], metadata['title']))
            conn.commit()
        except:
            print "Abstract error in dbconn"

		#Publication rank
        try:
            cur.execute("UPDATE publication SET publicationrank = %s WHERE title = %s;", (metadata['publication_rank'], metadata['title']))
            conn.commit()
        except:
            print "Publication rank error in dbconn"
        
        #journal
        try:
            cur.execute("UPDATE publication SET journal = %s WHERE title = %s;", (metadata['journal'], metadata['title']))
            conn.commit()
        except:
            print "Journal error in dbconn"

        #doi
        try:
            cur.execute("UPDATE publication SET doi = %s WHERE title = %s;", (metadata['doi'], metadata['title']))
            conn.commit()
        except:
            print "DOI error in dbconn"

        #pii
        try:
            cur.execute("UPDATE publication SET pii = %s WHERE title = %s;", (metadata['pii'], metadata['title']))
            conn.commit()
        except:
            print "PII error in dbconn"

        #datecrawled
        try:
            cur.execute("UPDATE publication SET datecrawled = %s WHERE title = %s;", (metadata['date_crawled'], metadata['title']))
            conn.commit()
        except: 
            print "Datecrawled error in dbconn"

        #yearofpublication
        try:
            cur.execute("UPDATE publication SET yearofpublication = %s WHERE title = %s;", (metadata['year_of_publication'], metadata['title']))
            conn.commit()
        except:
            print "Yearofpublication error in dbconn"

        #found searchwords
        try:
            for found in metadata['found_searchwords']:
                cur.execute("INSERT INTO searchword_publication (searchword_id, pub_id) SELECT searchword_id, pub_id FROM searchwords, publication WHERE searchwords.searchword = (%s) AND publication.title = (%s);", (found, metadata['title']))
                conn.commit()
        except Exception, e:
            print "Found_searchwords error", e
        cur.close()
        conn.close()
        

    #Get searchwords from database
    @staticmethod
    def retrieve_searchwords():
    
        searchwords = []

        try:
            conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='<atro>'")
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
        
    #Check already visited URLs
    @staticmethod
    def check_visited_urls(searchtermi, url):
    
        try:
            conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='<atro>'")
        except:
            print "Failed to establish connection to database"
            
        cur = conn.cursor()
        
        #Check if current URL already exists and save it to the database accordingly. Yield 'item' if successful.
        try:
            cur.execute("SELECT EXISTS(SELECT * FROM visitedurls WHERE searchterm = %s AND url = %s);", (searchtermi, url))
            urlexists = cur.fetchone()[0]
            
            if urlexists == False:
                cur.execute("INSERT INTO visitedurls (searchterm, url) VALUES (%s, %s);", (searchtermi, url))
                conn.commit()
                success = 1  
            else:
                success = 0
        except:
            print "could not retrieve searchwords from database"
            
        cur.close()
        conn.close()
        
        return success

    #Insert searchwords to database from a textfile
    @staticmethod
    def insert_searchwords():
        try:
            conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='<atro>'")
        except:
            print "Failed to establish connection to database"

        cur = conn.cursor()

        
        with open("searchwords_list.txt", "r") as wordinput, open('../inserted_searchwords.txt', 'a') as wordoutput:
            for line in wordinput:
                line = line.strip()
                line = line.lower()
                try:
                    #cur.execute("INSERT INTO searchwords (searchword) VALUES (%s);", (line,))
                    cur.execute("INSERT INTO searchwords (searchword) SELECT %s WHERE NOT EXISTS (SELECT searchword FROM searchwords WHERE searchword = %s);", (line,line))
                    conn.commit()
                except Exception, e:
                    wordoutput.write(str(e))
                wordoutput.write(line+'\n')
      
        cur.close()
        conn.close()
