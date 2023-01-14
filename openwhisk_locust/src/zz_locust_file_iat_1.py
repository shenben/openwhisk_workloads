import random
from locust import HttpUser, task, tag, between
import base64
import os
from pathlib import Path
import logging
import numpy as np
import time
import json

random.seed(time.time())

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

data_dir  = Path('/mnt/faas_data')    # for docker usage
image_dir = data_dir / 'image_process_base64'
video_dir = data_dir / 'video_process_base64'

image_data = {}
image_names = []
mobilenet_names = []

# logging.basicConfig(level=logging.INFO,
#                     # filename='/mnt/locust_log/locust_openwhisk_log.txt',
#                     # filemode='w+',
#                     format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logging.basicConfig(level=logging.INFO)

for img in os.listdir(str(image_dir)):
    full_path = image_dir / img
    image_names.append(img)
    with open(str(full_path), 'r') as f:
        image_data[img] = f.read()

video_data = {}
video_names = []

for video in os.listdir(str(video_dir)):
    full_path = video_dir / video
    video_names.append(video)
    with open(str(full_path), 'r') as f:
        video_data[video] = f.read()

# get through: wsk -i  property get --auth
auth_str = '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'
pwd_1, pwd_2 = auth_str.strip().split(':')
auth = (pwd_1, pwd_2)

lr_review_words = ["fine", "fancy", "food", "good", "so so", 
    "bad", "blabla", "brain", "wave", "rees", "reversed", 
    "ecg", "tao", "lee", "emmm", 
    "tian.ri.zhao.zhao", "ugly", "disgusting", "wu.ya", 
    "zuo.you.heng.tiao"]

mean_iat = 1  # seconds
intervals = np.random.exponential(scale=mean_iat, size=5000)

def compose_lr_review_text():
    global lr_review_words
    return ' '.join(lr_review_words)
    # l = random.randint(20, 100)
    # text = ""
    # for i in range(0, l):
    #     text += random.choice(lr_review_words) + ' '
    # return text

class OpenWhiskUser(HttpUser):
    # wait_time = between(5, 9)
    # return wait time in second
    def wait_time(self):
        global intervals
        global mean_iat
        return np.random.exponential(scale=mean_iat)
        # return random.choice(intervals)
        # self.last_wait_time += 1
        # return self.last_wait_time

    @task
    @tag('image_process')
    def image_process(self):
        params = {}
        # params['blocking'] = 'true'
        # params['result'] = 'true'

        url = '/api/v1/namespaces/_/actions/image_process'
        # img = random.choice(image_names)
        img = 'b64_building.jpg'
        body = {}
        body['image'] = image_data[img]

        r = self.client.post(url, params=params,
            json=body, auth=auth, verify=False,
            name="/image_process")
        if r.status_code > 202:
            logging.warning('image_process resp.status = %d, text=%s' %(r.status_code,
                r.text))
        try:
            aid = json.loads(r.text)['activationId']
            logging.info('aid--image_process:%s' %aid)
        except:
            logging.error('image_process response json parsing error')


    @task
    @tag('mobilenet')
    def mobilenet(self):
        params = {}
        # params['blocking'] = 'true'
        # params['result'] = 'true'

        url = '/api/v1/namespaces/_/actions/mobilenet'
        # img = random.choice(image_names)
        img = 'b64_building.jpg'
        body = {}
        body['image'] = image_data[img]
        body['format'] = img.split('.')[-1]

        r = self.client.post(url, params=params,
            json=body, auth=auth, verify=False,
            name='/mobilenet')
        if r.status_code > 202:
            logging.warning('mobilenet resp.status = %d, text=%s' %(r.status_code,
                r.text))
        # logging.info('resp.text=%s' %r.text)
        try:
            aid = json.loads(r.text)['activationId']
            logging.info('aid--mobilenet:%s' %aid)
        except:
            logging.error('mobilenet response json parsing error')

    @task
    @tag('video_process')
    def video_process(self):
        params = {}
        # params['blocking'] = 'true'
        # params['result'] = 'true'

        url = '/api/v1/namespaces/_/actions/video_process'

        # video = random.choice(video_names)
        video = 'b64_lion-sample.avi'
        body = {}
        body['video'] = video_data[video]
        body['video_name'] = video

        r = self.client.post(url, params=params,
            json=body, auth=auth, verify=False,
            name='/video_process')

        if r.status_code > 202:
            logging.warning('video_process resp.status = %d, text=%s' %(r.status_code,
                r.text))

        try:
            aid = json.loads(r.text)['activationId']
            logging.info('aid--video_process:%s' %aid)
        except:
            logging.error('video_process response json parsing error')

    @task
    @tag('lr_review')
    def lr_review(self):
        params = {}
        # params['blocking'] = 'true'
        # params['result'] = 'true'

        url = '/api/v1/namespaces/_/actions/lr_review'
        body = {}
        body["text"] = compose_lr_review_text()

        r = self.client.post(url, params=params,
            json=body, auth=auth, verify=False,
            name='/lr_review')

        if r.status_code > 202:
            logging.warning('lr_review resp.status = %d, text=%s' %(r.status_code,
                r.text))

        try:
            aid = json.loads(r.text)['activationId']
            logging.info('aid--lr_review:%s' %aid)
        except:
            logging.error('lr_review response json parsing error')


    @task
    @tag('chameleon')
    def chameleon(self):
        params = {}
        # params['blocking'] = 'true'
        # params['result'] = 'true'

        url = '/api/v1/namespaces/_/actions/chameleon'
        body = {}
        # body['rows'] = random.randint(200, 1000)
        # body['cols'] = random.randint(200, 1000)
        body['rows'] = 500
        body['cols'] = 500

        r = self.client.post(url, params=params,
            json=body, auth=auth, verify=False,
            name='/chameleon')

        if r.status_code > 202:
            logging.warning('chameleon resp.status = %d, text=%s' %(r.status_code,
                r.text))

        try:
            aid = json.loads(r.text)['activationId']
            logging.info('aid--chameleon:%s' %aid)
        except:
            logging.error('chameleon response json parsing error')

    @task
    @tag('float_op')
    def float_op(self):
        params = {}
        # params['blocking'] = 'true'
        # params['result'] = 'true'

        url = '/api/v1/namespaces/_/actions/float_op'
        body = {}
        # body['N'] = random.randint(500000, 5000000)
        body['N'] = 2500000

        r = self.client.post(url, params=params,
            json=body, auth=auth, verify=False,
            name='/float_op')

        if r.status_code > 202:
            logging.warning('float_op resp.status = %d, text=%s' %(r.status_code,
                r.text))

        try:
            aid = json.loads(r.text)['activationId']
            logging.info('aid--float_op:%s' %aid)
        except:
            logging.error('float_op response json parsing error')

    @task
    @tag('linpack')
    def linpack(self):
        params = {}
        # params['blocking'] = 'true'
        # params['result'] = 'true'

        url = '/api/v1/namespaces/_/actions/linpack'
        body = {}
        # body['N'] = random.randint(30, 150)
        body['N'] = 75

        r = self.client.post(url, params=params,
            json=body, auth=auth, verify=False,
            name='/linpack')

        if r.status_code > 202:
            logging.warning('linpack resp.status = %d, text=%s' %(r.status_code,
                r.text))

        try:
            aid = json.loads(r.text)['activationId']
            logging.info('aid--linpack:%s' %aid)
        except:
            logging.error('linpack response json parsing error')

    @task
    @tag('matmult')
    def matmult(self):
        params = {}
        # params['blocking'] = 'true'
        # params['result'] = 'true'

        url = '/api/v1/namespaces/_/actions/matmult'
        body = {}
        # body['N'] = random.randint(10, 200)
        body['N'] = 100

        r = self.client.post(url, params=params,
            json=body, auth=auth, verify=False,
            name='/matmult')

        if r.status_code > 202:
            logging.warning('matmult resp.status = %d, text=%s' %(r.status_code,
                r.text))

        try:
            aid = json.loads(r.text)['activationId']
            logging.info('aid--matmult:%s' %aid)
        except:
            logging.error('matmult response json parsing error')


    @task
    @tag('pyaes')
    def pyaes(self):
        params = {}
        # params['blocking'] = 'true'
        # params['result'] = 'true'

        url = '/api/v1/namespaces/_/actions/pyaes'
        body = {}
        # body['length'] = random.randint(100, 1000)
        # body['iteration'] = random.randint(50, 500)
        body['length'] = 500
        body['iteration'] = 250

        r = self.client.post(url, params=params,
            json=body, auth=auth, verify=False,
            name='/pyaes')

        if r.status_code > 202:
            logging.warning('pyaes resp.status = %d, text=%s' %(r.status_code,
                r.text))

        try:
            aid = json.loads(r.text)['activationId']
            logging.info('aid--pyaes:%s' %aid)
        except:
            logging.error('pyaes response json parsing error')

