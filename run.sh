#=====[ Step 1: configuration	]=====
echo "###[ Configuring primesense_receiver ]###"
source ./configure.sh

#=====[ Step 1: run the c++ program	]=====
echo "###[ Spawning primesense_receiver ]###"
cd primesense_receiver
source ./run.sh &
sleep 3
echo '-----'
pgrep procname && echo Running
cd ..


#=====[ Step 2: run the python program	]=====
cd bin
# python ./one_player_live.py
cd ..
