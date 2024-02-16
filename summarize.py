import argparse
import os
from modules.speech import ChatGPT
from modules.Transcriber import Transcriber
from modules.utils import append_texts, save_report, save_transcript_to_file

# Supported languages and their codes
languages = {"english": "en-US", "korean": "ko-KR"}

def make_a_prompt(summary_path, gpt):
    prompt_path = 'resources/prompt.txt'
    full_prompt = append_texts(prompt_path, summary_path)
    result = gpt.prompt(full_prompt)
    print(result)
    save_report(result)

def main():
    parser = argparse.ArgumentParser(description="Transcribe and generate a prompt from audio files.")
    parser.add_argument('--teacher', type=str, default='media/teacher.mp3', help="Teacher's audio file path.")
    parser.add_argument('--student', type=str, default='media/student.mp3', help="Student's audio file path.")
    parser.add_argument('--language', type=str, default='korean', choices=languages.keys(), help="Language for transcription.")
    parser.add_argument('--example', action='store_true', help='Use this flag to run with an example text.')

    args = parser.parse_args()

    # Assertions for audio files and language
    assert args.teacher.endswith(('.mp3', '.wav')), "Teacher's audio file must be .mp3 or .wav"
    assert args.student.endswith(('.mp3', '.wav')), "Student's audio file must be .mp3 or .wav"
    assert args.language in languages, f"Unsupported language. Supported languages are: {', '.join(languages.keys())}"

    print('Loading GPT...')
    gpt = ChatGPT()
    print('GPT Loaded.')

    if args.example:
        print("Running prompt from example files...")
        make_a_prompt('conversations/test.txt', gpt)
    else:
        print('Loading transcriber...')
        transcriber = Transcriber(credentials_path='resources/sa.json', language_code=languages[args.language])
        print('Starting transcription for teacher audio...')
        teacher_output = transcriber.transcribe(args.teacher, 'Teacher')
        print('Teacher audio transcription finished.')
        print('Starting transcription for student audio...')
        student_output = transcriber.transcribe(args.student, 'Student')
        print('Student audio transcription finished.')

        full_transcript = teacher_output + student_output
        print('Transcription complete.')
        print(full_transcript)

        count_summaries = len(os.listdir('conversations'))
        file_path = f'conversations/conversation_summary_{count_summaries}.txt'
        save_transcript_to_file(full_transcript, file_path)
        make_a_prompt(file_path, gpt)

if __name__ == '__main__':
    main()