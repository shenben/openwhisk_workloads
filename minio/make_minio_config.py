import sys
import os
import json

minio_config = {}
minio_config['endpoint'] = '172.17.0.8:9000' # ath-5
minio_config['access_key'] = 'zFE3frmjIeGtC-f_aimhUkn9ARiIm2HrkM1haFV4Mqw'
minio_config['secret_key'] = '756c222f96e27b3c85e8e703cf206fa900dce3e55ef32516bbed18136dbca23a'
minio_config['bucket'] = '166091a575b8640156a20993d48594689c3f51bd07f298f9e97b2a89b99596cd'

with open('./minio_config.json', 'w+') as f:
    json.dump(minio_config, f, indent=4, sort_keys=True)