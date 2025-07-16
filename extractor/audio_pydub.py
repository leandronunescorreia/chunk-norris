from pydub import AudioSegment
import numpy as np
from app.ports.extractor import Extractor

class AudioPydubExtractor(Extractor):
    
    def extract(self, file_name: str, audio_track: list[int], sampling: int = 16000, mixed: bool = False) -> np.ndarray:
        """
        Extract and downmix specified audio tracks into a single numpy array.

        Args:
            file_name (str): Path to the audio file.
            audio_track (list[int]): List of audio track indices to extract and downmix.
            sampling (int): Sampling rate for the audio.
            mixed (bool): Whether to mix the tracks into one.

        Returns:
            np.ndarray: Downmixed audio as a numpy array.
        """
        # Load the audio file
        audio = AudioSegment.from_file(file_name)

        # Ensure the file has 16 channels
        if audio.channels < len(audio_track):
            raise ValueError(f"The audio file have only {audio.channels}.")

        # Extract the specified tracks
        tracks = [audio.split_to_mono()[i] for i in audio_track]

        # Downmix the tracks if mixed is True
        if mixed:
            downmixed = tracks[0]
            for track in tracks[1:]:
                downmixed = downmixed.overlay(track)
            tracks = [downmixed]

        # Convert to numpy array
        samples = np.array(
            [np.array(track.get_array_of_samples(), dtype=np.float32) for track in tracks]
        )

        # Normalize to range [-1, 1]
        samples /= np.iinfo(audio.array_type).max

        # If mixed, return a single array; otherwise, return stacked arrays
        return samples[0] if mixed else np.stack(samples)