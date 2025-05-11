from detector import Detector
import whisper
from common.numpy_audio import rawbytes_to_numpy
import threading

class LanguageWhisperDetector(Detector):
    def __init__(self, config):
        super().__init__()
        self.model_path = config.get("model_path", None)
        self.model_loaded = False
        self.model = None
        self.method = config.get("method", "mel")

        self.load_thread = threading.Thread(target=self.load_model)
        self.load_thread.start()
      

    def load_model(self):
        self.model = whisper.load_model(self.model_path)
        self.model_loaded = True
    
    def detect(self, input_data: bytes):
        if self.model_loaded:

            if self.method == "mel":
                audio = rawbytes_to_numpy(input_data)
                mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

                _, probs = self.model.detect_language(mel)
                audio_lang = max(probs, key=probs.get)
                return audio_lang