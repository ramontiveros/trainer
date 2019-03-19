from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import time
from .models import Video

def index(request):
    return render(request, 'couch/index.html', { 'videos': Video.all})

def new(request):
    return render(request, 'couch/new.html')

def stream(request):
    return StreamingHttpResponse(gen(Video()),
                        content_type='multipart/x-mixed-replace; boundary=frame')

def record(request):
    return StreamingHttpResponse(gen(Video(time.strftime("%Y%m%d-%H%M%S") + ".mp4")),
                        content_type='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


