from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
app = Celery('celery', broker='redis://127.0.0.1:6379/8')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

import tensorflow as tf
import numpy as np
from keras.preprocessing import image
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras.preprocessing.image import ImageDataGenerator

@app.task
def train_model(path):
    # path = '/Volumes/data/Yi/2020Spring/295B/Online-training-system/server/media/training'

    train_datagen = ImageDataGenerator(rescale=1. / 255,
                                       shear_range=0.2,
                                       zoom_range=0.2,
                                       horizontal_flip=True)

    training_set = train_datagen.flow_from_directory(path + '/classifiedImage/train',
                                                     target_size=(64, 64),
                                                     batch_size=32,
                                                     class_mode='categorical')
    print(training_set)
    nb_train_samples = len(training_set.filenames)
    print(nb_train_samples)
    num_classes = len(training_set.class_indices)
    print(num_classes)

    test_datagen = ImageDataGenerator(rescale=1. / 255)
    test_set = test_datagen.flow_from_directory(path + '/classifiedImage/test',
                                                target_size=(64, 64),
                                                batch_size=32,
                                                class_mode='categorical')
    print(test_set)
    nb_test_samples = len(test_set.filenames)
    print(nb_test_samples)
    num_classes = len(test_set.class_indices)
    print(num_classes)

    classifier = Sequential()
    classifier.add(Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    classifier.add(Conv2D(32, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    classifier.add(Conv2D(32, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    classifier.add(Flatten())
    classifier.add(Dense(units=128, activation='relu'))
    classifier.add(Dropout(0.1))
    classifier.add(Dense(units=num_classes, activation='softmax'))
    classifier.add(Dropout(0.1))
    classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    classifier.fit_generator(training_set,
                             steps_per_epoch=nb_train_samples,
                             epochs=1,
                             validation_data=test_set,
                             validation_steps=nb_test_samples)
    print(classifier.summary())
    print(training_set.class_indices)

    # for file_list in os.walk(path + '/classifiedImage/validation/spiders/'):
    #     for file_name in file_list:
    #         file_path = os.path.join(path, file_name)
    #         test_image = image.load_img(file_path, target_size=(64, 64))
    #         test_image = image.img_to_array(test_image)
    #         test_image = np.expand_dims(test_image, axis=0)
    #         result = classifier.predict(test_image)
    #         print(result)

    s = str(training_set.class_indices)
    f = open(path + '/keras-models/classLabel.txt', 'w')
    f.writelines(s)
    f.close()

    classifier.save(path + '/keras-models/keras.h5')
    model = tf.keras.models.load_model(path + '/keras-models/keras.h5')
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    open(path + '/tflite-models/converted_model.tflite', "wb").write(tflite_model)