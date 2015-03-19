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
		
		#global searchwords
		searchwords = ['cervical', 'cancer', 'occipital']	
		for sword in searchwords:
			
			for word in abstractlist:
				my_regex = r"\b(?=\w)" + re.escape(sword) + r"\b(?!\w)"

			
				#if my_regex in word:
				if re.search(my_regex, word, re.IGNORECASE):
					
					wordcount = wordcount + 1
					with open('foundsearchwords.txt', 'a') as f:
						f.write('search word: {0}\n'.format(sword.encode('utf8'),))
						f.write('word in abstract: {0}\n'.format(word.encode('utf8'),))
						f.write('words found: {0}\n'.format(wordcount,))
					break
		return wordcount
				
				