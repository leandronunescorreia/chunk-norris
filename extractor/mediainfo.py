from pymediainfo import MediaInfo
from extractor import Extractor

class MediaInfoExtractor(Extractor):
    def extract(self, input_data: str):
        media_info = MediaInfo.parse(input_data)
        audio_tracks = []

        for track in media_info.tracks:
            if track.track_type == "Audio":
                audio_tracks.append(track)
                audio_tracks.append(track.to_data())

        return audio_tracks