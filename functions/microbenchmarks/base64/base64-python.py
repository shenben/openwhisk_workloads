# Copyright (c) 2019 Princeton University
# Copyright (c) 2014 'Konstantin Makarchev'
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import base64

def main(params):
    # STR_SIZE = 1000000
    # TRIES = 100
    # str1 = b"a" * STR_SIZE
    # str2 = b""
    str1 = str(params['str1'])
    str2 = str(params['str2'])
    TRIES = int(params['TRIES'])
    STR_SIZE= len(str1)
    str1,str2 = str1.encode(),str2.encode()
    # print(type(str1),str1)
    # print(type(str2),str2)
    # print(type(TRIES),TRIES)
    # print(type(STR_SIZE),STR_SIZE)
    s_encode = 0
    for _ in range(0, TRIES):
        str2 = base64.b64encode(str1)
        s_encode += len(str2)
    
    s_decode = 0
    for _ in range(0, TRIES):
        s_decode += len(base64.b64decode(str2))

    result = {'s_encode' : str(s_encode), 's_decode' : str(s_decode)}
    
    return result

# p={}
# p['str1']="b1WM0Vx8Fegr2tu6jAmPJZ9aRcG4TEpYNyvfz5Q7DoqBUS3CHl"
# p['str2']="SwDLqvpr"
# p['TRIES']='100'
# print(main(p))
# import random,string
# str1 = ''.join(random.sample(string.ascii_letters + string.digits, 50))
# str2 = ''.join(random.sample(string.ascii_letters + string.digits, 8))
# print(str1)
# print(str2)
