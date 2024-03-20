import sys
import pyzed.sl as sl
from signal import signal, SIGINT
import datetime
import numpy as np


cam = sl.Camera()
points = []
#Handler to deal with CTRL+C properly
def handler(signal_received, frame):
    cam.disable_recording()
    cam.close()
    sys.exit(0)

signal(SIGINT, handler)


def main():
    global points

    init = sl.InitParameters()
    init.depth_mode = sl.DEPTH_MODE.ULTRA # Set configuration parameters for the sl
    init.camera_resolution = sl.RESOLUTION.HD2K
    init.coordinate_units = sl.UNIT.METER
    init.depth_maximum_distance = 20

    status = cam.open(init) 
    if status != sl.ERROR_CODE.SUCCESS: 
        print("Camera Open", status, "Exit program.")
        exit(1)
        
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M")

    recording_param = sl.RecordingParameters(f"record/{current_time}.svo", sl.SVO_COMPRESSION_MODE.H264) # Enable recording with the filename specified in argument
    err = cam.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Recording sl : ", err)
        exit(1)


    runtime = sl.RuntimeParameters()
    print("SVO is Recording, use Ctrl-C to stop.") # Start recording SVO, stop with Ctrl-C command
    frames_recorded = 0  

    while True:
        if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS : # Check that a new image is successfully acquired
            frames_recorded += 1
            print("Frame count: " + str(frames_recorded), end="\r")

if __name__ == "__main__":
    main()