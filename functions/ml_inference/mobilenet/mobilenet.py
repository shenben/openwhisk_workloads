# surpress tensorflow warning 'Could not load dynamic library 'libcudart.so.10.1' 
# otherwise openwhisk treats it as error
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'    
import numpy as np
import tensorflow as tf
import time
from minio import Minio

def predict(img_path):
    start = time.time()
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=[224, 224])
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.keras.applications.mobilenet.preprocess_input(x[tf.newaxis,...])
    pretrained_model = tf.keras.applications.MobileNet()
    result = pretrained_model(x)
    tf.keras.backend.clear_session()
    ret_val = {}
    ret_val['latency'] = time.time() - start
    return ret_val

def main(params):
    endpoint = params['endpoint']
    access_key = params['access_key']
    secret_key = params['secret_key']
    bucket = params['bucket']

    minio_client = Minio(endpoint=endpoint,
                     access_key=access_key,
                     secret_key=secret_key,
                     secure=False)
    found = minio_client.bucket_exists(bucket)
    if not found:
        print("Bucket '%s' does not exist" %bucket)

    image_name = params['image']
    image_path = '/tmp/' + image_name

    minio_client.fget_object(bucket_name=bucket,
                       object_name=image_name,
                       file_path=image_path)
     
    return predict(image_path)

# tp={
#     "endpoint": "s3.ap-east-1.amazonaws.com",
#     "access_key": "AKIA3VGEFMSCA6L6AEXA",
#     "secret_key": "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",
#     "bucket": "bucket656056549",
#     "video": "720.avi",
#     "image": "drone.png"
# }
# print(main(tp))