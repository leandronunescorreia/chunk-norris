import numpy as np
from subprocess import CalledProcessError, run
from app.extractor import Extractor

class AudioFFmpegExtractor(Extractor):
    def extract(self, file_name: str, audio_track: int, sampling: int = 16000) -> np.ndarray:
        command = [
            "ffmpeg",
            "-nostdin",
            "-threads", "0",
            "-i", file_name,
            "-map", f"0:a:{audio_track}",
            "-f", "s16le",
            "-ac", "1",
            "-acodec", "pcm_s16le",
            "-ar", str(sampling),
            "-"
        ]

        try:
            out = run(command, capture_output=True, check=True).stdout
        except CalledProcessError as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

        # audio_data = np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

        return out