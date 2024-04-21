import tkinter as tk
import re
from youtube_transcript_api import YouTubeTranscriptApi
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

def extract_video_id(url):
    # Regular expression to find the video ID from the URL
    match = re.search(r'(?<=watch\?v=)[^&]+', url)
    if match:
        return match.group(0)
    else:
        return None

def get_video_transcript(video_id):
    try:
        # Retrieve the transcript of the video
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for transcript in transcript_list:
            if transcript.language_code == 'en':
                return ' '.join([line['text'] for line in transcript.fetch()])
        return None
    except Exception as e:
        print("An error occurred while fetching the transcript:", e)
        return None

def translate():
    url = entry1.get()
    video_id = extract_video_id(url)
    if video_id:
        transcript = get_video_transcript(video_id)
        if transcript:
            try:
                chunk_size = 4000  # Adjust the chunk size as needed
                translated_chunks = []
                for i in range(0, len(transcript), chunk_size):
                    chunk = transcript[i:i+chunk_size]
                    translated_chunk = GoogleTranslator(source='auto', target='gu').translate(chunk)
                    translated_chunks.append(translated_chunk)
                translated_text = ' '.join(translated_chunks)
                tts = gTTS(text=translated_text, lang='gu', slow=False)
                tts.save("translated_audio.mp3")
                os.system("translated_audio.mp3")
            except Exception as e:
                print("An error occurred during translation:", e)
        else:
            print("No transcript available for this video.")
    else:
        print("Invalid YouTube URL")

root = tk.Tk()
root.geometry("500x350")

label = tk.Label(root, text="YouTube Video Transcript Translator")
label.pack(pady=12, padx=10)

entry1 = tk.Entry(root, width=50)
entry1.pack(pady=12, padx=10)

button = tk.Button(root, text="Translate", command=translate)
button.pack(pady=12, padx=10)

root.mainloop()
