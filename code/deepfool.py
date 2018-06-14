# -*- coding: utf-8 -*-

import numpy as np
from keras.preprocessing import image
from keras.applications import inception_v3
from keras import backend as K
from PIL import Image
import matplotlib.pyplot as plt
from sklearn import datasets
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Conv1D,GlobalMaxPooling1D,Activation,Input,MaxPooling1D,Flatten,concatenate,Embedding
from sklearn.preprocessing import MinMaxScaler

"""
pip install keras==2.1.5
pip install tensorflow==1.4
pip install Pillow
pip install h5py
"""

"""
公式生成图片
https://www.codecogs.com/latex/eqneditor.php
"""

def deepfool():
    model = inception_v3.InceptionV3()


    print(model.trainable)

    #设置模型参数不可训练 不影响反向传递
    model.trainable = False

    model_input_layer = model.layers[0].input
    model_output_layer = model.layers[-1].output

    object_type_to_fake = 859


    img = image.load_img("../picture/pig.jpg", target_size=(299, 299))
    original_image = image.img_to_array(img)

    original_image /= 255.
    original_image -= 0.5
    original_image *= 2.

    original_image = np.expand_dims(original_image, axis=0)


    max_change_above = original_image + 0.01
    max_change_below = original_image - 0.01


    hacked_image = np.copy(original_image)


    cost_function = model_output_layer[0, object_type_to_fake]


    gradient_function = K.gradients(cost_function, model_input_layer)[0]


    grab_cost_and_gradients_from_model = K.function([model_input_layer, K.learning_phase()], [cost_function, gradient_function])

    cost = 0.0

    #参考- Ian J. Goodfellow, Jonathon Shlens & Christian Szegedy，EXPLAINING AND HARNESSING ADVERSARIAL EXAMPLES，arXiv:1412.6572
    e = 0.007
    learning_rate = 0.1

    index=1
    while cost < 0.60:

        #set_learning_phase set_learning_phase() 设置训练模式/测试模式0或1
        cost, gradients = grab_cost_and_gradients_from_model([hacked_image, 0])

        # fast gradient sign method
        # EXPLAINING AND HARNESSING ADVERSARIAL EXAMPLES
        # hacked_image += gradients * learning_rate
        n = np.sign(gradients)
        hacked_image += n * e
        # print gradients

        hacked_image = np.clip(hacked_image, max_change_below, max_change_above)
        hacked_image = np.clip(hacked_image, -1.0, 1.0)

        print("batch:{} Cost: {:.8}%".format(index, cost * 100))
        index += 1

    img = hacked_image[0]
    img /= 2.
    img += 0.5
    img *= 255.

    im = Image.fromarray(img.astype(np.uint8))
    im.save("../picture/hacked-pig-image-deepfool.png")

def fgsm():
    model = inception_v3.InceptionV3()


    print(model.trainable)

    #设置模型参数不可训练 不影响反向传递
    model.trainable = False

    model_input_layer = model.layers[0].input
    model_output_layer = model.layers[-1].output

    object_type_to_fake = 859


    img = image.load_img("../picture/pig.jpg", target_size=(299, 299))
    original_image = image.img_to_array(img)

    original_image /= 255.
    original_image -= 0.5
    original_image *= 2.

    original_image = np.expand_dims(original_image, axis=0)


    max_change_above = original_image + 0.01
    max_change_below = original_image - 0.01


    hacked_image = np.copy(original_image)
    img_x0= np.copy(original_image)


    cost_function = model_output_layer[0, object_type_to_fake]


    gradient_function = K.gradients(cost_function, model_input_layer)[0]


    grab_cost_and_gradients_from_model = K.function([model_input_layer, K.learning_phase()], [cost_function, gradient_function])

    cost = 0.0

    #参考- Ian J. Goodfellow, Jonathon Shlens & Christian Szegedy，EXPLAINING AND HARNESSING ADVERSARIAL EXAMPLES，arXiv:1412.6572
    e = 0.007
    learning_rate = 0.1

    index=1
    while cost < 0.60:

        #set_learning_phase set_learning_phase() 设置训练模式/测试模式0或1
        cost, gradients = grab_cost_and_gradients_from_model([hacked_image, 0])

        # fast gradient sign method
        # EXPLAINING AND HARNESSING ADVERSARIAL EXAMPLES
        # hacked_image += gradients * learning_rate
        n = np.sign(gradients)
        hacked_image += n * e
        # print gradients

        hacked_image = np.clip(hacked_image, max_change_below, max_change_above)
        hacked_image = np.clip(hacked_image, -1.0, 1.0)

        print("batch:{} Cost: {:.8}%".format(index, cost * 100))
        index += 1

    img = hacked_image[0]




    img /= 2.
    img += 0.5
    img *= 255.

    im = Image.fromarray(img.astype(np.uint8))
    im.save("../picture/hacked-pig-image-fgsm.png")


def  get_change_picture(x0_file,x1_file,out):

    x0_img = image.load_img(x0_file, target_size=(299, 299))
    x0 = image.img_to_array(x0_img)

    x1_img = image.load_img(x1_file, target_size=(299, 299))
    x1 = image.img_to_array(x1_img)

    d=x1-x0

    print(d)

    im = Image.fromarray(d.astype(np.uint8))
    im.save(out)

    return d



if __name__ == '__main__':
    #fgsm()

    get_change_picture("../picture/pig.jpg","../picture/hacked-pig-image-fgsm.png","../picture/hacked-pig-image-fgsm-d.png")