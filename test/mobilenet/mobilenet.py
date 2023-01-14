import numpy as np
import tensorflow as tf
import time
import os
from minio import Minio

def predict(img_path):
    start = time.time()
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=[224, 224])
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.keras.applications.mobilenet.preprocess_input(x[tf.newaxis,...])
    pretrained_model = tf.keras.applications.MobileNet()
    result = pretrained_model(x)
    ret_val = {}
    ret_val['latency'] = time.time() - start
    return ret_val

def main():
    # endpoint = params['endpoint']
    # access_key = params['access_key']
    # secret_key = params['secret_key']
    # bucket = params['params']
    endpoint = '128.253.128.68:9002'
    access_key = '5VCTEQOQ0GR0NV1T67GN'
    secret_key = '8MBK5aJTR330V1sohz4n1i7W5Wv/jzahARNHUzi3'
    bucket = 'openwhisk'

    minio_client = Minio(endpoint=endpoint,
                     access_key=access_key,
                     secret_key=secret_key,
                     secure=False)
    found = minio_client.bucket_exists(bucket)
    if not found:
        print("Bucket '%s' does not exist" %bucket)
    
    img_dir = '/tmp/faas_data/image_process/'

    for img_name in os.listdir(img_dir):
        print(img_name)
        img_path = '/tmp/' + img_name
        minio_client.fget_object(bucket_name=bucket,
            object_name=img_name,
            file_path=img_path)
        print('minio fetch %s' %img_name)
        print(predict(img_path))

if __name__ == '__main__':
    main()