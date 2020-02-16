from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import json
from videoToFrames.models import Image
import os
import shutil

class classifyImage(View):
    def post(self, request):
        print(request);
        received_json_data = json.loads(request.body)
        print(received_json_data)
        image = Image.objects.get(id=received_json_data['id'])
        if(image):
            image.type = received_json_data['type']
            # image.isTrain = True if received_json_data[data]['isTrain'] == 1 else False
            image.save()
            # move the image from unclassified folder to classified folder
            f_src = image.location;
            dst_path = "/Volumes/data/Yi/2020Spring/295B/Online-training-system/" \
                     "server/media/training/classifiedImage/training/" + image.type + "/"
            print(f_src);
            print(dst_path);
            try:
                if not os.path.exists(dst_path):
                    os.mkdir(dst_path)
                f_dst = os.path.join(dst_path+image.title)
                shutil.move(f_src, f_dst)
                image.location = f_dst
                image.url = "http://127.0.0.1:8000/media/training/" \
                            "classifiedImage/training/" + image.type + "/" + image.title
                image.save()
                print(image)
            except Exception as e:
                print('movie_file Error', e)
        return HttpResponse("ClassifyImage")




