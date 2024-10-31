import os
import ast
from pdf_processor import PDFProcessor
from text_processor import TextProcessor
from llm_client import LLMClient
from audio_generator import AudioGenerator

nubius_key = "eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnb29nbGUtb2F1dGgyfDExODAyNDEyMDQ0MzAyMjcxNTY1OSIsInNjb3BlIjoib3BlbmlkIG9mZmxpbmVfYWNjZXNzIiwiaXNzIjoiYXBpX2tleV9pc3N1ZXIiLCJhdWQiOlsiaHR0cHM6Ly9uZWJpdXMtaW5mZXJlbmNlLmV1LmF1dGgwLmNvbS9hcGkvdjIvIl0sImV4cCI6MTg4ODAzNzc0MywidXVpZCI6ImQ0YzY0NzQ3LWNjMjAtNDdlMS04YzE1LWI1MzI1NzE3N2Y0YyIsIm5hbWUiOiJub3RlYm9va0xNIiwiZXhwaXJlc19hdCI6IjIwMjktMTAtMzBUMDY6NTU6NDMrMDAwMCJ9.sshRCRWx5volb8re9tpvieni3IS5eyyFMUFzex6fZUM"

def main(pdf_path):
    # Initialize components
    pdf_processor = PDFProcessor()
    text_processor = TextProcessor()
    llm_client = LLMClient(
        base_url="https://api.studio.nebius.ai/v1/",
        api_key= nubius_key #os.environ.get("NEBIUS_API_KEY")
    )
    audio_generator = AudioGenerator()

    print("Extracting Text .....")
    extracted_text = pdf_processor.extract_text(pdf_path)
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
    audio_generator.generate_podcast(transcript_data, "final_podcast.mp3")

if __name__ == "__main__":
    pdf_path = "No-on-33-Rental-Owners-Fact-Sheet-0724_c.pdf"
    main(pdf_path)