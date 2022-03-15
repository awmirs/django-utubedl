from datetime import timedelta
from pathlib import Path

from django.shortcuts import render
from django.views import View
from pytube import *


class InformationView(View):
    template_name = "information.html"

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
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

        def progress(stream, _chunk, _file_handle, bytes_remaining):
            current = ((stream.filesize - bytes_remaining) / stream.filesize)
            percent = ('{0:.1f}').format(current * 100)
            # progress = int(50 * current)
            context['percentage'] = percent

        video.register_on_progress_callback(progress)

        try:
            video.streams.get_highest_resolution().download(filename=video.title + '.mp4',
                                                            output_path=str(Path.home() / 'Downloads/Video'))
        except:
            print("ERROR")

        # def downloading(streaming, chunk, bytes_remaining):
        #     print(stream.title, ': ', str(round((1 - bytes_remaining / streaming.filesize) * 100, 3)), '% done...')
        #
        # video.register_on_progress_callback(downloading)
        #
        # # downloads video
        # stream.download(filename=video.title + '.mp4', output_path=str(Path.home() / 'Downloads/Video'))
        return render(request, 'information.html', context)


class HomeView(View):

    def get(self, request):
        return render(request, 'home.html')


class DownloadView(View):
    template_name = "download.html"
    def get(self, request):
        return render(request, 'download.html')