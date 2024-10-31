from typing import List
from llama_index.core.node_parser import TokenTextSplitter

class TextProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def create_word_bounded_chunks(self, text: str, target_chunk_size: int) -> List[str]:
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            word_length = len(word) + 1
            if current_length + word_length > target_chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def read_file(self, filename: str):
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as file:
                    content = file.read()
                print(f"Successfully read file using {encoding} encoding.")
                return content
            except UnicodeDecodeError:
                continue
            except FileNotFoundError:
                print(f"Error: File '{filename}' not found.")
                return None
            except IOError:
                print(f"Error: Could not read file '{filename}'.")
                return None

        print(f"Error: Could not decode file '{filename}' with any common encoding.")
        return None