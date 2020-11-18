# Idea: assertions with >< (if we want to tolerate one mistake for example) - then we need to change the
# formalityTestResults.txt

import unittest
from pathlib import Path

path = Path("../formalityTestResults.txt")

class MyTestCase(unittest.TestCase):
    def test_consecutive_marks(self):
        f = open(path, "r")
        consecutive_marks_string = f.readline().strip()
        self.assertEqual(consecutive_marks_string,  '0 consecutive ! or ?')
        f.close()

    def test_all_caps_words(self):
        f = open(path, "r")
        all_lines = f.readlines()
        self.assertEqual(all_lines[1].strip(), '0 words in all caps found ')
        f.close()

    def test_spelling(self):
        f = open(path, "r")
        all_lines = f.readlines()
        self.assertEqual(all_lines[2].strip(), '0 spelling mistakes found')
        f.close()

    # def test_vocabulary_size(self):
    #     f = open(path, "r")
    #     all_lines = f.readlines()
    #     self.assertEqual(all_lines[3].strip(), 'TODO')
    #     f.close()

if __name__ == '__main__':
    unittest.main()
