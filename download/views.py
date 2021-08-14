# Create your views here.

# importing all the required modules
import sys
import threading
from pathlib import Path

from django.shortcuts import render
from pytube import *


# defining function
def youtube(request):
    # checking whether request.method is post or not
    def x():
        if request.method == 'POST':
            # getting link from frontend
            link = request.POST['link']

            def completed():
                print('Download Complete!')

            video = YouTube(link)

            # setting video resolution
            stream = video.streams.get_highest_resolution()

            def downloading(streaming, chunk, bytes_remaining):
                print(stream.title, ': ', str(round((1 - bytes_remaining / streaming.filesize) * 100, 3)), '% done...')

            video.register_on_progress_callback(downloading)

            # downloads video
            stream.download(filename=video.title + '.mp4', output_path=str(Path.home() / 'Downloads/Video'))

            # returning HTML page
            return render(request, 'home.html')

    y = threading.Thread(target=x)
    y.start()
    return render(request, 'home.html')
