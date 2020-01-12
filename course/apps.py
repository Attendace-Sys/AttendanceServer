from django.apps import AppConfig
# from keras.models import load_model
import os
import sys
# import tensorflow as tf
# from keras.models import model_from_json
# from course.inception_resnet_v1 import *


class CourseConfig(AppConfig):
    name = 'course'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        # you must import your modules here 
        # to avoid AppRegistryNotReady exception 
        # startup code here
        # # load keras model
        '''global keras_model
        global graph
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # keras_model = model_from_json(open(BASE_DIR + "/course/facenet_model.json", "r").read())
        keras_model = InceptionResNetV1()

        #https://drive.google.com/file/d/1971Xk5RwedbudGgTIrGAL4F7Aifu7id1/view?usp=sharing
        keras_model.load_weights(BASE_DIR + '/course/facenet_weights.h5')

        # keras_model = load_model(BASE_DIR + '/course/facenet_keras.h5')
        graph = tf.get_default_graph()'''
