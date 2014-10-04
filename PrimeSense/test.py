from DeviceReceiver import DeviceReceiver

if __name__ == '__main__':

	primesense_receiver = DeviceReceiver('primesense')
	frame = primesense_receiver.get_frame()