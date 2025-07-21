import io
import numpy as np


def rawbytes_to_numpy(buffer: bytes) -> np.ndarray:
    audio = np.frombuffer(buffer, dtype=np.int16).astype(np.float32) / 32768.0
    return audio
