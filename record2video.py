import numpy as np
import cv2
import pyzed.sl as sl
import os
import sys
import shutil
def progress_bar(percent_done, bar_length=50):
    #Display a progress bar
    done_length = int(bar_length * percent_done / 100)
    bar = '=' * done_length + '-' * (bar_length - done_length)
    sys.stdout.write('[%s] %i%s\r' % (bar, percent_done, '%'))
    sys.stdout.flush()

def builddir(path):
    if not os.path.exists(path):
        os.makedirs(path)
def main():
    svo_input_path = r"record\202403191934.svo"
    output_dir = svo_input_path.split('.')[0]
    builddir(output_dir)

    for vision in ['left','right','depth']:
        avi_output_path = os.path.join(output_dir,vision+'.avi')

        # Specify SVO path parameter
        init_params = sl.InitParameters()
        init_params.set_from_svo_file(svo_input_path)
        init_params.svo_real_time_mode = False  # Don't convert in realtime
        init_params.coordinate_units = sl.UNIT.MILLIMETER  # Use milliliter units (for depth measurements)
        
        zed = sl.Camera()

        err = zed.open(init_params)
        if err != sl.ERROR_CODE.SUCCESS:
            sys.stdout.write(repr(err))
            zed.close()
            exit()

        # Get image size
        image_size = zed.get_camera_information().camera_configuration.resolution
        width = image_size.width
        height = image_size.height

        # Prepare side by side image container equivalent to CV_8UC4
        svo_image_sbs_rgba = np.zeros((height, width, 4), dtype=np.uint8)

        # Prepare single image containers
        left_image = sl.Mat()

        video_writer = cv2.VideoWriter(avi_output_path,
                                       cv2.VideoWriter_fourcc('M', '4', 'S', '2'),
                                       max(zed.get_camera_information().camera_configuration.fps, 25),
                                       (width, height))
        if not video_writer.isOpened():
            sys.stdout.write("OpenCV video writer cannot be opened. Please check the .avi file path and write "
                             "permissions.\n")
            zed.close()
            exit()

        rt_param = sl.RuntimeParameters()
        nb_frames = zed.get_svo_number_of_frames()

        while True:
            err = zed.grab(rt_param)
            if err == sl.ERROR_CODE.SUCCESS:
                svo_position = zed.get_svo_position()

                if vision == 'left':
                    zed.retrieve_image(left_image, sl.VIEW.LEFT)
                elif vision == 'right':
                    zed.retrieve_image(left_image, sl.VIEW.RIGHT)
                else:
                    zed.retrieve_image(left_image, sl.VIEW.DEPTH)
                
                svo_image_sbs_rgba[0:height, 0:width, :] = left_image.get_data()
                ocv_image_sbs_rgb = cv2.cvtColor(svo_image_sbs_rgba, cv2.COLOR_RGBA2RGB)
                video_writer.write(ocv_image_sbs_rgb)

                progress_bar((svo_position + 1) / nb_frames * 100, 30)
            if err == sl.ERROR_CODE.END_OF_SVOFILE_REACHED:
                progress_bar(100 , 30)
                sys.stdout.write("\nSVO end has been reached. Exiting now.\n")
                break

        video_writer.release()    
        zed.close()
        sys.stdout.write(f"{avi_output_path} complete.\n")
    shutil.move(svo_input_path,os.path.join(output_dir, svo_input_path.split('\\')[1]) )
    return 0
if __name__ == "__main__":
    main()