import os
import sys
import subprocess
from pathlib import Path

top_dir = Path.cwd() / 'functions'
os.chdir(str(top_dir / 'microbenchmarks'/'json'))
for i in range(1,10):
    cmd = 'ruby generate_json.rb'
    subprocess.call(cmd, shell=True)
    j=i+1
    cmd = 'cp 1.json '+ str(j) +'.json'
    subprocess.call(cmd, shell=True)
