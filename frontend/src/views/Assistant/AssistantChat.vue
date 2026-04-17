<template>
  <div class="page-container">
    <!-- 聊天消息区域 -->
    <div class="chat-area">
      <div class="chat-container">
        <!-- 空状态 -->
        <div class="empty-state">
          <el-icon :size="60"><ChatRound /></el-icon>
          <p>还没有消息，开始对话吧！</p>
        </div>
      </div>
    </div>

    <!-- 固定在底部的输入区域 -->
    <div class="input-area">
      <div class="input-container">
        <el-input
          v-model="input"
          :rows="3"
          size="large"
          type="textarea"
          placeholder="给智能助手发消息"
          class="input-context"
          @keyup.enter="sendMessage"
        />
        <div class="input-button">
          <el-button size="large" type="primary" :icon="Top" circle @click="sendMessage" />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { Top } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import { useAiChatStore } from '@/stores/modules/aiAssistant/index'

const router = useRouter()
const AiChatStore = useAiChatStore()
const conversationId = ref()
const input = ref('')

const sendMessage = async () => {
  try {
    if (!input.value.trim()) return

    const messageContent = input.value.trim()
    input.value = '' // 清空输入框

    const createParams = {
      title: messageContent,
    }

    const data = await AiChatStore.createConversation(createParams)

    conversationId.value = data.id

    const chatParams = {
      message: [{ role: 'user', content: messageContent }],
      conversation_id: conversationId.value,
    }

    router.push(`/assistanthistory/${conversationId.value}/t`)

    await AiChatStore.chat(chatParams)
  } catch (error) {
    console.log(error)
  }
}
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 0;
}

/* 聊天区域 - 占据剩余空间 */
.chat-area {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  min-height: 0; /* 重要：允许flex容器收缩 */
}

.messages-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 10px 0;
  min-height: 0; /* 重要：允许flex容器收缩 */
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
}

/* 消息样式保持不变... */
.message-row {
  margin-bottom: 20px;
}

.assistant-message {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  justify-content: flex-start;
}

.user-message {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  justify-content: flex-end;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 8px;
  word-wrap: break-word;
}

.user-content {
  background-color: #e3eaff;
  color: black;
  border-top-right-radius: 2px;
}

.assistant-content {
  background-color: #e5e5e5;
  color: black;
  border: 1px solid #ebeef5;
  border-top-left-radius: 2px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message-text {
  line-height: 1.6;
}

.avatar {
  flex-shrink: 0;
}

.loading-message .message-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 输入区域 - 固定高度 */
.input-area {
  flex-shrink: 0;
  padding: 16px 20px;
  background: white;
  border-top: 1px solid #ebeef5;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.input-container {
  max-width: 100%;
  margin: 0 auto;
}

.input-button {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}

:deep(.input-context .el-textarea__inner) {
  font-size: 16px;
  resize: none;
  line-height: 1.5;
}

:deep(.input-button .el-button) {
  width: 48px;
  height: 48px;
}

:deep(.input-button .el-icon) {
  font-size: 20px;
}

/* 确保路由视图容器正确显示 */
.common-layout .el-main {
  padding: 0 !important;
  display: flex;
  flex-direction: column;
}

.common-layout .router-view-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 确保滚动条正常工作 */
.messages-wrapper::-webkit-scrollbar {
  width: 6px;
}

.messages-wrapper::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.messages-wrapper::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.messages-wrapper::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
