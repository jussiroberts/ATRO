import re
from dbconn import Dbconn

class Wordcheck():
	#abstract = "this is a dummy abstract"
	#searchwords = ['banana', 'apple', 'dummy']
	#wordcount = 0

    @staticmethod
    def check(abstract):
        my_regex = 'null'
        wordcount = 0
        abstractlist = abstract.split()
        db = Dbconn()
        
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
                if re.search(my_regex, multiword, re.IGNORECASE):
                    wordcount = wordcount + 1
                    with open('foundsearchwords.txt', 'a') as f:
                        f.write('search word: {0}\n'.format(sword.encode('utf8'),))
                        f.write('word in abstract: {0}\n'.format(word.encode('utf8'),))
                        f.write('words found: {0}\n'.format(wordcount,))
                    break

                
        return wordcount