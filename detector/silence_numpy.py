import numpy as np
from app.ports.detector import Detector

class SilenceNumpyDetector(Detector):

    def __init__(self, threshold: float = 0.01):
        self.threshold = threshold


    def calculate_segment_duration_and_num_segments(self, duration_seconds, overlap_seconds, max_size, bitrate_kbps):
        """Calculate the duration and number of segments for an audio file."""
        seconds_for_max_size = (max_size * 8 * 1024) / bitrate_kbps
        num_segments = max(2, int(duration_seconds / seconds_for_max_size) + 1)
        total_overlap = (num_segments - 1) * overlap_seconds
        actual_playable_duration = (duration_seconds - total_overlap) / num_segments
        return num_segments, actual_playable_duration + overlap_seconds

    def split_into_chunks(self, input_data: np.ndarray, chunk_size: int) -> np.ndarray:
        return input_data
    
    def detect(self, input_data: np.ndarray) -> bool:
        amplitude = np.mean(np.abs(input_data))
        return amplitude < self.threshold