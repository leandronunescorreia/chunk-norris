# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))

import numpy as np
import unittest
from detector.mute_track import MuteTrackDetector

class TestMuteTrackDetector(unittest.TestCase):
    def setUp(self):
        pass

    
    def test_detect_empty_input(self):
        detector = MuteTrackDetector()
        assert detector.detect(np.array([])) is True

    def test_detect_all_zeros(self):
        detector = MuteTrackDetector()
        data = np.zeros(4096)
        assert detector.detect(data) is True

    def test_detect_above_threshold(self):
        detector = MuteTrackDetector(threshold=0.01)
        data = np.ones(4096) * 0.02
        assert detector.detect(data) is False

    def test_detect_below_threshold(self):
        detector = MuteTrackDetector(threshold=0.05)
        data = np.ones(4096) * 0.01
        assert detector.detect(data) is True

    def test_detect_mixed_chunks(self):
        detector = MuteTrackDetector(threshold=0.01)
        data = np.concatenate([
            np.zeros(1024),
            np.ones(1024) * 0.02,
            np.zeros(1024),
            np.ones(1024) * 0.005
        ])
        assert detector.detect(data) is False


if __name__ == "__main__":
    unittest.main()