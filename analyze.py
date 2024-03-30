import math
import numpy as np
import cv2
import pyzed.sl as sl


def main(svo_input_path):
    # Specify SVO path parameter
    init_params = sl.InitParameters()
    init_params.set_from_svo_file(svo_input_path)
    init_params.svo_real_time_mode = False  # Don't convert in realtime
    init_params.coordinate_units = sl.UNIT.METER  # Use milliliter units (for depth measurements)
    cam = sl.Camera()
    runtime = sl.RuntimeParameters(confidence_threshold=90)

    err = cam.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(err)
        cam.close()
        exit()

    # Prepare side by side image container equivalent to CV_8UC4

    # Prepare single image containers
    image = sl.Mat()
    depth_image = sl.Mat(image.get_width(), image.get_height(), sl.MAT_TYPE.U8_C4)
    point_cloud = sl.Mat()

    def onmouse_pick_points_1(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # threeD = param
            print('\n像素座標 x = %d, y = %d' % (x, y))
            # print("世界坐标是：", threeD[y][x][0], threeD[y][x][1], threeD[y][x][2], "mm")
            err, point3D = point_cloud.get_value(x, y)
            x = point3D[0]
            y = point3D[1]
            z = point3D[2]
            color = point3D[3]
            print("世界座標xyz 是:%.3f,%.3f,%.3f "% (x,y,z))

            distance = math.sqrt(point3D[0] * point3D[0] + point3D[1] * point3D[1] + point3D[2] * point3D[2])
            print("距離是：", distance, "m")


    while True:
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            cam.retrieve_image(image, sl.VIEW.LEFT)
            cam.retrieve_image(depth_image,sl.VIEW.DEPTH)
            cam.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
            image_depth = depth_image.get_data()
            # 鼠标回调事件
            cv2.namedWindow("depth", cv2.WINDOW_AUTOSIZE)
            cv2.setMouseCallback("depth", onmouse_pick_points_1)
            cv2.imshow('depth', image_depth)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        elif err == sl.ERROR_CODE.END_OF_SVOFILE_REACHED: #Check if the .svo has ended
            
            print("SVO end has been reached. Looping back to 0")
            cam.set_svo_position(0)
        else:
            print("Grab ZED : ", err)
            break
    
    cam.close()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    svo_input_path = r"record\dest\3-72.5-164.5-318.5\202403251651.svo"
    main(svo_input_path)