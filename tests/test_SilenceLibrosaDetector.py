import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))

import numpy as np
import unittest
from detector.silence_librosa import SilenceLibrosaDetector

class TestSilenceLibrosaDetector(unittest.TestCase):
    def setUp(self):
        pass




if __name__ == "__main__":
    unittest.main()    