import sys

ULTRA_PATH = r"C:\Users\SuBaiShan\Desktop\CDetYOLO"
if ULTRA_PATH not in sys.path:
    sys.path.insert(0, ULTRA_PATH)

import cv2
import uvicorn
from ultralytics import YOLO
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import base64
from io import BytesIO
from PIL import Image
import torch
import time
from datetime import datetime
from contextlib import asynccontextmanager

app = FastAPI(title="CDetYOLO桑蚕病虫害检测API", version="1.0")

MODEL_PATH = './models/YOLO.pt'
CONFIDENCE_THRESHOLD = 0.25  # 置信度阈值
IOU_THRESHOLD = 0.45  # IOU阈值
    

# 检查GPU可用性
def check_gpu():
    if torch.cuda.is_available():
        gpu_count = torch.cuda.device_count()
        gpu_name = torch.cuda.get_device_name(0) if gpu_count > 0 else "Unknown"
        return {
            "available": True,
            "count": gpu_count,
            "device_name": gpu_name,
            "device": "cuda"
        }
    else:
        return {
            "available": False,
            "device": "cpu"
        }


# 生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时加载模型
    app.state.model = None
    try:
        print("正在加载YOLOv11模型...")
        # 检查设备
        app.state.device_info = check_gpu()
        print(f"设备信息: {app.state.device_info}")

        app.state.model = YOLO(MODEL_PATH)
        if app.state.device_info["available"]:
            app.state.model = app.state.model.cuda()
            print("模型已加载到GPU")
        else:
            print("模型运行在CPU上")

        print("模型加载成功!")
    except Exception as e:
        print(f"模型加载失败: {e}")
        raise e
    yield
    # 关闭时清理
    if app.state.model:
        del app.state.model
        print("模型已卸载")

# 初始化FastAPI应用
app = FastAPI(
    title="YOLOv11桑蚕病虫害检测API",
    version="1.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # 允许所有源
    allow_credentials=True,       # 允许凭据
    allow_methods=["*"],          # 允许所有方法
    allow_headers=["*"],          # 允许所有头
)


@app.get("/model-info")
async def model_info():
    """获取模型信息"""
    if app.state.model is None:
        raise HTTPException(status_code=503, detail="模型未加载")
    print(app.state.model)

    return {
        "model_type": type(app.state.model).__name__,
        "model_path": MODEL_PATH,
        "confidence_threshold": CONFIDENCE_THRESHOLD,
        "iou_threshold": IOU_THRESHOLD
    }


def preprocess_image(image: Image.Image) -> np.ndarray:
    """预处理图像"""
    # 转换为numpy数组 (H, W, C)
    image_np = np.array(image)
    
    # 确保图像为RGB格式
    if len(image_np.shape) == 2:  # 灰度图
        image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
    elif image_np.shape[2] == 4:  # RGBA
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
    elif image_np.shape[2] == 3:  # RGB
        pass
    else:
        raise ValueError("不支持的图像格式")
    
    return image_np


def process_yolov11_results(results):
    """处理YOLOv11的预测结果"""
    detections = []
    
    # 检查是否有检测结果
    if results and hasattr(results[0], 'boxes') and results[0].boxes is not None:
        for box in results[0].boxes:
            # 获取边界框坐标
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            confidence = float(box.conf[0].cpu().numpy())
            class_id = int(box.cls[0].cpu().numpy())
            class_name = results[0].names[class_id]
            
            detections.append({
                "class_id": class_id,
                "class_name": class_name,
                "confidence": confidence,
                "bbox": [float(x1), float(y1), float(x2), float(y2)],
                "area": float((x2 - x1) * (y2 - y1))
            })
    
    return detections


@app.post("/detect-raw/")
async def detect_pest_raw(original_image: UploadFile = File(...)):
    """返回原始检测数据，不包含图像（性能更好）"""
    try:
        start_time = time.time()
        
        if app.state.model is None:
            raise HTTPException(status_code=503, detail="模型未加载")
        
        # 读取上传的图像
        contents = await original_image.read()
        image = Image.open(BytesIO(contents)).convert("RGB")
        image_np = np.array(image)
        
        device = 'cuda' if app.state.device_info["available"] else 'cpu'

        # 使用YOLOv11进行预测
        results = app.state.model(
            image_np,
            conf=CONFIDENCE_THRESHOLD,
            iou=IOU_THRESHOLD,
            verbose=False,
            device=device
        )
        
        # 处理检测结果
        detections = process_yolov11_results(results)
        
        processing_time = time.time() - start_time
        
        return {
            "success": True,
            "detections": detections,
            "detection_count": len(detections),
            "processing_time": round(processing_time, 3),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理图像时发生错误: {str(e)}")


@app.post("/detect/")
async def detect_pest(original_image: UploadFile = File(...)):
    """病虫害检测端点"""
    try:
        start_time = time.time()
        
        # 检查模型是否加载
        if app.state.model is None:
            raise HTTPException(status_code=503, detail="模型未加载")
        
        # 读取上传的图像
        contents = await original_image.read()
        image = Image.open(BytesIO(contents)).convert("RGB")
        original_size = image.size
        
        # 预处理图像
        image_np = preprocess_image(image)
        
        # 使用YOLOv11进行预测
        results = app.state.model(
            image_np,
            conf=CONFIDENCE_THRESHOLD,
            iou=IOU_THRESHOLD,
            verbose=False  # 减少输出
        )

        # 处理检测结果
        detections = process_yolov11_results(results)
        
        # 获取绘制好的图像
        plotted_image = results[0].plot()  # 返回BGR格式的numpy数组
            
        # 转换为PIL图像 (BGR -> RGB)
        plotted_image_rgb = cv2.cvtColor(plotted_image, cv2.COLOR_BGR2RGB)
        output_image = Image.fromarray(plotted_image_rgb)
        
        
        # 将处理后的图像转换为base64
        buffered = BytesIO()
        output_image.save(buffered, format="JPEG", quality=95)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # 计算处理时间
        processing_time = time.time() - start_time
        
        # 返回结果
        return JSONResponse({
            "success": True,
            "detections": detections,
            "detection_count": len(detections),
            "processing_time": round(processing_time, 3),
            "original_size": {"width": original_size[0], "height": original_size[1]},
            "processed_image": f"data:image/jpeg;base64,{img_str}",
            "timestamp": datetime.now().isoformat(),
            "model_info": {
                "model_name": "CDet-YOLOv11",
                "confidence_threshold": CONFIDENCE_THRESHOLD,
                "iou_threshold": IOU_THRESHOLD
            }
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理图像时发生错误: {str(e)}")


@app.get("/gpu-status")
async def gpu_status():
    """检查GPU状态"""
    gpu_info = check_gpu()
    
    # 测试GPU性能
    if gpu_info["available"]:
        try:
            # 简单的GPU测试
            a = torch.randn(1000, 1000).cuda()
            b = torch.randn(1000, 1000).cuda()
            c = torch.matmul(a, b)
            gpu_info["test_passed"] = True
        except Exception as e:
            gpu_info["test_passed"] = False
            gpu_info["test_error"] = str(e)
    
    return gpu_info


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy" if app.state.model is not None else "unhealthy",
        "model_loaded": app.state.model is not None,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/")
async def root():
    """根端点"""
    return {
        "message": "YOLOv11桑蚕病虫害检测API",
        "version": "1.0",
        "endpoints": {
            "POST /detect/": "上传图像进行病虫害检测（返回图像）",
            "POST /detect-raw/": "上传图像进行检测（只返回数据）",
            'GET /gpu-status': '获取GPU状态',
            "GET /health": "健康检查",
            "GET /model-info": "获取模型信息",
        }
    }

if __name__ == '__main__':

    uvicorn.run(app, host="0.0.0.0", port=6006)



### 使用fastapi ultralytics pytorch库