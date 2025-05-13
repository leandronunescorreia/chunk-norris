from detector.language_whisper import LanguageWhisperDetector
from detector.silence_librosa import SilenceLibrosaDetector
from detector.silence_numpy import SilenceNumpyDetector

def create_new_language_detector (detector_type, config=None):
    if detector_type == 'whisper':
        return LanguageWhisperDetector(config)
    else:
        raise ValueError(f"Unknown detector type: {detector_type}")

def create_new_silence_detector (detector_type, config=None):
    if detector_type == 'librosa':
        return SilenceLibrosaDetector(config)
    elif detector_type == 'numpy':
        return SilenceNumpyDetector(config.get('threshold', 0.01))
    else:
        raise ValueError(f"Unknown detector type: {detector_type}")