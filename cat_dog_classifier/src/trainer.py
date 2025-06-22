from .model import create_model
from .data_loader import load_data
from keras.callbacks import ModelCheckpoint
import os

def train_model():
    # 确保 models 目录存在
    os.makedirs('../models', exist_ok=True)
    
    # 加载数据
    X_train, X_val, y_train, y_val = load_data(data_dir='data')  # 使用正确的路径
    
    model = create_model()
    
    # 保存最佳模型
    checkpoint = ModelCheckpoint(
        '../models/best_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max'
    )
    
    print(f"训练数据形状: {X_train.shape}")
    print(f"验证数据形状: {X_val.shape}")
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=30,
        batch_size=16,  # 减小批次大小以避免内存问题
        callbacks=[checkpoint]
    )
    
    return history