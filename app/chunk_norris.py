from detector import Detector
from extractor import Extractor

class NorrisSetup:
    def __init__(self, model_path=None, silence_threshold=0.5, silence_duration=0.5,
                 info_extractor=None, audio_extractor=None, lang_detector=None, silence_detector=None):
        self.model_path = model_path
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.info_extractor = info_extractor
        self.audio_extractor = audio_extractor
        self.lang_detector = lang_detector
        self.silence_detector = silence_detector


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
        # Implement the detection logic here
        pass

