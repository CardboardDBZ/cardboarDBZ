import os
import subprocess
import time


if __name__ == '__main__':
	
	#=====[ Step 1: configure package ]=====
	os.system('source ./configure.sh')

	#=====[ Step 2: spawn primesense receiver	]=====
	os.chdir('primesense_receiver')
	os.system('source ./run.sh')
	os.chdir('..')

	#=====[ Step 3: spawn python package	]=====
	os.chdir('bin')
	os.system('python one_player_live.py')
	os.chdir('..')


