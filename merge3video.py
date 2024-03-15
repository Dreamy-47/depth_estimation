import cv2

# 讀取三個影片
video1 = cv2.VideoCapture('depth.avi')
video2 = cv2.VideoCapture('left.avi')
video3 = cv2.VideoCapture('left_depthgray.mp4')

# 檢查影片是否成功打開
if not (video1.isOpened() and video2.isOpened() and video3.isOpened()):
    print("無法打開一個或多個影片文件")
    exit()

# 取得第一個影片的尺寸
width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 設置新的尺寸 (三倍寬度，同高度)
new_width = width * 3
new_height = height

# 建立一個新的影片寫入物件
out = cv2.VideoWriter('merged_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (new_width, new_height))

# 讀取影片幀並寫入新影片
while True:
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()
    ret3, frame3 = video3.read()

    # 檢查是否成功讀取幀
    if not (ret1 and ret2 and ret3):
        break

    # 將幀調整大小以符合新的尺寸
    frame1_resized = cv2.resize(frame1, (width, height))
    frame2_resized = cv2.resize(frame2, (width, height))
    frame3_resized = cv2.resize(frame3, (width, height))

    # 將三個幀水平合併
    merged_frame = cv2.hconcat([frame1_resized, frame2_resized, frame3_resized])

    # 將合併後的幀寫入新影片
    out.write(merged_frame)

# 釋放資源
video1.release()
video2.release()
video3.release()
out.release()
cv2.destroyAllWindows()
