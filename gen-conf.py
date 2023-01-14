import os
import json
import pandas as pd
conf = json.loads(open('tc.json','r').read())
# conf=pd.read_json('tc.json')
application = 'video_process'
# print(conf)
# conf['instances']={}
copies = 50
# print(os.listdir('/home/emc_admin/openwhisk_workloads/openwhisk_locust/faas_data/video_process'))
da = ['grb_2.avi', 'dolbycanyon.avi', 'DLP_PART_2_768k.avi', '640.avi', 'lion-sample.avi', 'bird.avi', '720.avi', 'small.avi', 'cbw3.avi', 'P6090053.avi', 'drop.avi', '360.avi', 'star_trails.avi', 'video-sample.avi', 'flame.avi']
da = da * 4

tp={
    "endpoint": "s3.ap-east-1.amazonaws.com",
    "access_key": "AKIA3VGEFMSCA6L6AEXA",
    "secret_key": "VMLceiaC/Ho1Zh1rTvxXmmL+aqUyfWcZqJGIC8Wv",
    "bucket": "bucket656056549",
    "video": "720.avi",
    "image": "drone.png"
}
if not os.path.exists('data'):
    os.mkdir('data')
for i in range(0,copies):
    fnam='data/'+'%s-%d'%(application,i)+'.json'
    with open(fnam,'w') as f:
        tp["video"]=da[i]
        json.dump(tp, f, indent=4)

ins = conf['instances']
exp=ins['instance1'].copy()
for i in range(0,copies):
    app = '%s-%d'%(application,i)
    exp['application']=app
    exp['param_file']='data/'+app+'.json'
    idx = 'instance%d'%(i+1)
    ins[idx] = exp.copy()
  
# open('conf.json', 'w').write(json.dumps(conf))
# data = json.dumps(conf, sort_keys=True, indent=2)
# data = data.encode('utf-8').decode('unicode_escape')
# open('conf.json', 'w').write(data)
# print(ins["instance1"])
# print(exp)
with open("conf.json", "w") as write_file:
    json.dump(conf, write_file, indent=4)
print("Done writing PrettyPrinted JSON data into file with indent=4")
# conf.to_json('conf.json')