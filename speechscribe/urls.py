"""speechscribe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

# handler404 = 'home.views.custom_404_view'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home.urls")),
]


from django.core.files.storage import default_storage
from moviepy.editor import *
# from pydub import AudioSegment
import os
import uuid
import openai
from django.shortcuts import render

# def custom_404_view(request, exception):
#     return render(request, '404.html', status=404)

openai.api_key = "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"

def ConvertToText(filepath):
    audio_file= open(filepath, "rb")
    transcript = openai.Audio.translate("whisper-1", audio_file)
    return transcript

def ConvertToaudio(file):
    clip = VideoFileClip(file.temporary_file_path())
    audio_clip = clip.audio
    audio_file_name = f"{file.name.split('.')[0]}.mp3"
    audio_file_path = f"upload/{audio_file_name}"
    audio_clip.write_audiofile(file, codec='libmp3lame')
    # Close the clips
    clip.close()
    audio_clip.close()

    ConvertToText(audio_file_path)
# ConvertToaudio("sie.mp4")




# # Create your views here.
def index(request):
    if request.method == "POST":
        uploaded_file=request.FILES.get("video_audio")
        ext = os.path.splitext(uploaded_file)
        if ext in ('.mp3', '.wav', '.ogg', '.flac', '.aac'):
            filename=f"upload/{uploaded_file.name}"
            default_storage.save(filename,uploaded_file)
            with open(filename, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            ConvertToText(f"upload/{uploaded_file}")
        elif ext in ('.mp4', '.avi', '.mkv', '.wmv', '.mov'):
            ConvertToaudio(uploaded_file)
                # ConvertToAudio(filename)
       
# # # specify the input file path
# # input_path = 'path/to/input/file'

# # # get the file extension
# # _, ext = os.path.splitext(input_path)

# # # load the audio file
# # audio = AudioSegment.from_file(input_path, format=ext[1:])

# # # specify the output file path
# output_path = 'path/to/output/file.mp3'

# # convert the audio to MP3 format
# audio.export(output_path, format='mp3')





    return render(request,"index.html")