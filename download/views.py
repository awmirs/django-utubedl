# Create your views here.

# importing all the required modules
import threading
from datetime import timedelta
from pathlib import Path
from time import sleep

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
        title = video.title
        thumbnail = video.thumbnail_url
        # setting video resolution
        # stream = video.streams.get_highest_resolution()
        # video file size in Megabytes
        try:
            size = str(round(video.streams.get_highest_resolution().filesize / 1000000, 2)) + ' MB'
        except:
            size = 'An error occurred'
        length = str(timedelta(seconds=video.length))
        context = {
            'link': link,
            'title': title,
            'thumbnail': thumbnail,
            'size': size,
            'length': length
        }
        video.streams.get_highest_resolution().download()

        def progress(stream, _chunk, _file_handle, bytes_remaining):
            current = ((stream.filesize - bytes_remaining) / stream.filesize)
            percent = ('{0:.1f}').format(current * 100)
            # progress = int(50 * current)
            context['percentage'] = percent

        video.register_on_progress_callback(progress)


        # def downloading(streaming, chunk, bytes_remaining):
        #     print(stream.title, ': ', str(round((1 - bytes_remaining / streaming.filesize) * 100, 3)), '% done...')
        #
        # video.register_on_progress_callback(downloading)
        #
        # # downloads video
        # stream.download(filename=video.title + '.mp4', output_path=str(Path.home() / 'Downloads/Video'))


        return render(request, 'download.html', context)

        # returning HTML page
    return render(request, 'information.html')

    # y = threading.Thread(target=x)
    # y.start()
    # return render(request, 'information.html')


def get_link(request):
    return render(request, 'home.html')


def download(request):

    return render(request, 'download.html')
