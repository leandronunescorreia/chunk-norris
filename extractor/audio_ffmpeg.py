import numpy as np
from subprocess import CalledProcessError, run
from app.ports.extractor import Extractor

class AudioFFmpegExtractor(Extractor):

    def get_command_with_filter_complex(self, file_name, audio_track, sampling, mixed):
        if mixed:
            if len(audio_track) > 1:
                pan_filter = "[0:a:0]pan=mono|c0=" + "+".join([f"0.5*c{track}" for track in audio_track])

            return [
            "ffmpeg",
            "-nostdin",
            "-threads", "0",
            "-i", file_name,
            "-filter_complex", pan_filter+"[aout]",
            "-map", "[aout]",
            "-f", "s16le",
            "-ac", "1",
            "-acodec", "pcm_s16le",
            "-ar", str(sampling),
            "-"
            ]
        else:
            if len(audio_track) > 1:
                stream_indices = "".join([f"[0:a:{track}]" for track in audio_track])
                multiple_streams = f"{stream_indices}amerge=inputs={len(audio_track)},pan=mono|c0=" + "+".join([f"0.5*c{idx}" for idx in range(len(audio_track))])
            return [
            "ffmpeg",
            "-nostdin",
            "-threads", "0",
            "-i", file_name,
            "-filter_complex", multiple_streams+"[aout]",            
            "-map", "[aout]",
            "-f", "s16le",
            "-ac", "1",
            "-acodec", "pcm_s16le",
            "-ar", str(sampling),
            "-"
            ]

    def get_default_command(self, file_name, audio_track, sampling):
        audio_map = None
        if len(audio_track) > 1:
            audio_map = f"0:a:{audio_track[0]}"

        command = [
            "ffmpeg",
            "-nostdin",
            "-threads", "0",
            "-i", file_name,
        ]
        if audio_map:
            command += ["-map", audio_map]
        command += [
            "-f", "s16le",
            "-ac", "1",
            "-acodec", "pcm_s16le",
            "-ar", str(sampling),
            "-"
        ]
        return command
    def extract(self, file_name: str, audio_track: list[int], sampling: int = 16000, mixed:bool=False) -> np.ndarray:
        command = self.get_default_command(file_name, audio_track, sampling) if not mixed else self.get_command_for_mixed_channel(file_name, audio_track, sampling) 

        try:
            out = run(command, capture_output=True, check=True).stdout
        except CalledProcessError as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

        # audio_data = np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

        return np.frombuffer(out, dtype=np.int16)