import os
from dotenv import load_dotenv, dotenv_values

from app.chunk_norris import NorrisSetup, ChunkNorris
from common.output_format import *
import argparse

def main(args):
    load_dotenv()
    config = dotenv_values(".env")
    
    model_path = args.model_path if args.model_path is not None else config.get("MODEL_PATH", None)
    silence_threshold = args.silence_threshold if args.silence_threshold is not None else config.get("SILENCE_THRESHOLD", 0.5)
    silence_duration = args.silence_duration if args.silence_duration is not None else config.get("SILENCE_DURATION", 0.5)
    
    info_extractor = args.info_extractor if args.info_extractor is not None else config.get("INFO_EXTRACTOR", None)
    audio_extractor = args.audio_extractor if args.audio_extractor is not None else config.get("AUDIO_EXTRACTOR", None)
    lang_detector = args.lang_detector if args.lang_detector is not None else config.get("LANG_DETECTOR", None)
    silence_detector = args.silence_detector if args.silence_detector is not None else config.get("SILENCE_DETECTOR", None)
    muted_track = args.muted_detector if args.muted_detector is not None else config.get("MUTED_DETECTOR", None)
    output_format = args.format if args.format is not None else config.get("OUTPUT_FORMAT", "json")

    norris_setup = NorrisSetup(
        model_path=model_path,
        silence_threshold=silence_threshold,
        silence_duration=silence_duration,
        info_extractor=info_extractor,
        audio_extractor=audio_extractor,
        lang_detector=lang_detector,
        silence_detector=silence_detector,
        mute_detector=muted_track
    )

    chunk_norris = ChunkNorris(setup=norris_setup)
    result = chunk_norris.run(input_path=args.input)
    process_output(result, output_format, args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chunk Norris CLI")
    parser.add_argument("--input", "-i", required=True, help="Input file path")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    parser.add_argument("--format", "-f", required=True, help="Output format (e.g., 'json', 'csv', 'txt')")
    parser.add_argument("--model-path", "-m", help="Path to the model")
    parser.add_argument("--silence-threshold", "-st", type=float, help="Silence threshold value")
    parser.add_argument("--silence-duration", "-sd", type=float, help="Silence duration value")
    parser.add_argument("--info-extractor", "-ie", help="Info extractor module")
    parser.add_argument("--audio-extractor", "-ae", help="Audio extractor module")
    parser.add_argument("--lang-detector", "-ld", help="Language detector module")
    parser.add_argument("--silence-detector", "-sdt", help="Silence detector module")
    parser.add_argument("--muted-detector", "-mdt", help="Muted Track detector module")
    
    args = parser.parse_args()

    main(args)