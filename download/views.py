# Create your views here.

# importing all the required modules
from pathlib import Path

from django.shortcuts import render
from pytube import *




# defining function
def youtube(request):
    # checking whether request.method is post or not
    if request.method == 'POST':
        # getting link from frontend
        link = request.POST['link']
        video = YouTube(link)

        # setting video resolution
        stream = video.streams.get_lowest_resolution()

        # downloads video
        stream.download(output_path=str(Path.home() / "Downloads"))

        # returning HTML page
        return render(request, 'utube.html')
    return render(request, 'utube.html')


def home(request):
    return render(request, 'home.html')
