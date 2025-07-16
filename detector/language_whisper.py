from app.ports.detector import Detector
import torch
import whisper
from common.numpy_audio import rawbytes_to_numpy
import threading

class LanguageWhisperDetector(Detector):
    def __init__(self, model_path=None, method="mel"):
        super().__init__()
        self.model_path = model_path
        self.model = None
        self.method = method
        self.model_loaded_event = threading.Event()

        self.load_thread = threading.Thread(target=self.load_model)
        self.load_thread.start()
      
    def load_model(self):
        if not self.model_path:
            self.model = whisper.load_model("turbo")
        else:
            self.model = whisper.load_model(name='turbo', download_root=self.model_path)

        self.model.to("cuda" if torch.cuda.is_available() else "cpu")
        self.model.eval()
        self.model_loaded_event.set()
    
    def detect(self, input_data):
        self.model_loaded_event.wait()

        if self.method == "mel":
            audio = rawbytes_to_numpy(input_data)
            mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

            _, probs = self.model.detect_language(mel)
            audio_lang = max(probs, key=probs.get)
            return audio_lang
        else:
            raise ValueError(f"Unsupported method: {self.method}. Supported methods: mel.")