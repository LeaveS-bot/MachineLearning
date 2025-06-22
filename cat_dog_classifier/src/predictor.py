import cv2
import numpy as np
from keras.models import load_model
import os

class Predictor:
    def __init__(self, model_path=None):
        if model_path is None:
            # 自动确定模型路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            model_path = os.path.join(project_root, 'models', 'best_model.h5')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型文件不存在: {model_path}")
        
        print(f"加载模型: {model_path}")
        try:
            self.model = load_model(model_path)
            self.img_size = (150, 150)
            print("模型加载成功")
        except Exception as e:
            raise RuntimeError(f"加载模型失败: {str(e)}")
    
    def predict(self, img_path):
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"图片文件不存在: {img_path}")
        
        try:
            img = cv2.imread(img_path)
            if img is None:
                raise ValueError(f"无法读取图片: {img_path}")
            
            img = cv2.resize(img, self.img_size)
            img = img / 255.0
            img = np.expand_dims(img, axis=0)
            
            prediction = self.model.predict(img)[0][0]
            return '狗' if prediction > 0.5 else '猫', float(prediction)
        except Exception as e:
            raise RuntimeError(f"预测失败: {str(e)}")