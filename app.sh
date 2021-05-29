(python /home/workspace/producers/simulation.py &) &
(cd /home/workspace/consumers/ && faust -A faust_stream worker &) &
(python /home/workspace/consumers/ksql.py &) &
(python /home/workspace/consumers/server.py &) &
