from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from .models import Project, Video, Image
from rest_framework import viewsets
from .serializers import ProjectSerializer, VideoSerializer, ImageSerializer
from django.core import serializers
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser, FormParser


import json
import datetime
import time
import cv2

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class videoToFrames(View):
    def get(self, request):
        return render(request, 'upload.html')

    def post(self, request):
        print("POST received - return done")
        parser_classes = (MultiPartParser, FormParser, FileUploadParser)
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d-%H:%M:%S") + "-"
        print(timestamp)
        user = User.objects.get(id=1)
        project = Project.objects.get(id=1)
        uploaded_file = request.FILES['video']
        print(uploaded_file)

        locationOfVideos = settings.MEDIA_ROOT+"/training/videos/"
        locationOfFrames = settings.MEDIA_ROOT+"/training/images/"

        fs = FileSystemStorage(location=locationOfVideos)
        fs.save(timestamp+uploaded_file.name, uploaded_file)

        videoFile  = locationOfVideos+timestamp+uploaded_file.name
        outputFile = locationOfFrames

        video = Video(title = timestamp+uploaded_file.name,
                      description = "default",
                      location = locationOfVideos+timestamp+uploaded_file.name,
                      url = "http://127.0.0.1:8000/media/training/videos/"+timestamp+uploaded_file.name,
                      type = "unclassified",
                      user = user,
                      project = project)
        video.save()

        vc = cv2.VideoCapture(videoFile)
        c = 1
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            print('openerror!')
            rval = False

        timeF = 100  # 视频帧计数间隔次数
        while rval:
            rval, frame = vc.read()
            if c % timeF == 0:
                # print(2)
                cv2.imwrite(outputFile + timestamp + str(int(c / timeF)) + '.jpg', frame)

                title = timestamp + str(int(c / timeF)) + '.jpg'
                location = outputFile + title
                desciption = "default"
                type = "unclassified"
                url = "http://127.0.0.1:8000/media/training/images/"+title

                image = Image(title = title,
                              location = location,
                              url = url,
                              description = desciption,
                              type = type,
                              user = user,
                              project = project,
                              video = video,
                              isTrain=True)
                image.save()
            c += 1
            cv2.waitKey(1)
        vc.release()

        unclassifiedImages = Image.objects.filter(type="unclassified")
        json_list = []
        for image in unclassifiedImages:
            json_dict = {}
            json_dict['id'] = image.id
            json_dict['title'] = image.title
            json_dict['url'] = image.url
            json_dict['description'] = image.description
            json_list.append(json_dict)
        return HttpResponse(json.dumps(json_list), content_type="application/json")