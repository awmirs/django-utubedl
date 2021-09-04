# Create your views here.

# importing all the required modules
from datetime import timedelta
import threading
from pathlib import Path

from django.shortcuts import render
from pytube import *


# defining function
def information(request):
    # checking whether request.method is post or not
    # def x():
    if request.method == 'POST':
        # getting link from frontend
        link = request.POST['link']

        # create YouTube object with the provided link
        video = YouTube(link)

        # setting video resolution
        # stream = video.streams.get_highest_resolution()

        title = video.title
        thumbnail = video.thumbnail_url
        # video file size in Megabytes
        try:
            size = str(round(video.streams.get_highest_resolution().filesize / 1000000, 2)) + ' MB'
        except:
            size = 'An error occurred'
        length = str(timedelta(seconds=video.length))
        # def downloading(streaming, chunk, bytes_remaining):
        #     print(stream.title, ': ', str(round((1 - bytes_remaining / streaming.filesize) * 100, 3)), '% done...')
        #
        # video.register_on_progress_callback(downloading)
        #
        # # downloads video
        # stream.download(filename=video.title + '.mp4', output_path=str(Path.home() / 'Downloads/Video'))

        context = {
            'link': link,
            'title': title,
            'thumbnail': thumbnail,
            'size': size,
            'length': length
        }
        return render(request, 'information.html', context)

        # returning HTML page
    return render(request, 'information.html')

    # y = threading.Thread(target=x)
    # y.start()
    # return render(request, 'information.html')


def get_link(request):
    return render(request, 'home.html')


def download(request):
    if request.method == 'POST':
        link = request.POST['link']
        video = YouTube(link, on_complete_callback=lambda: print('Download Complete!'))
        video.streams.get_highest_resolution().download(filename=video.title + '.mp4', output_path=str(Path.home() / 'Downloads/Video'))
        return render(request, 'download.html')
    return render(request, 'download.html')
