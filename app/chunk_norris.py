from detector import Detector
from extractor import Extractor
from common.numpy_audio import normalize_audio
import json

from detector.det_factory import create_new_language_detector, create_new_silence_detector
from extractor.ext_factory import create_new_audio_extractor, create_new_info_extractor

SAMPLING_RATE=16000

class NorrisSetup:
    def __init__(self, model_path=None, silence_threshold=0.5, silence_duration=0.5,
                 info_extractor=None, audio_extractor=None, lang_detector=None, silence_detector=None):
        self.model_path = model_path
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        
        self.info_extractor = create_new_info_extractor(info_extractor)
        self.audio_extractor = create_new_audio_extractor(audio_extractor)
        self.lang_detector = create_new_language_detector(lang_detector)
        self.silence_detector = create_new_silence_detector(silence_detector)


class ChunkNorris(Detector, Extractor):
    def __init__(self, setup:NorrisSetup):    
        self.model_path = setup.model_path
        self.silence_threshold = setup.silence_threshold
        self.silence_duration = setup.silence_duration
        
        self.info_extractor = setup.info_extractor
        self.audio_extractor = setup.audio_extractor
        self.lang_detector = setup.lang_detector
        self.silence_detector = setup.silence_detector
        

    def run(self, input_path:str, output_path:str):
        media_info = self.info_extractor.extract(input_path)
        audio_tracks = []

        for track in media_info.tracks:
            if track.track_type == "Audio":
                raw_data_np = self.audio_extractor.extract(input_path, track.to_data().get('stream_identifier'), SAMPLING_RATE)
                norm_flat_buffer = normalize_audio(raw_data_np)
                audio_tracks.append({
                        "track": track,
                        "lang": self.lang_detector.detect(norm_flat_buffer),
                        "silence": self.silence_detector.detect(norm_flat_buffer, self.silence_threshold, self.silence_duration)
                    })

        for item in audio_tracks:
            print(json.dumps(item, indent=4, default=str))

