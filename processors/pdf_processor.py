import PyPDF2
from typing import Optional
import os

class PDFProcessor:
    @staticmethod
    def validate_pdf(file_path: str) -> bool:
        if not os.path.exists(file_path):
            print(f"Error: File not found at path: {file_path}")
            return False
        if not file_path.lower().endswith('.pdf'):
            print("Error: File is not a PDF")
            return False
        return True

    def extract_text(self, file_path: str, max_chars: int = 100000) -> Optional[str]:
        if not self.validate_pdf(file_path):
            return None

        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                print(f"Processing PDF with {num_pages} pages...")

                extracted_text = []
                total_chars = 0

                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()

                    if total_chars + len(text) > max_chars:
                        remaining_chars = max_chars - total_chars
                        extracted_text.append(text[:remaining_chars])
                        print(f"Reached {max_chars} character limit at page {page_num + 1}")
                        break

                    extracted_text.append(text)
                    total_chars += len(text)
                    print(f"Processed page {page_num + 1}/{num_pages}")

                final_text = '\n'.join(extracted_text)
                print(f"\nExtraction complete! Total characters: {len(final_text)}")
                return final_text

        except PyPDF2.PdfReadError:
            print("Error: Invalid or corrupted PDF file")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return None

    def get_metadata(self, file_path: str) -> Optional[dict]:
        if not self.validate_pdf(file_path):
            return None

        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = {
                    'num_pages': len(pdf_reader.pages),
                    'metadata': pdf_reader.metadata
                }
                return metadata
        except Exception as e:
            print(f"Error extracting metadata: {str(e)}")
            return None

    def save_text(self, text: str, output_file: str = 'tmp/extracted_text.txt') -> str:
        os.makedirs("tmp", exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        return output_file