import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))

import unittest
from extractor.audio_ffmpeg import AudioFFmpegExtractor
import numpy as np

class TestAudioFFmpegExtractor(unittest.TestCase):
    TEST_ROOT = os.path.join(os.path.dirname(__file__))
    HOME_PATH = Path.home()

    def setUp(self):
        self.extractor = AudioFFmpegExtractor()

    def test_get_command_with_filter_complex_mixed(self):
        file_name = "test_audio.mp4"
        audio_track = [8, 9]
        sampling = 16000
        mixed = True

        expected_command = [
            "ffmpeg",
            "-nostdin",
            "-threads", "0",
            "-i", file_name,
            "-filter_complex", "[0:a:0]pan=mono|c0=0.5*c8+0.5*c9[aout]",
            "-map", "[aout]",
            "-f", "s16le",
            "-ac", "1",
            "-acodec", "pcm_s16le",
            "-ar", str(sampling),
            "-"
        ]

        command = self.extractor.get_command_with_filter_complex(file_name, audio_track, sampling, mixed)
        self.assertEqual(command, expected_command)

    def test_get_command_with_filter_complex_non_mixed(self):
        file_name = "test_audio.mp4"
        audio_track = [7, 8]
        sampling = 16000
        mixed = False

        expected_command = [
            "ffmpeg",
            "-nostdin",
            "-threads", "0",
            "-i", file_name,
            "-filter_complex", "[0:a:7][0:a:8]amerge=inputs=2,pan=mono|c0=0.5*c0+0.5*c1[aout]",
            "-map", "[aout]",
            "-f", "s16le",
            "-ac", "1",
            "-acodec", "pcm_s16le",
            "-ar", str(sampling),
            "-"
        ]

        command = self.extractor.get_command_with_filter_complex(file_name, audio_track, sampling, mixed)
        self.assertEqual(command, expected_command)


    def test_with_mono_m4a_file(self):
        audio_path = os.path.join(self.TEST_ROOT, 'resources', 'Learn_OAI_Whisper_Sample_Audio01.m4a')
        audio_buffer = self.extractor.extract(file_name=audio_path, audio_track=[0], sampling=16000, mixed=False)
        self.assertGreater(len(audio_buffer), 0)
        self.assertIsInstance(audio_buffer, np.ndarray)
        self.assertIsInstance(audio_buffer[0], np.int16)

if __name__ == "__main__":
    unittest.main()