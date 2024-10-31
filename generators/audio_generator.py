import torch
import numpy as np
from transformers import BarkModel, AutoProcessor, AutoTokenizer
from parler_tts import ParlerTTSForConditionalGeneration
import io
from scipy.io import wavfile
from pydub import AudioSegment

class AudioGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._initialize_models()

    def _initialize_models(self):
        # ParlerTTS for Speaker 1
        self.parler_model = ParlerTTSForConditionalGeneration.from_pretrained(
            "parler-tts/parler-tts-mini-v1").to(self.device)
        self.parler_tokenizer = AutoTokenizer.from_pretrained(
            "parler-tts/parler-tts-mini-v1")
        
        # Bark for Speaker 2
        self.bark_processor = AutoProcessor.from_pretrained("suno/bark")
        self.bark_model = BarkModel.from_pretrained(
            "suno/bark", 
            torch_dtype=torch.float16
        ).to(self.device)
        
        self.speaker1_description = """Laura's voice is expressive and dramatic in delivery, 
        speaking at a moderately fast pace with a very close recording that almost has no background noise."""

    def generate_speaker1_audio(self, text: str) -> tuple:
        input_ids = self.parler_tokenizer(
            self.speaker1_description, 
            return_tensors="pt"
        ).input_ids.to(self.device)
        
        prompt_input_ids = self.parler_tokenizer(
            text, 
            return_tensors="pt"
        ).input_ids.to(self.device)
        
        generation = self.parler_model.generate(
            input_ids=input_ids, 
            prompt_input_ids=prompt_input_ids
        )
        audio_arr = generation.cpu().numpy().squeeze()
        return audio_arr, self.parler_model.config.sampling_rate

    def generate_speaker2_audio(self, text: str) -> tuple:
        inputs = self.bark_processor(
            text, 
            voice_preset="v2/en_speaker_6"
        ).to(self.device)
        
        speech_output = self.bark_model.generate(
            **inputs, 
            temperature=0.9, 
            semantic_temperature=0.8
        )
        audio_arr = speech_output[0].cpu().numpy()
        return audio_arr, 24000  # Bark sampling rate

    @staticmethod
    def numpy_to_audio_segment(audio_arr: np.ndarray, sampling_rate: int) -> AudioSegment:
        audio_int16 = (audio_arr * 32767).astype(np.int16)
        byte_io = io.BytesIO()
        wavfile.write(byte_io, sampling_rate, audio_int16)
        byte_io.seek(0)
        return AudioSegment.from_wav(byte_io)

    def generate_podcast(self, transcript_data: list, output_file: str = "podcast.mp3"):
        final_audio = None
        
        for speaker, text in transcript_data:
            if speaker == "Speaker 1":
                audio_arr, rate = self.generate_speaker1_audio(text)
            else:
                audio_arr, rate = self.generate_speaker2_audio(text)
            
            audio_segment = self.numpy_to_audio_segment(audio_arr, rate)
            
            if final_audio is None:
                final_audio = audio_segment
            else:
                final_audio += audio_segment

        final_audio.export(
            output_file,
            format="mp3",
            bitrate="192k",
            parameters=["-q:a", "0"]
        )