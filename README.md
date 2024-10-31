# Open PodcastLM

## Overview

Open-PodcastLM is inspired by the NotebookLM and [NotebookLlama](https://github.com/meta-llama/llama-recipes/tree/main/recipes/quickstart/NotebookLlama). It transforms PDF documents into engaging podcast-style conversations using opensource language models and text-to-speech technology. The tool processes PDF content, generates natural dialogues, and creates high-quality audio output featuring two distinct voices.

Built with:
- [Meta LLaMA 3.1 8B, 405B](https://studio.nebius.ai/playground?models=meta-llama%2FMeta-Llama-3.1-405B-Instruct) via [Nebius AI Studio](https://studio.nebius.ai/)
- [ParlerTTS](https://huggingface.co/parler-tts/parler-tts-mini-v1) for Host Voice
- [Bark](https://huggingface.co/suno/bark) for Guest Voice

# Features

- **Intelligent PDF Processing:** Advanced text extraction and cleaning
- **Natural Dialogue Generation:** Creates engaging conversations between host and guest
- **Dual Voice System:** Distinct voices for host and guest using state-of-the-art TTS models
- **High-Quality Audio:** Professional-grade audio output with natural speech patterns

## Installation

1. Clone the repository:
```bash
git clone https://github.com/krishnaadithya/open-podcastlm.git
cd open-podcastlm
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Nebius API key:
```bash
export NEBIUS_API_KEY='your_api_key_here'
```

Command Line Arguments
--pdf, -p: Path to the input PDF file (required)
--output, -o: Output audio file path (default: output.mp3)

## Usage

```bash
python main.py --pdf path/to/document.pdf --output podcast.mp3
```

## Result:

[Listen to Sample Generated Podcast](https://github.com/krishnaadithya/open-podcastlm/blob/main/asset/gen_podcast.mp3)

## Project Structure

```bash
├── src/
│   ├── processors/
│   │   ├── text_processor.py
│   │   └── pdf_processor.py
│   ├── generators/
│   │   └── audio_generator.py
│   ├── clients/
│   │   └── llm_client.py
│   └── main.py
├── assets/
├── tmp/
├── README.md
└── requirements.txt
```

## Components

- **PDFProcessor**: Handles PDF text extraction
- **TextProcessor**: Cleans and formats extracted text
- **LLMClient**: Manages API interactions with LLaMA models
- **AudioGenerator**: Generates podcast audio using dual TTS engines

## Configuration

The system uses two different TTS models:
- ParlerTTS for Speaker 1 (Main host)
- Bark for Speaker 2 (Guest)

## Requirements
- CUDA-compatible GPU recommended
- Nebius API access

## License
MIT License

