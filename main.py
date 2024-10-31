import os
import ast
import argparse
from processors.pdf_processor import PDFProcessor
from processors.text_processor import TextProcessor
from clients.llm_client import LLMClient
from generators.audio_generator import AudioGenerator

def setup_args():
    parser = argparse.ArgumentParser(description='Convert PDF to an engaging podcast conversation.')
    parser.add_argument('--pdf', '-p', type=str, required=True, help='Path to the input PDF file')
    parser.add_argument('--output', '-o', type=str, default='output.mp3', help='Output audio file path (default: output.mp3)')
    return parser.parse_args()


def main():

    args = setup_args()

    nubius_key = os.environ.get("NEBIUS_API_KEY")

    if not nubius_key:
        print("Error: NEBIUS_API_KEY environment variable not set")
        return

    # Initialize components
    pdf_processor = PDFProcessor()
    text_processor = TextProcessor()
    llm_client = LLMClient(
        base_url="https://api.studio.nebius.ai/v1/",
        api_key= nubius_key #os.environ.get("NEBIUS_API_KEY")
    )
    audio_generator = AudioGenerator()

    print("Extracting Text .....")
    extracted_text = pdf_processor.extract_text(args.pdf)
    if not extracted_text:
        return
    
    text_file = pdf_processor.save_text(extracted_text)

    print("Processing text")
    # Clean and process text
    cleaned_text = text_processor.read_file(text_file)
    if not cleaned_text:
        return

    # Generate podcast transcript
    system_prompts = LLMClient.get_system_prompts()
    
    # Clean text
    cleaned_transcript = llm_client.generate_response(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        system_prompt=system_prompts["cleaner"],
        user_prompt=cleaned_text,
        temperature = 0.7,
        max_tokens = 1024)


    # Generate initial transcript
    podcast_transcript = llm_client.generate_response(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct",
        system_prompt=system_prompts["transcript_writer"],
        user_prompt=cleaned_transcript,
        temperature = 1,
        max_tokens = 8126*2)

    # Rewrite transcript for TTS
    final_transcript = llm_client.generate_response(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct",
        system_prompt=system_prompts["transcript_rewriter"],
        user_prompt=podcast_transcript,
        temperature = 1,
        max_tokens = 8126*2)


    # Convert transcript string to list of tuples
    transcript_data = ast.literal_eval(final_transcript)

    # Generate audio
    audio_generator.generate_podcast(transcript_data, args.output)

if __name__ == "__main__":
    #pdf_path = "No-on-33-Rental-Owners-Fact-Sheet-0724_c.pdf"
    main()