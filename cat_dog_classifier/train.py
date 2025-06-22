from src.trainer import train_model

if __name__ == '__main__':
    print("开始训练模型...")
    history = train_model()
    print("模型训练完成! 最佳模型已保存到 models/ 目录")