from google.cloud import speech_v1 as speech
from google.oauth2 import service_account
import io
from pydub import AudioSegment
from pydub.utils import make_chunks
import os
from tqdm import tqdm
from modules.utils import convert_time

class Transcriber:
    def __init__(self, credentials_path, language_code):
        # Initialize the SpeechClient with credentials
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.client = speech.SpeechClient(credentials=credentials)
        self.language_code = language_code

    def transcribe(self, audio_file_path, speaker):
        # Ensure the directory for chunked audio exists
        os.makedirs("chunked/media", exist_ok=True)

        # Load the audio file
        audio = AudioSegment.from_mp3(audio_file_path)
        chunk_length_ms = 10000  # Duration of each audio chunk in milliseconds (10 seconds)
        chunks = make_chunks(audio, chunk_length_ms)
        full_transcript = []
        sound_threshold = -50  # dBFS threshold for considering a chunk as silent

        for i, chunk in tqdm(enumerate(chunks), desc="Transcribing audio"):
            # Skip silent chunks based on dBFS threshold
            if chunk.dBFS < sound_threshold:
                continue

            # Export the current chunk to a WAV file
            chunk_name = f'./chunked/{os.path.basename(audio_file_path)}_{i}.wav'
            print(f'Exporting {chunk_name}')
            chunk.export(chunk_name, format='wav')

            # Read the exported chunk for transcription
            with io.open(chunk_name, "rb") as audio_chunk_file:
                content = audio_chunk_file.read()
                recognition_audio = speech.RecognitionAudio(content=content)
                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=48000,
                    language_code=self.language_code,
                    enable_word_time_offsets=True,
                    use_enhanced=False)

                # Perform speech recognition on the chunk
                response = self.client.recognize(config=config, audio=recognition_audio)
                for result in response.results:
                    transcript = result.alternatives[0].transcript
                    start_time = convert_time(i * chunk_length_ms / 1000)  # Convert start time to a readable format
                    end_time = convert_time((i * chunk_length_ms + len(chunk)) / 1000)  # Convert end time to a readable format
                    transcript_entry = {'speaker': speaker, 'transcript': transcript, 'start_time': start_time, 'end_time': end_time}
                    print(transcript_entry)
                    full_transcript.append(transcript_entry)

                # Remove the temporary chunk file
                os.remove(chunk_name)

        return full_transcript
