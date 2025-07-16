import unittest
import sys
import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values
import platform

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from app.chunk_norris import NorrisSetup, ChunkNorris

class TestChunkNorrisIntegration(unittest.TestCase):
    TEST_ROOT = os.path.join(os.path.dirname(__file__))
    HOME_PATH = Path.home()
        
    def setUp(self):
        conf_test_path = os.path.join(self.TEST_ROOT, ".test_env")
        self.assertTrue(os.path.exists(conf_test_path))
        config = dotenv_values(conf_test_path)
        # Setup NorrisSetup with default arguments
        self.norris_setup = NorrisSetup(
            model_path=os.path.join(self.HOME_PATH, config.get("MODEL_PATH", None)),
            silence_threshold=config.get("SILENCE_THRESHOLD", None),
            silence_duration=config.get("SILENCE_DURATION", None),
            info_extractor=config.get("INFO_EXTRACTOR", None),
            audio_extractor=config.get("AUDIO_EXTRACTOR", None),
            lang_detector=config.get("LANG_DETECTOR", None),
            silence_detector=config.get("SILENCE_DETECTOR", None),
            mute_detector=config.get("MUTED_DETECTOR", None)
        )

        self.chunk_norris = ChunkNorris(setup=self.norris_setup)

    def test_run_integration(self):
        # Use a real input file for integration testing
        input_path = os.path.join(self.TEST_ROOT, "..", "jupyter", "20241125-NOVA_EQUIPE_na_Frmula_1.mp4")
        output_path = "test_output.json"

        self.assertTrue(os.path.exists(input_path))

        # Run the method
        result = self.chunk_norris.run(input_path)

        # Save the result to the output file
        with open(output_path, "w") as f:
            f.write(result.to_json())

        # Assertions
        self.assertEqual(result.filename, "20241125-NOVA_EQUIPE_na_Frmula_1.mp4")
        self.assertIsNotNone(result.audio_tracks)
        self.assertGreater(len(result.audio_tracks), 0)

        # Clean up
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == "__main__":
    unittest.main()
