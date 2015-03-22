# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import psycopg2
from datetime import datetime
from wordcheck import Wordcheck

#The pipeline processes all items that are yielded by the spider. Each item contains relevant metadata for one publication.
class AtroPipeline(object):
    def process_item(self, item, spider):
        w1 = Wordcheck()
        publicationrank = 0
        #Write metadata to a txt file for testing purposes until database is available again
        with open('atro1.txt', 'a') as f, open('excepts.txt', 'a') as fb:
            #Since the metadata is saved to "dictionary" containers they have to be iterated through to get the individual 
            #elements

            for t in item['title']: 
                #Check to see whether the title ends with a dot. Dots in the end don't look good in the database so we want to
                #remove those
                if t.endswith('.'):
                    #Here we save the left side of the string (the side before the dot) to a variable and discard the dot
                    #For example: the string "Test."'s last element is a dot. t[-1] points to that element. Now since we want
                    #to get all elements before that dot we specify t[:-1]
                    t = t[:-1]
                    try:
                        f.write('title: {0}\n'.format(t.encode('utf8'),))
                    except:
                        fb.write('No title available\n')
                else:   
                    f.write('title: {0}\n'.format(t.encode('utf8'),))

            for a in item['author']:
                try:
                    f.write('author: {0}\n'.format(a.encode('utf8'),))
                except:
                    fb.write('No author available\n')
            #for j in item['journal']:
                #Remove the dot in the end
                #if j.endswith('.'):
                #    j = j[:-1]
                #    f.write('journal: {0}\n'.format(j.encode('utf8'),))
                #else:
                #    f.write('journal: {0}\n'.format(j.encode('utf8'),))

            #The item otherinfo contains some metadata that is grouped together in a single html element on PubMed.
            #We only want to get the publication year, which is the first word in the html element, as well as the doi which 
            #is in the middle of the html element. 
            for p in item['otherinfo']:
                #First change the item element to a string so we can apply string methods to it.
                otherinfostr = str(p.encode('utf8'))
                #Now that the item element is a string, we can split the string into parts. Now every word that is separated
                #by a space is a single string in this list
                otherinfolist = otherinfostr.split(" ")
                #To get the publication year we need to separate the metadata by a dot, since the publication year follows
                #the journal which ends in a dot.
                otherinfolist2 = otherinfostr.split(".")
                #Now the metadata is split into elements separated by dots. We still need to split the part containing the 
                #publication year by spaces to separate the actual publication year from the others. 
                publicationyearlist = otherinfolist2[1].split(' ')
                #Since we know that the publication year is the first word in the list (the first element [0] is a space) 
                #we can specify publicationyearlist[1] to get the publication year 
                try:
                    f.write('publication year: {0}\n'.format(publicationyearlist[1],))
                except:
                    fb.write('No publication year available\n')
                #Now we want to find the doi of the publication. We know that the html element on PubMed follows the syntax
                #"doi: xxx" where xxx is the actual doi code. So the list element we want to find is the next element after 
                #the word "doi". 
                try:    
                    #Here we get the next element after the word "doi"
                    index = otherinfolist.index('doi:') + 1
                    #Again, we want to remove the last dot from the doi code if the dot is in the end
                    if otherinfolist[index].endswith('.'):
                        doi = otherinfolist[index][:-1]
                        f.write('doi: {0}\n'.format(doi.encode('utf8'),))
                    else:
                        f.write('doi: {0}\n'.format(otherinfolist[index],))
                except:
                    #Some publications don't have a doi
                    fb.write('No doi available\n')
                try:
                    f.write('journal: {0}\n'.format(otherinfolist2[0],))
                except:
                    fb.write('No journal available\n')
            #Abstracts on PubMed are sometimes grouped into different parts, for example: introduction, methods, results...
            #We want to have the whole abstract in a single string so we can put it to the database, that's why we need to
            #append the strings in the item together.
            ab = ''
            for b in item['abstract']:
                #Append the different abstract groups together
                ab += str(b.encode('utf8'))+' '
            #We want to remove the last space in the end of the abstract
            ab = ab[:-1]
            try:
                publication_rank = w1.check(ab)
                
            except:
                fb.write('No abstract to search\n')
            try:
                f.write('publication rank: {0}\n'.format(publication_rank))

            except:
                fb.write('No publication rank\n')
            try:
                f.write('abstract: {0}\n'.format(ab.encode('utf8'),))
            except:
                fb.write('No abstract available\n')
            #The keywords on PubMed are grouped together in a single html element, where the keywords are separated 
            #by semicolons. Since we have a separate table for keywords, we want to get the individual keywords to their own
            #columns.
            try:
                for k in item['keywords']:
                   keywordstr = str(k.encode('utf8'))
                   #Split the keywords by semicolons into strings in a list
                   keywordlist = keywordstr.split("; ")
                   #Iterate through the list and print the individual keywords
                   for key in keywordlist:
                      f.write('keywords: {0}\n'.format(key.encode('utf8'),))
            except:
                fb.write('No keywords available\n')
            f.write('Date crawled: {0}\n'.format(str(datetime.now()),))
            f.write('...\n')


        
        return item
