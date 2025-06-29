# chunk-norris
Chunk Norris – The Audio Track vigilante

> "Silence? That’s illegal in this town."

Chunk Norris is an audio tool designed to analyze and process audio tracks accurately and efficiently. It is designed to identify silent tracks, and the primary language of non-silent tracks.


> “When Chunk Norris enters, even mute tracks start talking.”

## Setting Up the Environment

To create a conda environment named `chunk-norris` and install the required dependencies, follow these steps:

1. Open a terminal or command prompt.
2. Run the following commands:

```bash
# Create the conda environment
conda create --name chunk-norris python=3.9 -y

# Activate the environment
conda activate chunk-norris

# Install the requirements
pip install -r requirements.txt
```

Make sure you have the `requirements.txt` file in the same directory where you run the commands. This file should contain all the necessary dependencies for the project.


## Running the Chunk Norris CLI

To execute the Chunk Norris tool, use the following command:

```bash
python main.py --input <input_path> --output <output_path> [optional parameters]
```

### Required Parameters
- `--input` or `-i`: Path to the input file.
- `--output` or `-o`: Path to the output file.

### Optional Parameters
- `--model-path` or `-m`: Path to the model file.
- `--silence-threshold` or `-st`: Threshold value for detecting silence (float).
- `--silence-duration` or `-sd`: Minimum duration of silence to detect (float).
- `--info-extractor` or `-ie`: Module for extracting information.
- `--audio-extractor` or `-ae`: Module for extracting audio.
- `--lang-detector` or `-ld`: Module for detecting language.
- `--silence-detector` or `-sdt`: Module for detecting silence.
- `--muted-detector` or `-mdt`: Module for detecting muted tracks.

### Example Usage

```bash
python main.py --input example.mp4 --output output.json --silence-threshold 0.3 --silence-duration 0.5
```


# Chunk-Norris Facts


> “No silence escapes his ears.”


> “Chunk Norris once detected silence… and gave it a voice.”


> “He doesn’t listen to tracks — they confess.”



> “Chunk Norris doesn’t just detect languages ​​— he makes them reveal themselves out of fear.”



>Chunk Norris once stared at a 5.1 surround track...
>It downmixed itself into mono out of respect.


