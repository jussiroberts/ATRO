import unittest
from wordcheck import Wordcheck

class WordcheckTests(unittest.TestCase):

	def setUp(self):
		self.w1 = Wordcheck()

	def testFindLowercase(self):
		wordcount, found_searchwords = self.w1.check("acclimatization these days is a common problem")
		self.assertEqual(wordcount, 1)

	def testFindUpperCase(self):
		wordcount, found_searchwords = self.w1.check("ACETYLCHOLINESTERASE IS DANGEROUS IF NOT HANDLED PROPERLY")
		self.assertEqual(wordcount, 1)

	def testFindConsecutiveSearchwords(self):
		wordcount, found_searchwords = self.w1.check("activins and activin receptors are the reason for acute kidney injury denervation")
		self.assertEqual(wordcount, 5)

	def testFindSearchwordOnlyOnce(self):
		wordcount, found_searchwords = self.w1.check("activins activins activins are ACTIVINS ACTIVINS activins? activins!!!")
		self.assertEqual(wordcount, 1)

	def testReturnFoundSearchwords(self):
		wordcount, found_searchwords = self.w1.check("activins and activin receptors are the reason for acute kidney injury denervation")
		self.assertIn("acute kidney injury", found_searchwords)
		self.assertIn("activins", found_searchwords)
		self.assertIn("activin receptors", found_searchwords)
		self.assertIn("denervation", found_searchwords)
		self.assertIn("kidney", found_searchwords)

	def testFindLongSearchword(self):
		wordcount, found_searchwords = self.w1.check("adaptor proteins, signal transducing: genetics")
		self.assertEqual(wordcount, 3)

	def testFindManySearchwords(self):
		wordcount, found_searchwords = self.w1.check("Xenopus laevis Yeasts Young Adult Zebrafish Warfarin Virulence Vital Capacity Vasculitis Vacuoles Uric Acid Up-Regulation Ubiquitins Ubiquitination Tyrosine Tunicamycin Triazoles Tretinoin Transgenes Toxoplasma Touch Time Factors Thymidine")
		self.assertEqual(wordcount, 24)

	def testfindWithChars(self):
		wordcount, found_searchwords = self.w1.check("bladders. and :xenopus laevis,")
		self.assertEqual(wordcount, 2)



if __name__ == '__main__':
    unittest.main()