class AudioTrack:
    title: str
    duration: float
    language: str
    channel_layout: str
    silence_points: list
    is_muted: bool

    def __init__(self, title: str, duration: float, language: str, channel_layout: str, silence_points: list, is_muted: bool):
        self.title = title
        self.duration = duration
        self.language = language
        self.channel_layout = channel_layout
        self.silence_points = silence_points
        self.is_muted = is_muted