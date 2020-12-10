# Idea: assertions with >< (if we want to tolerate one mistake for example) - then we need to change the
# formalityTestResults.txt

import unittest
from pathlib import Path

path = Path("../formalityTestResults.txt")

class MyTestCase(unittest.TestCase):

    def test_marks_title(self):
        f = open(path, "r")
        marks_string = f.readline().strip()
        self.assertEqual(marks_string,  '0 ! or ? in title')
        f.close()

    def test_marks_total(self):
        f = open(path, "r")
        all_lines = f.readlines()
        self.assertEqual(all_lines[1].strip(),  '0 ? in total')
        f.close()

    def test_consecutive_marks(self):
        f = open(path, "r")
        all_lines = f.readlines()
        self.assertEqual(all_lines[2].strip(),  '0 consecutive ! or ?')
        f.close()

    def test_all_caps_words(self):
        f = open(path, "r")
        all_lines = f.readlines()
        self.assertEqual(all_lines[3].strip(), '0 words in all caps found')
        f.close()

    def test_spelling_title(self):
        f = open(path, "r")
        all_lines = f.readlines()
        self.assertEqual(all_lines[4].strip(), '0 spelling mistakes found in title')
        f.close()

    def test_spelling(self):
        f = open(path, "r")
        all_lines = f.readlines()
        self.assertEqual(all_lines[5].strip(), 'Acceptable error rate')
        f.close()

    def test_vocabulary(self):
        f = open(path, "r")
        all_lines = f.readlines()
        self.assertEqual(all_lines[6].strip(), 'Higher than average lexical richness')
        f.close()


if __name__ == '__main__':
    unittest.main()
