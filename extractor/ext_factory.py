

from extractor.audio_ffmpeg import AudioFFmpegExtractor
from extractor.mediainfo import MediaInfoExtractor


def create_new_audio_extractor (detector_type, config=None):
    if detector_type == 'ffmpeg':
        return AudioFFmpegExtractor(config)
    else:
        raise ValueError(f"Unknown detector type: {detector_type}")

def create_new_info_extractor (detector_type, config=None):
    if detector_type == 'mediainfo':
        return MediaInfoExtractor(config)
    else:
        raise ValueError(f"Unknown detector type: {detector_type}")