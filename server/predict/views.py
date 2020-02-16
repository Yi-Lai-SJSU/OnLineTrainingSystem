from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import tensorflow as tf
from keras.preprocessing import image
import numpy as np
import os

# Create your views here.
def predict_image(request):
    print("predict_image")
    path = "/Volumes/data/Yi/2020Spring/295B/Online-training-system/server/media/training/"
    new_model = tf.keras.models.load_model(path + 'keras-models/keras.h5')
    print(new_model)

    uploaded_file = request.FILES['image']
    # test_image = image.load_img(path + 'classifiedImage/testing/Beagle/3098-beagle.jpg',
    #                             target_size=(64, 64))

    test_image = image.load_img(uploaded_file, target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = new_model.predict(test_image)
    print(result)

    classIndex = np.argmax(result)
    print(classIndex)

    fr = open(path + 'keras-models/classLabel.txt', 'r+')
    dic = eval(fr.read())  # 读取的str转换为字典
    print(dic)
    fr.close()

    for key in dic:
        if (dic[key] == classIndex):
            print(key)
            return HttpResponse(key)

    return HttpResponse("unknown object")