import unittest
from items import AtroItem
from pipelines import AtroPipeline

class PipelinesTests(unittest.TestCase):

	def setUp(self):
		self.p1 = AtroPipeline()

	def testRemoveDotFromtitle(self):
		title = self.p1.process_title("Hello.")
		self.assertNotIn(".", title)

	def testFindDoi(self):
		year_of_publication, journal, doi, pii = self.p1.process_otherinfo("jajajaja doppelganger 851241 doi: 8124123")
		self.assertEquals("8124123", doi)

	def testFindOtherinfo(self):
		year_of_publication, journal, doi, pii= self.p1.process_otherinfo("Semin Cell Dev Biol. 2014 Jun 6. pii: S1084-9521(14)00171-2. doi: 10.1016/j.semcdb.2014.05.016. ")
		self.assertEquals("2014", year_of_publication)
		self.assertEquals("Semin Cell Dev Biol", journal)
		self.assertEquals("10.1016/j.semcdb.2014.05.016", doi)
		self.assertEquals("S1084-9521(14)00171-2", pii)


if __name__ == '__main__':
    unittest.main()