 #####################################################################################
#This class implements a mechanism to check if the abstract of an article contains    #
#any words that we might be interested in. It compares the words in the abstract to   #
#the list of words in the searchwords table in the database. The more matching words, #
#the higher the ranking of the article.                                               #
 #####################################################################################

import re
from dbconn import Dbconn

class Wordcheck():
    @staticmethod
    def check(abstract):
        my_regex = 'null'
        wordcount = 0
        abstractlist = abstract.split()
        db = Dbconn()
        found_searchwords = []
        
        #Get the searchwords from database
        searchwords = set(db.retrieve_searchwords())

        print "Looking for searchwords in publication abstract"
        for sword in searchwords:
            my_regex = r"\b(?=\w)" + re.escape(sword) + r"\b(?!\w)"
            words_in_searchword = sword.count(' ')+1
            for word in abstractlist:
                multiword = word
                for i in range(1, words_in_searchword):
                    try:
                        multiword = multiword+' '+abstractlist[abstractlist.index(word)+i]
                    except Exception, e:
                        break
                #Check whether the word in abstract matches the word in searchwordlist
                if re.search(my_regex, multiword, re.IGNORECASE):
                    wordcount = wordcount + 1
                    found_searchwords.append(sword)
                    break               
        return wordcount, found_searchwords