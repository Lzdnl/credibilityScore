import unittest
from pathlib import Path


path = Path("../neutralityTestResults.txt")


class MyTestCase(unittest.TestCase):

    def test_superlatives(self):
        f = open(path, "r")
        marks_string = f.readline().strip()
        self.assertEqual(marks_string,  '0 superlatives identified')
        f.close()

    def test_profanities(self):
        f = open(path, "r")
        all_lines = f.readlines()
        self.assertEqual(all_lines[1].strip(),  '0 profanities found in 0 instances')
        f.close()

    def test_emotional(self):
        f = open(path, "r")
        all_lines = f.readlines()
        self.assertEqual(all_lines[2].strip(),  'Acceptable emotional word ratio')
        f.close()

    def test_slurs(self):
        f = open(path, "r")
        all_lines = f.readlines()
        self.assertEqual(all_lines[3].strip(),  '0 slurs identified')
        f.close()


if __name__ == '__main__':
    unittest.main()
