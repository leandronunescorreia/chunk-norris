from detector.language_whisper import LanguageWhisperDetector
from detector.silence_librosa import SilenceLibrosaDetector
from detector.silence_numpy import SilenceNumpyDetector
from detector.mute_track import MuteTrackDetector

def create_new_language_detector (detector_type, model_path, method):
    if detector_type == 'whisper':
        return LanguageWhisperDetector(model_path, method)
    else:
        raise ValueError(f"Unknown detector type: {detector_type}")

def create_new_silence_detector (detector_type):
    if detector_type == 'librosa':
        return SilenceLibrosaDetector()
    elif detector_type == 'numpy':
        return SilenceNumpyDetector()
    else:
        raise ValueError(f"Unknown detector type: {detector_type}")


def create_new_mute_detector (detector_type):
    if detector_type == 'librosa':
        return None
    elif detector_type == 'numpy':
        return MuteTrackDetector()
    else:
        raise ValueError(f"Unknown detector type: {detector_type}")