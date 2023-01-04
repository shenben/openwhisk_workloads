CPU_ID=23
# perf stat --repeat 10 -e cache-misses,cache-references,instructions,cycles,branch-misses,branch-instructions -C $CPU_ID  \
taskset -c $CPU_ID python -c "import json;from json2 import main; params=json.loads(open('1.json','r').read());print(main(params));" & # > h1.txt
# perf stat --repeat 10 -e cache-misses,cache-references,instructions,cycles,branch-misses,branch-instructions -C $CPU_ID  \
taskset -c $CPU_ID python -c "import json;from primes2 import main;params={};params['N']=2000000;print(main(params));" & # > h2.txt
# perf stat --repeat 10 -e cache-misses,cache-references,instructions,cycles,branch-misses,branch-instructions -C $CPU_ID  \
taskset -c $CPU_ID python -c "import json;from httpendpoint2 import main;params={};print(main(params));" & # >h3.txt
# perf stat --repeat 10 -e cache-misses,cache-references,instructions,cycles,branch-misses,branch-instructions -C $CPU_ID  \
taskset -c $CPU_ID python -c "import json;from base642 import main;params={};print(main(params));"  # >h4.txt
