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
        
        searchwords = db.retrieve_searchwords()

        for sword in searchwords:
            print sword
            for word in abstractlist:
                my_regex = r"\b(?=\w)" + re.escape(sword) + r"\b(?!\w)"
                
                
                words_in_searchword = sword.count(' ')+1
                multiword = word
                for i in range(1, words_in_searchword):
                    try:
                        multiword = multiword+' '+abstractlist[abstractlist.index(word)+i]
                    except Exception, e:
                        print "End of abstract"
                        print str(e)
                        break
                if re.search(my_regex, multiword, re.IGNORECASE):
                    wordcount = wordcount + 1
                    found_searchwords.append(sword)
                    break

                
        return wordcount, found_searchwords