

from extractor.audio_ffmpeg import AudioFFmpegExtractor
from extractor.mediainfo import MediaInfoExtractor


def create_new_audio_extractor (detector_type):
    if detector_type == 'ffmpeg':
        return AudioFFmpegExtractor()
    else:
        raise ValueError(f"Unknown detector type: {detector_type}")

def create_new_info_extractor (detector_type):
    if detector_type == 'mediainfo':
        return MediaInfoExtractor()
    else:
        raise ValueError(f"Unknown detector type: {detector_type}")