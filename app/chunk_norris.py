from detector import Detector
from extractor import Extractor

class ChunkNorris(Detector, Extractor):
    def __init__(self, config):
        self.model_path = config.get("model_path", None)
        self.infoExtractor =  config.get("info_extractor", None)
        

    def run(self, input_data):
        # Implement the detection logic here
        pass

