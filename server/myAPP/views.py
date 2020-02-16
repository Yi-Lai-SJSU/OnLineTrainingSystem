from django.shortcuts import render
from django.http import HttpResponse
from mysite.celery import train_model
from django_celery_results.models import TaskResult
from django.shortcuts import get_object_or_404

def train_Model(request):
    path = '/Volumes/data/Yi/2020Spring/295B/Online-training-system/server/media/training'
    result = train_model.delay(path)
    print(result)
    return HttpResponse(result)

def check_TrainingStatus(request):
    if request.method == 'GET':
        print(request)
        task_id = request.GET.get('task_id')
        print(task_id)
        try:
            task = TaskResult.objects.get(task_id=task_id)
            print("work done")
            return HttpResponse("yes")
        except TaskResult.DoesNotExist:
            print("not done")
            return HttpResponse("no")