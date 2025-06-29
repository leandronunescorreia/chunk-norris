class ResultInfo:
    filename: str
    duration: float
    audio_tracks: list
    audio_track_count: int

    def __init__(self, filename: str, duration: float, audio_tracks: list):
        self.filename = filename
        self.duration = duration
        self.audio_tracks = audio_tracks
        self.audio_track_count = len(audio_tracks) if audio_tracks else 0


    def to_dict(self):        return {
            "filename": self.filename,
            "duration": self.duration,
            "audio_tracks": [track.to_dict() for track in self.audio_tracks],
            "audio_track_count": self.audio_track_count
        }

    def to_json(self):
        import json
        return json.dumps(self.to_dict(), indent=4)

    def to_csv(self):
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["filename", "duration", "audio_track_count"])
        writer.writerow([self.filename, self.duration, self.audio_track_count])

        writer.writerow([])
        writer.writerow(["Audio Track Title", "Language", "Duration", "Sample Rate", "Bitrate"])
        for track in self.audio_tracks:
            writer.writerow([track.title, track.language, track.duration, track.sample_rate, track.bitrate])

        return output.getvalue()

    def to_txt(self):
        output = []
        output.append(f"Filename: {self.filename}")
        output.append(f"Duration: {self.duration} seconds")
        output.append(f"Audio Track Count: {self.audio_track_count}")
        output.append("Audio Tracks:")
        
        for track in self.audio_tracks:
            output.append(f"  - Title: {track.title}, Language: {track.language}, Duration: {track.duration} seconds, Sample Rate: {track.sample_rate} Hz, Bitrate: {track.bitrate} kbps")
        
        return "\n".join(output)

    def __str__(self):
        return f"ResultInfo(filename={self.filename}, duration={self.duration}, audio_track_count={self.audio_track_count})"    
    