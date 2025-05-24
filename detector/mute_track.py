import numpy as np
from app.detector import Detector

class MuteTrackDetector(Detector):

    def __init__(self, threshold: float = 0.01):
        self.threshold = threshold

    def split_into_equal_size_chunks(self, input_data: np.ndarray, chunk_size: int) -> np.ndarray:
        num_chunks = len(input_data) // chunk_size
        return input_data[:num_chunks * chunk_size].reshape(num_chunks, chunk_size)

    
    def detect(self, input_data: np.ndarray) -> bool:
        if len(input_data) == 0:
            return True

        chunks = self.split_into_equal_size_chunks(input_data, 1024)

        means = np.mean(np.abs(chunks), axis=1)
        if np.any(means >= self.threshold):
            return False

        return True