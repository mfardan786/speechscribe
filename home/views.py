from moviepy.editor import *
import os
import uuid
import openai
from django.shortcuts import render
from django.http import JsonResponse
from pydub import AudioSegment

openai.api_key = "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"

def openai_request(filepath):
    transcript1 = {"text": "this is faizan mumtaz"}
    try:
        audio_file = open(filepath, "rb")
        # transcript = openai.Audio.translate("whisper-1", audio_file)
        return transcript1["text"]
    except Exception as e:
        return "There is some error"
    finally:
        os.remove(filepath)

def convert_to_mp3(filepath):
    if not filepath.endswith(".mp3"):
        try:
            audio_file = AudioSegment.from_file(filepath, format="")
            mp3_file = audio_file.export(f"upload/{str(uuid.uuid4())}.mp3", format="mp3")
            return openai_request(mp3_file.name)
        except Exception as e:
            return "There is some error"
        finally:
            os.remove(filepath)
    else:
        return openai_request(filepath)

def convert_to_audio(file):
    try:
        video = VideoFileClip(file)
        audio = video.audio
        filename = os.path.splitext(file)[0]
        audio_filename = f"{filename}.mp3"
        audio.write_audiofile(audio_filename)
        data = openai_request(audio_filename)
        return data
    except Exception as e:
        return "There is some error"
    finally:
        os.remove(file)

def index(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("video_audio")
        ext = os.path.splitext(uploaded_file.name)[1]
        if ext in ('.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a'):
            filename = f"upload/{str(uuid.uuid4())}+{uploaded_file.name}"
            with open(filename, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            transcript = convert_to_mp3(filename)
            return JsonResponse({"response": transcript})
        elif ext in ('.mp4', '.avi', '.mkv', '.wmv', '.mov', '.webm'):
            filename = f"video/{str(uuid.uuid4())}+{uploaded_file.name}"
            with open(filename, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            transcript = convert_to_audio(filename)
            return JsonResponse({"response": transcript})
        else:
            return JsonResponse({"response": "none"})
    return render(request, 'index.html')
