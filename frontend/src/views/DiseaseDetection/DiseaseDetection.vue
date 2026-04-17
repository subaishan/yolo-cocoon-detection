<template>
  <div class="pest-identification-container">
    <!-- 页面标题 -->
    <div class="page-title">
      <h2>病虫害图像识别</h2>
      <p>上传图片，获取专业的病虫害识别结果</p>
    </div>

    <!-- 图片对比区域 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <div class="image-panel">
          <h3 class="panel-title">
            <el-icon><Picture /></el-icon>
            原始图片
          </h3>
          <div class="image-uploader" @click="triggerUpload">
            <el-upload
              ref="uploadRef"
              class="avatar-uploader"
              action="#"
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleImageChange"
              accept="image/*"
            >
              <template v-if="originalImage">
                <img :src="originalImage" class="uploaded-image" />
              </template>
              <!-- <img v-if="originalImage" :src="originalImage" class="uploaded-image" /> -->
            </el-upload>
            <div v-if="!originalImage" class="upload-tip">
              <p>点击上传图片</p>
              <p>支持 JPG、PNG 格式，最大5MB</p>
            </div>
          </div>
          <el-button
            v-if="originalImage"
            type="danger"
            :icon="Delete"
            @click="removeImage"
            class="remove-btn"
          >
            移除图片
          </el-button>
        </div>
      </el-col>

      <el-col :span="12">
        <div class="image-panel">
          <h3 class="panel-title">
            <el-icon><Search /></el-icon>
            识别结果
          </h3>
          <div class="result-image-container">
            <div v-if="isLoading" class="loading-container">
              <el-icon class="is-loading"><Loading /></el-icon>
              <p>正在分析中...</p>
            </div>
            <img v-else-if="resultImage" :src="resultImage" class="result-image" />
            <div v-else class="placeholder">
              <el-icon><Crop /></el-icon>
              <p>识别结果将显示在这里</p>
            </div>
          </div>
          <el-button
            v-if="resultImage"
            type="primary"
            :icon="Download"
            @click="downloadResult"
            class="download-btn"
          >
            下载结果
          </el-button>
        </div>
      </el-col>
    </el-row>

    <!-- 识别按钮 -->
    <div class="action-section">
      <el-button
        type="success"
        :icon="MagicStick"
        :loading="isLoading"
        :disabled="!originalImage"
        @click="startIdentification"
        size="large"
      >
        {{ isLoading ? '识别中...' : '开始识别' }}
      </el-button>
    </div>

    <!-- 详细信息区域 -->
    <div class="details-section" v-if="showDetails">
      <el-collapse v-model="activeNames">
        <el-collapse-item title="识别详细信息" name="1">
          <div class="detail-content" style="font-size: large">{{ descriptionText }}</div>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Picture,
  Search,
  Delete,
  Download,
  MagicStick,
  Crop,
  Loading,
} from '@element-plus/icons-vue'
import { useImageDetectionStore } from '@/stores/modules/imageDetection/index'

const ImageDetection = useImageDetectionStore()

// 响应式数据
const uploadRef = ref()
const originalImage = ref('')
const originalImageFile = ref(null)
const resultImage = ref('')
const isLoading = ref(false)
const showDetails = ref(false)
const activeNames = ref(['1', '2'])
const descriptionText = ref('')

// 处理方法
const triggerUpload = () => {
  if (!originalImage.value) {
    uploadRef.value.$el.querySelector('input').click()
  }
}

const handleImageChange = (file) => {
  const isJPGOrPNG = file.raw.type === 'image/jpeg' || file.raw.type === 'image/png'
  const isLt5M = file.raw.size / 1024 / 1024 < 5

  if (!isJPGOrPNG) {
    ElMessage.error('上传图片只能是 JPG 或 PNG 格式!')
    return false
  }
  if (!isLt5M) {
    ElMessage.error('上传图片大小不能超过 5MB!')
    return false
  }

  // 创建本地URL用于预览
  originalImageFile.value = file.raw
  originalImage.value = URL.createObjectURL(file.raw)
  resultImage.value = ''
  showDetails.value = false
  return true
}

const removeImage = () => {
  if (originalImage.value) {
    URL.revokeObjectURL(originalImage.value)
  }
  originalImageFile.value = ''
  originalImage.value = ''
  resultImage.value = ''
  showDetails.value = false
  descriptionText.value = ''
}

const startIdentification = async () => {
  if (!originalImage.value) {
    ElMessage.warning('请先上传图片')
    return
  }

  isLoading.value = true

  try {
    const params = new FormData()
    params.append('original_image', originalImageFile.value)
    const data = await ImageDetection.createRecord(params)

    resultImage.value = data.image

    // 直接在这里计算统计信息
    const classStatistics = {}

    data.data.detection_data.forEach((item) => {
      classStatistics[item.class_name] = (classStatistics[item.class_name] || 0) + 1
    })

    // 创建描述文字
    for (const [className, count] of Object.entries(classStatistics)) {
      descriptionText.value += `${className}种类检测数量是${count}个,`
    }

    // 去掉最后一个换行符
    console.log(descriptionText.value)
    console.log('检测结果统计:', classStatistics)

    showDetails.value = true

    ElMessage.success('识别成功')
  } catch (error) {
    ElMessage.error('识别失败: ' + (error.message || '网络错误'))
    console.error('Identification error:', error)
  } finally {
    isLoading.value = false
  }
}

const downloadResult = async () => {
  if (!resultImage.value) {
    ElMessage.warning('没有可下载的结果')
    return
  }

  // 使用fetch获取图片
  const response = await fetch(resultImage.value)
  const blob = await response.blob()

  // 创建blob URL（这个URL浏览器会视为可下载的）
  const blobUrl = URL.createObjectURL(blob)

  const link = document.createElement('a')
  link.href = blobUrl
  link.download = '病虫害识别结果.jpg'
  document.body.appendChild(link)
  link.click()

  // 清理
  document.body.removeChild(link)
  URL.revokeObjectURL(blobUrl) // 释放内存

  ElMessage.success('下载成功')

  ElMessage.success('下载成功')
}
</script>

<style scoped>
.pest-identification-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);

  .page-title {
    text-align: center;
    margin-bottom: 30px;

    h2 {
      color: #303133;
      font-size: 24px;
      margin-bottom: 10px;
      font-weight: 600;
    }

    p {
      color: #606266;
      font-size: 14px;
    }
  }
}

.image-panel {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;

  .panel-title {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    color: #303133;
    width: 100%;

    .el-icon {
      margin-right: 8px;
      color: #409eff;
    }
  }
}

.image-uploader {
  width: 100%;
  height: 300px;
  border: 2px dashed #dcdfe6;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;

  &:hover {
    border-color: #409eff;
  }

  :deep(.avatar-uploader) {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .uploaded-image {
    max-width: 100%;
    max-height: 100%;
    height: 300px;
    object-fit: contain;
  }

  .upload-tip {
    text-align: center;
    color: #8c939d;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    p {
      margin: 5px 0;
    }
  }
}

.result-image-container {
  width: 100%;
  height: 300px;
  border: 1px solid #e6e6e6;
  border-radius: 6px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
  background-color: #f9f9f9;

  .loading-container {
    text-align: center;

    .el-icon {
      font-size: 40px;
      color: #409eff;
      margin-bottom: 10px;
      animation: rotating 2s linear infinite;
    }

    p {
      color: #606266;
    }
  }

  .result-image {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }

  .placeholder {
    text-align: center;
    color: #8c939d;

    .el-icon {
      font-size: 40px;
      margin-bottom: 10px;
    }
  }
}

.remove-btn,
.download-btn {
  width: 100%;
}

.action-section {
  text-align: center;
  margin: 30px 0;
}

.details-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

  :deep(.el-collapse-item__header) {
    font-weight: 600;
    font-size: 16px;
  }

  .detail-content,
  .suggestion-content {
    padding: 10px;
  }
}
</style>
