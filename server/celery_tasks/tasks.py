from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8');
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator

@app.task
def train_mode(path):
    # path = '/Volumes/data/Yi/2020Spring/295B/Online-training-system/server/media/training'
    train_datagen = ImageDataGenerator(rescale=1. / 255,
                                       shear_range=0.2,
                                       zoom_range=0.2,
                                       horizontal_flip=True)
    training_set = train_datagen.flow_from_directory(path + '/classifiedImage/training',
                                                     target_size=(64, 64),
                                                     batch_size=16,
                                                     class_mode='categorical')
    print(training_set)
    nb_train_samples = len(training_set.filenames)
    print(nb_train_samples)
    num_classes = len(training_set.class_indices)
    print(num_classes)

    test_datagen = ImageDataGenerator(rescale=1. / 255)
    test_set = test_datagen.flow_from_directory(path + '/classifiedImage/testing',
                                                target_size=(64, 64),
                                                batch_size=16,
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
    classifier.add(Dense(units=num_classes, activation='softmax'))
    classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    classifier.fit_generator(training_set,
                             steps_per_epoch=nb_train_samples,
                             epochs=1,
                             validation_data=test_set,
                             validation_steps=nb_test_samples)
    print(classifier.summary())

    classifier.save(path + '/keras-models/keras.h5')
    model = tf.keras.models.load_model(path + '/keras-models/keras.h5')
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    print("fore open...")
    open(path + '/tflite-models/converted_model.tflite', "wb").write(tflite_model)








