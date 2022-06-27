import cv2
import numpy as np
import tensorflow as tf
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

def predict(img_path,model_path):
    test_pics = []
    imgs = []
    test_pics.append(img_path)
    for picpath in test_pics:
        img = cv2.imread(picpath)
        img = cv2.resize(img, (128, 128), cv2.INTER_AREA)
        img = img / 255.
        imgs.append(img)

    model = tf.keras.models.load_model(model_path)
    predict_ans= model.predict(np.array(imgs))
    print(predict_ans)
    print(np.argmax(model.predict(np.array(imgs)), axis=1))
    return np.argmax(model.predict(np.array(imgs)), axis=1)