import re

class Wordcheck():
	#abstract = "this is a dummy abstract"
	#searchwords = ['banana', 'apple', 'dummy']
	#wordcount = 0

    @staticmethod
    def check(abstract):
        my_regex = 'null'
        wordcount = 0
        abstractlist = abstract.split()
		
        #with open('searchwords_list.txt') as f:
            #searchwords = f.readlines()
        #with open('kokkeilu.txt', 'a') as f:
        #    for sword in searchwords:
        #        f.write('{0}'.format(sword.encode('utf8'),))
        searchwords = ['cancer', 'tumor', 'false-positive', 'high sGPT levels']

        for sword in searchwords:
            for word in abstractlist:
                my_regex = r"\b(?=\w)" + re.escape(sword) + r"\b(?!\w)"
                try:

                    nextwordindex = abstractlist.index(word)+1
                    nextword = abstractlist[nextwordindex]
                    nextnextword = abstractlist[nextwordindex+1]
                except:
                    print "end of abstract"
                if (" ") in sword:
                    if re.search(my_regex, word+' '+nextword+' '+nextnextword, re.IGNORECASE):
                        wordcount = wordcount + 1
                        with open('foundsearchwords.txt', 'a') as f:
                            f.write('search word: {0}\n'.format(sword.encode('utf8'),))
                            f.write('word in abstract: {0}\n'.format(word.encode('utf8'),))
                            f.write('words found: {0}\n'.format(wordcount,))
                        break

                if re.search(my_regex, word, re.IGNORECASE):

                    wordcount = wordcount + 1
                    with open('foundsearchwords.txt', 'a') as f:
                        f.write('search word: {0}\n'.format(sword.encode('utf8'),))
                        f.write('word in abstract: {0}\n'.format(word.encode('utf8'),))
                        f.write('words found: {0}\n'.format(wordcount,))
                    break
        return wordcount