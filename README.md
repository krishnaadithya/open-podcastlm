# open-podcastlm
Convert any PDF into a podcast episode

Here's a comprehensive README.md and requirements.txt for your project.

# PDF to Podcast Converter

An AI-powered tool that converts PDF documents into engaging podcast-style conversations using advanced language models and text-to-speech technology.


## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-to-podcast
cd pdf-to-podcast
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Nebius API key:
```bash
export NEBIUS_API_KEY='your_api_key_here'
```

## Usage

```python
from main import main

# Convert a PDF to podcast
main("path/to/your/document.pdf")
```

## Project Structure

```
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

