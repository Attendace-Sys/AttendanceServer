from django.apps import AppConfig
from keras.models import load_model
import os
import sys
import tensorflow as tf
class CourseConfig(AppConfig):
    name = 'course'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        # you must import your modules here 
        # to avoid AppRegistryNotReady exception 
        # startup code here
        # # load keras model
        global keras_model
        global graph
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        keras_model = load_model(BASE_DIR + '/course/facenet_keras.h5')
        graph = tf.get_default_graph()


