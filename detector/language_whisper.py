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
            self.model = whisper.load_model(name="turbo", download_root=self.model_path)

        self.model.to("cuda" if torch.cuda.is_available() else "cpu")
        self.model.eval()
        self.model_loaded_event.set()

    def detect(self, input_data):
        self.model_loaded_event.wait()

        if self.method == "mel":
            audio_np = rawbytes_to_numpy(input_data)

            if audio_np.ndim > 1:
                audio_np = audio_np.mean(axis=1)

            audio_np = whisper.pad_or_trim(audio_np)

            mel = whisper.log_mel_spectrogram(
                audio_np, n_mels=self.model.dims.n_mels
            ).to(self.model.device)

            _, probs = self.model.detect_language(mel)
            language = max(probs, key=probs.get)
            return language
        else:
            raise ValueError(
                f"Unsupported method: {self.method}. Supported methods: mel."
            )
