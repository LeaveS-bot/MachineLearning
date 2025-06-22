import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

def load_data(data_dir='data', img_size=(150, 150)):  # 修改为 'data' 而不是 '../data'
    categories = ['cats', 'dogs']
    X, y = [], []
    
    # 获取当前脚本所在目录的绝对路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, data_dir)
    
    for label, category in enumerate(categories):
        path = os.path.join(data_path, category)
        print(f"正在加载数据从: {path}")  # 添加调试信息
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"目录不存在: {path}")
        
        for img_file in os.listdir(path):
            img_path = os.path.join(path, img_file)
            try:
                img = cv2.imread(img_path)
                if img is None:
                    print(f"警告: 无法读取图片 {img_path}")
                    continue
                    
                img = cv2.resize(img, img_size)
                img = img / 255.0  # 归一化
                
                X.append(img)
                y.append(label)
            except Exception as e:
                print(f"处理图片 {img_path} 时出错: {str(e)}")
    
    return train_test_split(
        np.array(X), np.array(y),
        test_size=0.2,
        random_state=42
    )