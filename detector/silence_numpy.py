import numpy as np
from app.detector import Detector

class SilenceNumpyDetector(Detector):

    def __init__(self, threshold: float = 0.01):
        self.threshold = threshold


    def split_into_chunks(self, input_data: np.ndarray, chunk_size: int) -> np.ndarray:
        return input_data
    
    def detect(self, input_data: np.ndarray) -> bool:
        amplitude = np.mean(np.abs(input_data))
        return amplitude < self.threshold