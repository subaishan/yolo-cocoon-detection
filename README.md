# 蚕茧质量检测系统

基于 YOLO 算法的蚕茧质量检测系统，实现蚕茧的自动检测、分类和质量评估。

## 技术栈

### 后端

- Django
- Django REST Framework
- SQLite / MySQL

### 前端

- Vue 3
- Vite
- TypeScript
- Element Plus / Ant Design Vue

### AI 模型

- YOLO (You Only Look Once)
- PyTorch
- Ultralytics

## 项目结构

```txt
cocoon-detection/
├── backend/ # Django 后端
│ ├── accounts/ # 用户管理
│ ├── aiAssistant/ # AI 辅助功能
│ ├── BYwork/ # 主配置
│ ├── Environmental/ # 环境监测
│ ├── gateways/ # 网关管理
│ ├── imageDetection/ # 图像检测
│ ├── pestDetection/ # 害虫检测
│ ├── regions/ # 区域管理
│ ├── sensors/ # 传感器管理
│ ├── utils/ # 工具函数
│ └── manage.py
├── frontend/ # Vue3 前端
│ ├── src/
│ ├── public/
│ ├── package.json
│ └── vite.config.ts
└── yolo-api/ # YOLO 检测服务
│ ├── main.py
│ ├── test.py
│ └── models/ # 模型文件目录
└── requirements.txt # 环境依赖
```

## 快速开始

### 环境要求

- Python >= 3.8
- Node.js >= 16
- npm 或 yarn

### 环境依赖

#### venv

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### conda

```bash
# 创建 conda 环境
conda create -n cocoon-backend python=3.10

# 激活环境
conda activate cocoon-backend

# 安装依赖
pip install -r requirements.txt
```

### 模型权重下载

- 链接：[https://pan.baidu.com/s/1wtx5KDxrBy17ur4jBOkBrAx](https://pan.baidu.com/s/1wtx5KDxrBy17ur4jBOkBrA)
- 提取码：migv

下载后将模型文件放入 `yolo-api/models/` 目录。

### 后端安装

```bash
# 进入后端目录
cd backend

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 运行服务
python manage.py runserver
```

### 前端安装

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 开发模式运行
npm run dev

# 生产构建
npm run build
```

### YOLO服务

```bash
# 进入 YOLO 服务目录
cd yolo-api

# 运行服务
python main.py
```

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件

## 说明

- 本课题为2026届本科毕业设计
- 如有问题请联系：a18830896647@163.com
