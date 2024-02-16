# summarizer
Summarize tutoring conversation between a teacher and student using audio files 

# Requirement
- Install required libraries with: `pip3 install -r requirements.txt`
- Set OpenAI API key with: `export OPENAI_API_KEY='You-API-Key'`
- Download Google speech API's credentials to `'resources/'` and rename it to 'sa.json'

# Running the code
- To run the code from examples (no audio but from text example): </br>
  `python3 summarize.py --example`
- To run the code with audio files:</br>
  `python3 summarize.py --teacher='path/to/audio.mp3' --student='path/to/audio.mp3' --language='Korean'`
