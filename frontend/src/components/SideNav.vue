<template>
  <el-menu router :default-active="$route.path" class="side-nav">
    <el-menu-item :index="{ name: 'home' }">
      <el-icon><HomeFilled /></el-icon>
      <span>首页</span>
    </el-menu-item>

    <el-menu-item :index="{ name: 'dashboard' }">
      <el-icon><DataBoard /></el-icon>
      <span>数据看板</span>
    </el-menu-item>

    <el-sub-menu index="regions">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>园区管理</span>
      </template>
      <el-menu-item index="/#">园区列表</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="gateways">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>网关管理</span>
      </template>
      <el-menu-item index="/#">网关列表</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="sensors">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>传感器管理</span>
      </template>
      <el-menu-item index="/#">传感器列表</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="diseasedetection">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>病虫害识别</span>
      </template>
      <el-menu-item :index="{ name: 'diseasedetection' }">病虫害检测</el-menu-item>
      <el-menu-item :index="{ name: 'detectionhistory' }">检测历史记录</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="aiAssistant">
      <template #title>
        <el-icon><ChatDotRound /></el-icon>
        <span>智能助手</span>
      </template>
      <el-menu-item :index="{ name: 'assistantchat' }">
        <el-icon><Plus /></el-icon>
        <span>新的会话</span>
      </el-menu-item>

      <!-- 历史对话子菜单 -->
      <el-sub-menu index="assistanthistory">
        <template #title>
          <el-icon><Clock /></el-icon>
          <span>历史对话 ({{ conversationKeys.length }})</span>
        </template>
        <el-menu-item
          v-for="conversationId in conversationKeys"
          :key="conversationId"
          :index="`/assistanthistory/${conversationId}`"
        >
          <span class="conversation-title">
            {{ conversationsInfo[conversationId]?.title || `对话 ${conversationId}` }}
          </span>

          <!-- 删除图标 -->
          <el-icon
            class="delete-icon"
            @click.stop="confirmDelete(conversationId, conversationsInfo[conversationId].title)"
          >
            <Close />
          </el-icon>
        </el-menu-item>
      </el-sub-menu>
    </el-sub-menu>

    <el-menu-item :index="{ name: 'about' }">
      <el-icon><InfoFilled /></el-icon>
      <span>关于系统</span>
    </el-menu-item>
  </el-menu>
</template>

<script setup lang="ts">
import {
  HomeFilled,
  DataBoard,
  Setting,
  InfoFilled,
  ChatDotRound,
  Plus,
  Close,
} from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { useRoute } from 'vue-router'
import { onMounted, computed } from 'vue'
import { useAiChatStore } from '@/stores/modules/aiAssistant/index'

const AiChatStore = useAiChatStore()
const $route = useRoute()

// 直接从 store 中获取 conversationsInfo
const conversationsInfo = computed(() => {
  return AiChatStore.getconversationsInfo() || {}
})

// 获取对话ID的数组
const conversationKeys = computed(() => {
  return AiChatStore.getConversations() || []
})

// 加载对话列表
onMounted(async () => {
  try {
    await AiChatStore.loadConversations()
  } catch (error) {
    console.error('加载对话列表失败:', error)
  }
})

// 确认删除对话框
const confirmDelete = (conversationId, conversationTitle) => {
  ElMessageBox.confirm(`确定要删除对话"${conversationTitle}"吗？此操作不可恢复。`, '确认删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
    customClass: 'delete-confirm-dialog',
    distinguishCancelAndClose: true,
  })
    .then(async () => {
      // 用户点击确定
      await deleteConversation(conversationId)
    })
    .catch((action) => {
      if (action === 'cancel') {
        // 用户点击取消
        ElMessage.info('已取消删除')
      }
    })
}

// 执行删除操作
const deleteConversation = async (conversationId) => {
  try {
    // 调用 store 中的删除方法
    await AiChatStore.deleteConversation(conversationId)

    ElMessage.success('删除成功')
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败，请重试')
  }
}
</script>

<style scoped>
.side-nav {
  border-right: none;
  height: 100%;
}

.conversation-title {
  flex: 1;
  font-size: 14px;
}

.delete-icon {
  color: #909399;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
  opacity: 0.5;
}

.delete-icon:hover {
  color: #f56c6c;
  background-color: #fef0f0;
  opacity: 1;
}

/* 确保鼠标悬停在整行时显示删除图标 */
.history-item:hover .delete-icon {
  opacity: 0.8;
}

:deep(.el-menu-item) {
  display: flex;
  align-items: center;
}

.delete-confirm-dialog .el-message-box__status {
  color: #f56c6c;
}

.delete-confirm-dialog .el-message-box__message {
  text-align: center;
}
</style>
