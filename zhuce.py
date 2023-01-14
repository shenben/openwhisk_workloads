# register some apps that does not need additional docker environment
# apps are from openwhisk_workloads
import os
import sys
import subprocess
from pathlib import Path

top_dir = Path.cwd() / 'functions'

def invoke_wsk():
    cmd = 'wsk action invoke float_op -i -p N 10 -r'
    subprocess.call(cmd, shell=True)

    cmd = 'wsk action invoke base64 -i -p str1 b1WM0Vx8Fegr2tu6jAmPJZ9aRcG4TEpYNyvfz5Q7DoqBUS3CHl -p str2 SwDLqvpr -p TRIES 100 -r'
    subprocess.call(cmd, shell=True)
    
    os.chdir(str(top_dir / 'microbenchmarks'/'json'))
    cmd = 'wsk action invoke json -i -P 1.json -r'
    subprocess.call(cmd, shell=True)
    
    cmd = 'wsk action invoke http-endpoint -i -p N 10 -r'
    subprocess.call(cmd, shell=True)

    cmd = 'wsk action invoke primes -i -p N 10 -r'
    subprocess.call(cmd, shell=True)

    cmd = 'wsk action invoke matmult -i -p N 10 -r'
    subprocess.call(cmd, shell=True)

    cmd = 'wsk action invoke pyaes -i -p length 10 -p iteration 10 -r'
    subprocess.call(cmd, shell=True)

def invoke_api():
    cmd = "curl http://172.17.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/wsk_exp/base64 " + \
        '-X GET -H "Content-Type: application/json" '+ \
        '-d \'{"str1":"b1WM0Vx8Fegr2tu6jAmPJZ9aRcG4TEpYNyvfz5Q7DoqBUS3CHl","str2":"SwDLqvpr","TRIES":"100" }\' '
    subprocess.call(cmd, shell=True)
    cmd = "curl http://172.17.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/wsk_exp/pyaes " + \
        '-X GET -H "Content-Type: application/json" '+ \
        '-d \'{"length":10,"iteration":10}\' '
    subprocess.call(cmd, shell=True)
    cmd = 'curl  http://172.17.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/wsk_exp/float_op?N=10'
    subprocess.call(cmd, shell=True)
    cmd = 'curl  http://172.17.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/wsk_exp/http-endpoint'
    subprocess.call(cmd, shell=True)
    os.chdir(str(top_dir / 'microbenchmarks'/'json'))
    cmd = 'curl -X POST -H "Content-Type: application/json" -d @1.json http://172.17.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/wsk_exp/json'
    subprocess.call(cmd, shell=True)
    cmd = 'curl  http://172.17.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/wsk_exp/primes?N=10'
    subprocess.call(cmd, shell=True)
    cmd = "curl http://172.17.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/wsk_exp/matmult " + \
        '-X GET -H "Content-Type: application/json" '+ \
        '-d \'{"N":10}\' '
    subprocess.call(cmd, shell=True)

def create_api():
    os.chdir(str(top_dir / 'matmult'))
    cmd = 'wsk action create matmult matmult.py --docker yz2297/python3_openwhisk --web true --memory 512 -i'
    subprocess.call(cmd, shell=True)

    os.chdir(str(top_dir / 'pyaes'))
    cmd = 'wsk action create pyaes faas_pyaes.py --docker yz2297/pyaes_openwhisk --web true -i'
    subprocess.call(cmd, shell=True)

    os.chdir(str(top_dir / 'float_operation'))
    cmd = 'wsk action create float_op float_operation.py --web true -i'
    subprocess.call(cmd, shell=True)


    os.chdir(str(top_dir / 'microbenchmarks'/'base64'))
    cmd = 'wsk action create base64 base64-python.py --web true -i'
    subprocess.call(cmd, shell=True)

    os.chdir(str(top_dir / 'microbenchmarks'/'json'))
    cmd = 'wsk action create json json-python.py --web true -i'
    subprocess.call(cmd, shell=True)

    
    os.chdir(str(top_dir / 'microbenchmarks'/'http-endpoint'))
    cmd = 'wsk action create http-endpoint http-endpoint-python.py --web true -i'
    subprocess.call(cmd, shell=True)

    
    os.chdir(str(top_dir / 'microbenchmarks'/'primes'))
    cmd = 'wsk action create primes primes-python.py --web true -i'
    subprocess.call(cmd, shell=True)

    cmd = " wsk action list -i | awk '{print $1}' "
    res = subprocess.check_output(cmd,shell=True)
    res = res.decode()
    res = res.split('\n')[1:-1]
    
    for i in res:
        app = i.replace("/guest/","")
        for meth in ["get","post"]:
            cmd ='wsk api create /wsk_exp /'+app +" " + meth +" "+app+' --response-type json -i'
            subprocess.call(cmd, shell=True)
            print(cmd)

    
def remove_api():
    cmd = " wsk action list -i | awk '{print $1}' "
    res = subprocess.check_output(cmd,shell=True)
    res = res.decode()
    res = res.split('\n')[1:-1]
    for i in res:
        try:
            i = i.replace("/guest/","")
            cmd = "wsk -i action delete "+i
            subprocess.call(cmd, shell=True)
        except:
            print(i,"error")

    cmd = "wsk -i api delete /wsk_exp"
    subprocess.call(cmd, shell=True)
    
remove_api()
create_api()
invoke_wsk()
invoke_api()



