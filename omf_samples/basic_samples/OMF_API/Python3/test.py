import unittest
from program import main


class ProgramTestCase(unittest.TestCase):

	def test_itRuns(self):
	    main()


if __name__ == "__main__":
    unittest.main(True)
