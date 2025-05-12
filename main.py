import os
from dotenv import load_dotenv, dotenv_values

from app import chunk_norris
from app.chunk_norris import NorrisSetup
import argparse


def main(args):
    load_dotenv()
    config = dotenv_values(".env")
    
    model_path = args.model_path if args.model_path is not None else config.get("model_path", None)
    silence_threshold = args.silence_threshold if args.silence_threshold is not None else config.get("silence_threshold", 0.5)
    silence_duration = args.silence_duration if args.silence_duration is not None else config.get("silence_duration", 0.5)
    
    info_extractor = args.info_extractor if args.info_extractor is not None else config.get("info_extractor", None)
    audio_extractor = args.audio_extractor if args.audio_extractor is not None else config.get("audio_extractor", None)
    lang_detector = args.lang_detector if args.lang_detector is not None else config.get("lang_detector", None)
    silence_detector = args.silence_detector if args.silence_detector is not None else config.get("silence_detector", None)

    norris_setup = NorrisSetup(
        model_path=model_path,
        silence_threshold=silence_threshold,
        silence_duration=silence_duration,
        info_extractor=info_extractor,
        audio_extractor=audio_extractor,
        lang_detector=lang_detector,
        silence_detector=silence_detector
    )

    chunk_norris = chunk_norris.ChunkNorris(setup=norris_setup)
    chunk_norris.run(input_path=args.input, output_path=args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chunk Norris CLI")
    parser.add_argument("--input", "-i", required=True, help="Input file path")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    parser.add_argument("--model-path", "-m", help="Path to the model")
    parser.add_argument("--silence-threshold", "-st", type=float, help="Silence threshold value")
    parser.add_argument("--silence-duration", "-sd", type=float, help="Silence duration value")
    parser.add_argument("--info-extractor", "-ie", help="Info extractor module")
    parser.add_argument("--audio-extractor", "-ae", help="Audio extractor module")
    parser.add_argument("--lang-detector", "-ld", help="Language detector module")
    parser.add_argument("--silence-detector", "-sdt", help="Silence detector module")
    
    args = parser.parse_args()

    main(args)