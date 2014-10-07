#=====[ Step 1: configuration	]=====
source ./configure.sh

#=====[ Step 1: run the c++ program	]=====
cd primesense_receiver
source ./run.sh &
cd ..

#=====[ Step 2: run the python program	]=====
cd bin
python ./one_player_live.py
cd ..
