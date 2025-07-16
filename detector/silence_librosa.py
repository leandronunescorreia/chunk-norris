import librosa
import numpy as np
from app.ports.detector import Detector

class SilenceLibrosaDetector(Detector):

    def __init__(self, threshold: float = 0.01):
        self.threshold = threshold


    def split_into_chunks(self, input_data: np.ndarray, sr: int, chunk_size: int = 30) -> list:
        max_samples = chunk_size * sr  # Maximum samples per chunk
        silence_threshold = self.threshold  # Silence threshold
        chunks = []
        start = 0

        # Calculate the energy of the audio signal
        rms = librosa.feature.rms(y=input_data)[0]
        silence_frames = np.where(rms < silence_threshold)[0]

        for i in range(0, len(input_data), max_samples):
            end = min(i + max_samples, len(input_data))
            # Find the nearest silence frame within the range
            silence_in_range = silence_frames[(silence_frames >= i) & (silence_frames < end)]
            if len(silence_in_range) > 0:
                end = silence_in_range[0] * (len(input_data) // len(rms))  # Map frame to sample index
            chunks.append(input_data[start:end])
            start = end

        # Add the last chunk if any data remains
        if start < len(input_data):
            chunks.append(input_data[start:])

        return chunks
    
    def detect(self, input_data: np.ndarray) -> bool:
        # Calculate the root mean square (RMS) energy of the audio signal
        rms = librosa.feature.rms(y=input_data)

        # Check if the mean RMS energy is below the threshold
        return np.mean(rms) < self.threshold