import unittest
import os
from pathlib import Path
import numpy as np
import sys
from dotenv import load_dotenv, dotenv_values

import torch

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "..")))
from detector.language_whisper import LanguageWhisperDetector
from extractor.audio_ffmpeg import AudioFFmpegExtractor


class TestLanguageWhisperDetector(unittest.TestCase):
    TEST_ROOT = os.path.join(os.path.dirname(__file__))
    HOME_PATH = Path.home()

    def setUp(self):
        gpu_count = torch.cuda.device_count()
        self.assertGreaterEqual(gpu_count, 0, "No GPU available for testing.")

        conf_test_path = os.path.join(self.TEST_ROOT, ".test_env")
        self.assertTrue(os.path.exists(conf_test_path))
        config = dotenv_values(conf_test_path)

        model_path = os.path.join(os.getcwd(), config.get("MODEL_PATH", None))
        self.assertTrue(os.path.exists(model_path))

        self.detector = LanguageWhisperDetector(model_path=model_path, method="mel")
        self.audio_extractor = AudioFFmpegExtractor()

    def test_detect_language_returns_str(self):
        audio_path = os.path.join(
            self.TEST_ROOT, "resources", "Learn_OAI_Whisper_Sample_Audio01.m4a"
        )
        self.assertTrue(os.path.exists(audio_path), "Test audio file does not exist.")

        audio_buffer = self.audio_extractor.extract(
            file_name=audio_path, audio_track=[0], sampling=16000, mixed=False
        )
        self.assertIsInstance(audio_buffer, bytes, "Audio buffer should be bytes.")

        lang = self.detector.detect(audio_buffer)
        self.assertIsInstance(lang, str)
        self.assertTrue(len(lang) > 0)
        self.assertEqual(lang, "eng")


if __name__ == "__main__":
    unittest.main()
