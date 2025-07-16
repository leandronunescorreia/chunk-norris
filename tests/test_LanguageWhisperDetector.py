import unittest
import os
from pathlib import Path
import numpy as np
import sys
from dotenv import load_dotenv, dotenv_values

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))
from detector.language_whisper import LanguageWhisperDetector
from extractor.audio_ffmpeg import AudioFFmpegExtractor

class TestLanguageWhisperDetector(unittest.TestCase):
    TEST_ROOT = os.path.join(os.path.dirname(__file__))
    HOME_PATH = Path.home()
    
    def setUp(self):
        conf_test_path = os.path.join(self.TEST_ROOT, ".test_env")
        self.assertTrue(os.path.exists(conf_test_path))
        config = dotenv_values(conf_test_path)
        model_path = os.path.join(self.HOME_PATH, config.get("MODEL_PATH", None))
        self.detector = LanguageWhisperDetector(model_path=None, method="mel")

    def test_detect_language_returns_str(self):
        self.audio_extractor = AudioFFmpegExtractor()

        audio_path = os.path.join(self.TEST_ROOT, 'resources', 'Learn_OAI_Whisper_Sample_Audio01.m4a')
        audio_buffer = self.audio_extractor.extract(file_name=audio_path, audio_track=[0], sampling=16000, mixed=False)
    
        lang = self.detector.detect(audio_buffer)
        self.assertIsInstance(lang, str)
        self.assertTrue(len(lang) > 0)

    def test_unsupported_method_raises(self):
        detector = LanguageWhisperDetector(method="invalid")
        detector.load_thread.join()
        dummy_audio = np.zeros(16000, dtype=np.float32).tobytes()
        with self.assertRaises(ValueError):
            detector.detect(dummy_audio)

if __name__ == "__main__":
    unittest.main()
