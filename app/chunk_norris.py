from common.numpy_audio import normalize_audio

from detector.det_factory import create_new_language_detector, create_new_silence_detector, create_new_mute_detector
from extractor.ext_factory import create_new_audio_extractor, create_new_info_extractor

from app.models.result_info import ResultInfo
from app.models.audio_track import AudioTrack

SAMPLING_RATE=16000

class NorrisSetup:
    def __init__(self, model_path=None, silence_threshold=0.5, silence_duration=0.5,
                 info_extractor=None, audio_extractor=None, lang_detector=None,
                 silence_detector=None, mute_detector=None):
        self.model_path = model_path
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        
        self.info_extractor = create_new_info_extractor(info_extractor)
        self.audio_extractor = create_new_audio_extractor(audio_extractor)
        self.lang_detector = create_new_language_detector(lang_detector, self.model_path, "mel")
        self.silence_detector = create_new_silence_detector(silence_detector)
        self.mute_detector = create_new_mute_detector(mute_detector)


class ChunkNorris():
    def __init__(self, setup:NorrisSetup):    
        self.model_path = setup.model_path
        self.silence_threshold = setup.silence_threshold
        self.silence_duration = setup.silence_duration
        
        self.info_extractor = setup.info_extractor
        self.audio_extractor = setup.audio_extractor
        self.lang_detector = setup.lang_detector
        self.silence_detector = setup.silence_detector
        self.mute_detector = setup.mute_detector
        

    def run(self, input_path:str):
        media_info = self.info_extractor.extract(input_path)
        audio_tracks = []

        if not self.validate_mediainfo(media_info):
            raise ValueError("Invalid media info provided.")

        result_info = ResultInfo(
            filename=media_info.get('filename', None),
            duration=media_info.get('duration', None),
            audio_tracks=[])

        for track in media_info.get('audio_tracks', []):
            if track.track_type == "Audio":
                raw_data_np = self.audio_extractor.extract(input_path, track.to_data().get('stream_identifier'), SAMPLING_RATE)
                norm_flat_buffer = normalize_audio(raw_data_np)

                track = AudioTrack(
                    title=track.to_data().get('title'),
                    duration=track.to_data().get('duration'),
                    language=self.lang_detector.detect(norm_flat_buffer, self.silence_threshold),
                    channel_layout=track.to_data().get('channel_layout'),
                    silence_points=self.silence_detector.detect(norm_flat_buffer, self.silence_threshold, self.silence_duration),
                    is_muted=self.mute_detector.detect(norm_flat_buffer, self.silence_threshold)
                )
                
                audio_tracks.append(track)

        result_info.audio_tracks = audio_tracks
        return result_info

    def validate_mediainfo(self, media_info):
        if not media_info:
            raise ValueError("Invalid media info provided.")
        if len(media_info) == 0:
            raise ValueError("No audio tracks found in the media info.")
        return True
