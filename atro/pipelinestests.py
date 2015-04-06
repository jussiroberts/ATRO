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
		year_of_publication, journal, doi = self.p1.process_otherinfo("jajajaja doppelganger 851241 doi: 8124123")
		self.assertEquals("8124123", doi)

	def testFindOtherinfo(self):
		year_of_publication, journal, doi = self.p1.process_otherinfo("PLoS One. 2014 Aug 11;9(8):e104568. doi: 10.1371/journal.pone.0104568. eCollection 2014.")
		self.assertEquals("2014", year_of_publication)
		self.assertEquals("PLoS One", journal)
		self.assertEquals("10.1371/journal.pone.0104568", doi)


if __name__ == '__main__':
    unittest.main()