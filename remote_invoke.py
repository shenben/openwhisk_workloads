import requests
# import schedule
import time
import threading
API = "http://10.113.183.63:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/"
NameSpace ="wsk_exp/"
UrlSuff = API+NameSpace

def invoke(url = 'http://10.113.183.63:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/wsk_exp/primes',\
            payload = {"N":10}):
    headers = {'Content-Type': 'application/json'}
    
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=16, pool_maxsize=16, max_retries=16)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    for i in range(1):
        try:
            requests.packages.urllib3.disable_warnings()
            resp = session.post(url, json=payload, headers=headers, timeout=10)
            print(resp.text)
        except:
            print('error ', url)


apps=["primes", "http-endpoint", "json", "base64", "float_op", "pyaes", "matmult"]
dats={
    "float_op":{"N":10},
    "matmult":{"N":10},
    "primes":{"N":10},
    "http-endpoint":{},
    "json":{"coordinates": [
                {
                "x": 0.5813050260802741,
                "y": 0.7931966135795514,
                "z": 0.1257968906879401
                },
                {
                "x": 0.8393548652113877,
                "y": 0.8643427200877976,
                "z": 0.18909043576907159,
                }]},
    "base64":{"str1":"b1WM0Vx8Fegr2tu6jAmPJZ9aRcG4TEpYNyvfz5Q7DoqBUS3CHl","str2":"SwDLqvpr","TRIES":100 },
    "pyaes":{"length":10,"iteration":10}
}
threads = []
for i,app in enumerate(apps):
    url = UrlSuff+app
    payload=dats[app]
    thread = threading.Thread(target=invoke, args=(url,payload))
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()

