import os
import pandas as pd
import numpy as np

# 遍历指定文件夹中的所有CSV文件
folder_path = r'record\202403191939'  # 替换成你的文件夹路径

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # 读取CSV文件
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)

        # 计算深度图的灰度值并添加到DataFrame中
        depth_gray = []
        for index, row in df.iterrows():
            depth_rgb = np.array([int(x) for x in row['1'][1:-1].split()])
            depth_gray_value = np.dot(depth_rgb, [0.299, 0.587, 0.114])  # 加权平均法计算灰度值
            depth_gray.append(depth_gray_value)

        df['深度圖灰度值'] = depth_gray

        # 计算模型的灰度值并添加到DataFrame中
        model_gray = []
        for index, row in df.iterrows():
            model_rgb = np.array([int(x) for x in row['2'][1:-1].split()])
            model_gray_value = np.dot(model_rgb, [0.299, 0.587, 0.114])  # 加权平均法计算灰度值
            model_gray.append(model_gray_value)

        df['模型灰度值'] = model_gray

        # 将DataFrame保存回CSV文件
        output_file_path = os.path.join(folder_path, 'output_' + filename)
        df.to_csv(output_file_path, index=False)
