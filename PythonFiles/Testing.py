import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model
import time

def start_predicting(rootpath):
    #Define Path
    model_path = f'{rootpath}/data_set1/models/model.h5'#'./models/model.h5'
    model_weights_path = f'{rootpath}/data_set1/models/weights.h5'#'./models/weights.h5'
    test_path = '../data_set1/data/alien_test'#'./data/alien_test'

    #Load the pre-trained models
    model = load_model(model_path)
    model.load_weights(model_weights_path)
    return model

#Define image parameters
img_width, img_height = 150, 150

#Prediction Function
def predict(file,model):
    x = load_img(file, target_size=(img_width,img_height))
    x = img_to_array(x)
    x = np.expand_dims(x, axis=0)
    array = model.predict(x)
    result = array[0]
    #print(result)
    answer = np.argmax(result)
    print(f'{file} --{answer}')
    

    return answer

#action_dict = {0:'InteractingWithComputer',1:'Photographing',2:'PlayingMusic',3:'RidingBike'}
#filename='D:/workspace/PycharmProjects/CaptionGeneration_MES/project/data_set2/data/train/RidingBike/action0229.jpg'
#model = start_predicting()
#result = predict(filename,model)
#print(action_dict[result])

