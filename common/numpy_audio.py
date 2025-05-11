import io
import numpy as np

def rawbytes_to_numpy(buffer: bytes) -> np.ndarray:
    buffer = io.BytesIO()
    buffer.seek(0)

    return np.frombuffer(buffer.read(), dtype=np.int16).flatten().astype(np.float32) / 32768.0