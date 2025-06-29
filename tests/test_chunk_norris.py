import unittest
import sys
import os
from dotenv import load_dotenv, dotenv_values

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from app.chunk_norris import NorrisSetup, ChunkNorris

class TestChunkNorrisIntegration(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        conf_test_path = os.path.join(os.getcwd(), "tests", ".test_env")
        config = dotenv_values(conf_test_path)
        # Setup NorrisSetup with default arguments
        self.norris_setup = NorrisSetup(
            model_path=None,
            silence_threshold=0.5,
            silence_duration=0.25,
            info_extractor="mediainfo",
            audio_extractor="ffmpeg",
            lang_detector="whisper",
            silence_detector="librosa",
            mute_detector="numpy"
        )

        self.chunk_norris = ChunkNorris(setup=self.norris_setup)

    def test_run_integration(self):
        # Use a real input file for integration testing
        input_path = os.path.join("jupyter", "20241125-NOVA_EQUIPE_na_Frmula_1.mp4")
        output_path = "test_output.json"

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
