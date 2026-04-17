import { ref } from 'vue'
import { defineStore } from 'pinia'
import * as api from '@/api/aiAssistant/index'
import * as types from './types'

export const useAiChatStore = defineStore('aiChat', () => {
  // state
  const conversations = ref<number[]>([]) //全部会话ID
  const conversationsInfo = ref<Record<number, { title: string }>>({}) //全部会话的基本信息
  const activeConversations = ref<number>() //当前激活的会话
  const messagesMap = ref<Record<number, { content: types.MessageContent }[]>>({}) //激活过的会话的全部message历史信息
  const isReply = ref(false)

  // 获取当前激活的会话
  const getActiveConversation = () => {
    return activeConversations.value
  }

  // 获取全部会话列表
  const getConversations = () => {
    return conversations.value
  }

  // 获取会话详细信息
  const getconversationsInfo = () => {
    return conversationsInfo.value
  }

  // 获取当前激活的会话的历史信息
  const getMessagesMap = () => {
    if (!activeConversations.value) return []
    return messagesMap.value[activeConversations.value] || []
  }

  const setIsReply = (data: boolean) => {
    isReply.value = data
  }

  const getIsReply = () => {
    return isReply.value
  }

  async function loadConversations() {
    try {
      const data = await api.chatList()
      conversations.value = data.results.map((item) => item.id)
      // 构建会话信息字典
      const infoDict: Record<number, { title: string }> = {}
      data.results.forEach((item) => {
        infoDict[item.id] = {
          title: item.title,
        }
      })
      conversationsInfo.value = infoDict
      return data
    } catch (error) {
      console.log(error)
    }
  }

  async function setActiveConversation(id: number) {
    activeConversations.value = id
    if (!messagesMap.value[id]) {
    }
  }

  async function loadMessages(id: number) {
    try {
      const data = await api.getMessages(id)
      messagesMap.value[id] = data.results
      return data
    } catch (error) {
      console.log(error)
    }
  }

  async function createConversation(params: types.CreateRequestParams) {
    try {
      const data = await api.chatCreate(params)
      conversationsInfo.value[data.id] = { title: data.title }
      conversations.value.unshift(data.id)
      setActiveConversation(data.id)
      return data
    } catch (error) {
      console.log(error)
    }
  }

  async function updateConversation(id: number, params: types.UpdateRequestParams) {
    try {
      const data = await api.chatUpdate(id, params)
      conversationsInfo.value[id] = { title: data.title }
      return data
    } catch (error) {
      console.log(error)
    }
  }

  async function deleteConversation(id: number) {
    try {
      const data = await api.chatDelete(id)
      conversations.value = conversations.value.filter((convId) => convId !== id)
      delete conversationsInfo.value[id]
      delete messagesMap.value[id]
      return data
    } catch (error) {
      console.log(error)
    }
  }

  async function chat(params: types.ChatRequestParams) {
    try {
      isReply.value = true
      if (!messagesMap.value[params.conversation_id]) {
        messagesMap.value[params.conversation_id] = []
      }

      messagesMap.value[params.conversation_id].push({
        content: params.message[0],
      })
      const data = await api.chat(params)
      messagesMap.value[params.conversation_id].push({
        content: {
          role: 'assistant',
          content: data.message,
        },
      })
      isReply.value = false
      return data
    } catch (error) {
      console.log(error)
    } finally {
      isReply.value = false
    }
  }

  return {
    getActiveConversation,
    getConversations,
    getconversationsInfo,
    getMessagesMap,
    setIsReply,
    getIsReply,
    loadConversations,
    setActiveConversation,
    loadMessages,
    createConversation,
    updateConversation,
    deleteConversation,
    chat,
  }
})
