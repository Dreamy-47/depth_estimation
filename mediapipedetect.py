import cv2
import mediapipe as mp
import numpy as np
import time
import pandas as pd
import os
def draw_pose_connections(frame, landmarks, connections):
    for connection in connections:
        point1 = (int(landmarks[connection[0]].x * frame.shape[1]), int(landmarks[connection[0]].y * frame.shape[0]))
        point2 = (int(landmarks[connection[1]].x * frame.shape[1]), int(landmarks[connection[1]].y * frame.shape[0]))
        cv2.line(frame, point1, point2, (0, 255, 0), 2)

def main(folder):
    target_frame_num = [50,100,150]
    vedio_name = [r"depth.avi" , r"left_depthgray.mp4",r"left.avi"]

    capd = cv2.VideoCapture(os.path.join(folder,vedio_name[0]))
    capl = cv2.VideoCapture(os.path.join(folder,vedio_name[2]))
    capld = cv2.VideoCapture(os.path.join(folder,vedio_name[1]))

    mp_pose = mp.solutions.pose
    pose_connection = mp_pose.POSE_CONNECTIONS

    def save2img(cap,target,name):
        ret, frame = cap.read()
        cv2.imwrite(f"20240312/frame_{target}_video_{name.split('.')[0]}.jpg", frame)


    with mp.solutions.pose.Pose(static_image_mode=True,
                                model_complexity=2,
                                min_detection_confidence=0.5) as mp_sample_pose:
        """
        i = 0
        while capl.isOpened():
            ret , framel = capl.read()
            _ , framed = capd.read()
            _ , frameld = capld.read()
            if not ret:
                break
            if i in target_frame_num:

            i+=1"""
        for target in target_frame_num:
            capd.set(cv2.CAP_PROP_POS_FRAMES,target)
            capl.set(cv2.CAP_PROP_POS_FRAMES,target)
            capld.set(cv2.CAP_PROP_POS_FRAMES,target)
            """
            save2img(capd,target,vedio_path[0])
            save2img(capl,target,vedio_path[2])
            save2img(capld,target,vedio_path[1])
            """
            _ , frame = capl.read()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            landmarks = mp_sample_pose.process(cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2RGB)).pose_landmarks.landmark
            #print(landmarks)

            _ , framed = capd.read()
            _ , frameld = capld.read()
            depvalue = []
            for landmark in landmarks:
                if landmark.visibility >= 0.8:
                    image_h, image_w, _ = frame_rgb.shape
                    """
                    Remember video resolution
                    NEED TO CHANGE
                    2K : 2208 * 1242
                    """
                    landmark_x = int(landmark.x * 2208)
                    landmark_y = int(landmark.y * 1242)
                    depth_value = framed[landmark_y, landmark_x]
                    depth_value_left = frameld[landmark_y, landmark_x]
                    depvalue.append([f"({landmark_x},{landmark_y})",depth_value, depth_value_left])
            #draw_pose_connections(frame_rgb, landmarks, pose_connection)
            #cv2.imwrite(f"20240312/frame_{target}_video_{vedio_path[2].split('.')[0]}.jpg", frame_rgb)
            
            df = pd.DataFrame(depvalue)
            df.to_csv(f"{folder}/depout{target}.csv",index = False)
            print(depvalue)
    capd.release()
    capl.release()
    capld.release()

if __name__ == '__main__':
    folder = r'record\202403191939'
    main(folder)
