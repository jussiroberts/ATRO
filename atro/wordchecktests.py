import unittest
from wordcheck import Wordcheck

class WordcheckTests(unittest.TestCase):

	def setUp(self):
		self.w1 = Wordcheck()

	#Should find acclimitization
	def testFindLowercase(self):
		wordcount, found_searchwords = self.w1.check("acclimatization these days is a common problem")
		self.assertIn("acclimatization", found_searchwords)
		self.assertEqual(wordcount, 1)

	#Should find acetylcholinesterase
	def testFindUpperCase(self):
		wordcount, found_searchwords = self.w1.check("ACETYLCHOLINESTERASE IS DANGEROUS IF NOT HANDLED PROPERLY")
		self.assertIn("acetylcholinesterase", found_searchwords)
		self.assertEqual(wordcount, 1)

	#Should find activins, activin receptors, acute kidney injury, kidney and denervation
	def testFindConsecutiveSearchwords(self):
		wordcount, found_searchwords = self.w1.check("activins and activin receptors are the reason for acute kidney injury denervation")
		self.assertIn("activins", found_searchwords)
		self.assertIn("activin receptors", found_searchwords)
		self.assertIn("acute kidney injury", found_searchwords)
		self.assertIn("kidney", found_searchwords)
		self.assertIn("denervation", found_searchwords)
		self.assertEqual(wordcount, 5)

	#Should find activins only one, wordcount should be 1
	def testFindSearchwordOnlyOnce(self):
		wordcount, found_searchwords = self.w1.check("activins activins activins are ACTIVINS ACTIVINS activins? activins!!!")
		self.assertIn("activins", found_searchwords)
		self.assertEqual(wordcount, 1)

	#Should find adaptor proteins, signal transducing: genetics
	def testFindLongSearchword(self):
		wordcount, found_searchwords = self.w1.check("adaptor proteins, signal transducing: genetics")
		self.assertIn("adaptor proteins, signal transducing: genetics", found_searchwords)
		self.assertIn("adaptor proteins, signal transducing", found_searchwords)
		self.assertIn("proteins", found_searchwords)
		self.assertEqual(wordcount, 3)

	#Should find 24 different searchwords
	def testFindManySearchwords(self):
		wordcount, found_searchwords = self.w1.check("Xenopus laevis Yeasts Young Adult Zebrafish Warfarin Virulence Vital Capacity Vasculitis Vacuoles Uric Acid Up-Regulation Ubiquitins Ubiquitination Tyrosine Tunicamycin Triazoles Tretinoin Transgenes Toxoplasma Touch Time Factors Thymidine")
		self.assertEqual(wordcount, 24)

	#Should find xenopus and xenopus laevis
	def testfindWithChars(self):
		wordcount, found_searchwords = self.w1.check("bladders. and :xenopus laevis,")
		self.assertIn("xenopus", found_searchwords)
		self.assertIn("xenopus laevis", found_searchwords)
		self.assertEqual(wordcount, 2)



if __name__ == '__main__':
    unittest.main()