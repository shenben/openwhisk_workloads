CPU_ID=23
perf stat --repeat 10 -e cache-misses,cache-references,instructions,cycles,branch-misses,branch-instructions -C $CPU_ID  \
seq -100 | xargs -i bash invoke.sh
