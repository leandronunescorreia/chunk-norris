from pymediainfo import MediaInfo
from app.ports.extractor import Extractor

class MediaInfoExtractor(Extractor):

    def extract(self, input_data: str):
        media_info = MediaInfo.parse(input_data)


        result = {"audio_tracks": []}
        general = next((track for track in media_info.tracks if track.track_type == "General"), None)
        if general:
            duration_ms = general.duration
            hours = int(duration_ms // 3600000)
            minutes = int((duration_ms % 3600000) // 60000)
            seconds = int((duration_ms % 60000) // 1000)
            result = {
                "filename": general.complete_name,
                "duration": "{:02}:{:02}:{:02}".format(hours, minutes, seconds),
                "audio_tracks": []
            }

        for track in media_info.tracks:
            if track.track_type == "Audio":
                result["audio_tracks"].append(track)

        return result