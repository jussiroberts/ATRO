import unittest
from items import AtroItem
from pipelines import AtroPipeline

class PipelinesTests(unittest.TestCase):

	def setUp(self):
		self.p1 = AtroPipeline()

		#Title should not have a dot
	def testRemoveDotFromTitle(self):
		title = self.p1.process_title("Impaired cognitive flexibility in amyotrophic lateral sclerosis.")
		self.assertNotIn(".", title)

		#The number after "doi:" should be returned
	def testFindOnlyDoi(self):
		year_of_publication, journal, doi, pii = self.p1.process_otherinfo("Semin Cell Dev Biol. 2014 Jun 6.doi: 10.1016/j.semcdb.2014.05.016.")
		self.assertEquals("10.1016/j.semcdb.2014.05.016", doi)

		#Year of publication, journal, doi and pii information should be returned
	def testFindAll(self):
		year_of_publication, journal, doi, pii= self.p1.process_otherinfo("Semin Cell Dev Biol. 2014 Jun 6. pii: S1084-9521(14)00171-2. doi: 10.1016/j.semcdb.2014.05.016. ")
		self.assertEquals("2014", year_of_publication)
		self.assertEquals("Semin Cell Dev Biol", journal)
		self.assertEquals("10.1016/j.semcdb.2014.05.016", doi)
		self.assertEquals("S1084-9521(14)00171-2", pii)

		#The year should be returned
	def testFindYearOfPublicationNoSpaces(self):
		year_of_publication, journal, doi, pii= self.p1.process_otherinfo("Semin Cell Dev Biol. 2014Jun6. pii: S1084-9521(14)00171-2. doi: 10.1016/j.semcdb.2014.05.016. ")
		self.assertEquals("2014", year_of_publication)

		#Pii should be returned
	def testFindOnlyPii(self):
		year_of_publication, journal, doi, pii= self.p1.process_otherinfo("Semin Cell Dev Biol. 2014Jun6. pii: S1084-9521(14)00171-2.")
		self.assertEquals("S1084-9521(14)00171-2", pii)

		#Abstract should be grouped together
	def testAppendAbstractGroups(self):
		abstract = self.p1.process_abstract(['This', 'is', 'an', 'abstract.'])
		self.assertEquals("This is an abstract.", abstract)

if __name__ == '__main__':
    unittest.main()