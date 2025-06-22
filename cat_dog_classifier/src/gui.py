import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
from .predictor import Predictor
import os

class CatDogGUI:
    def __init__(self, master):
        self.master = master
        master.title("猫狗识别分类器")
        master.geometry("600x600")
        
        # 初始化预测器
        try:
            self.predictor = Predictor()
        except Exception as e:
            messagebox.showerror("错误", f"无法加载模型: {str(e)}")
            master.destroy()
            return
        
        # 创建界面元素
        self.create_widgets()
        
        # 当前选择的图片
        self.current_image = None
    
    def create_widgets(self):
        # 标题
        self.title_label = ttk.Label(
            self.master, 
            text="猫狗识别分类器", 
            font=("Arial", 20))
        self.title_label.pack(pady=20)
        
        # 图片显示区域
        self.image_frame = ttk.Frame(self.master)
        self.image_frame.pack(pady=10)
        
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack()
        
        # 按钮区域
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(pady=10)
        
        # 选择图片按钮
        self.browse_button = ttk.Button(
            self.button_frame, 
            text="选择图片", 
            command=self.browse_image
        )
        self.browse_button.grid(row=0, column=0, padx=10)
        
        # 识别按钮
        self.predict_button = ttk.Button(
            self.button_frame, 
            text="识别", 
            command=self.predict_image,
            state=tk.DISABLED  # 初始禁用
        )
        self.predict_button.grid(row=0, column=1, padx=10)
        
        # 结果区域
        self.result_frame = ttk.Frame(self.master)
        self.result_frame.pack(pady=20)
        
        # 识别结果
        ttk.Label(
            self.result_frame, 
            text="识别结果:", 
            font=("Arial", 14)
        ).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        self.result_text = ttk.Label(
            self.result_frame, 
            text="", 
            font=("Arial", 16),
            foreground="red"
        )
        self.result_text.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # 置信度
        ttk.Label(
            self.result_frame, 
            text="置信度:", 
            font=("Arial", 14)
        ).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        
        self.confidence_text = ttk.Label(
            self.result_frame, 
            text="", 
            font=("Arial", 16)
        )
        self.confidence_text.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    
    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png")]
        )
        
        if file_path:
            try:
                self.display_image(file_path)
                self.current_image = file_path
                self.predict_button.config(state=tk.NORMAL)  # 启用识别按钮
            except Exception as e:
                messagebox.showerror("错误", f"无法加载图片: {str(e)}")
    
    def display_image(self, path):
        # 使用PIL打开图片并调整大小
        img = Image.open(path)
        img = img.resize((300, 300), Image.LANCZOS)
        
        # 转换为Tkinter兼容格式
        photo = ImageTk.PhotoImage(img)
        
        # 更新标签
        self.image_label.configure(image=photo)
        self.image_label.image = photo  # 保持引用
    
    def predict_image(self):
        if self.current_image:
            try:
                label, confidence = self.predictor.predict(self.current_image)
                conf_percent = f"{abs(confidence-0.5)*200:.1f}%"
                
                self.result_text.config(text=label)
                self.confidence_text.config(text=conf_percent)
            except Exception as e:
                messagebox.showerror("错误", f"识别失败: {str(e)}")
        else:
            messagebox.showwarning("警告", "请先选择图片文件")

def run_gui():
    root = tk.Tk()
    app = CatDogGUI(root)
    root.mainloop()

if __name__ == '__main__':
    run_gui()