import request from '@/api/request'
import { AIASSISTANT_API } from '../constants'
import * as Types from './types'

// 会话创建
export const chatCreate = (
  data: Types.CreateRequestParams,
): Promise<Types.CreateResponseParams> => {
  return request.post(AIASSISTANT_API.CREATE, data)
}

// 会话列表
export const chatList = (): Promise<Types.ListResponseParams> => {
  return request.get(AIASSISTANT_API.LIST)
}

// 会话更新
export const chatUpdate = (
  id: number,
  data: Types.UpdateResponseParams,
): Promise<Types.UpdateResponseParams> => {
  return request.put(`${AIASSISTANT_API.UPDATE}${id}/`, data)
}

// 会话删除
export const chatDelete = (id: number) => {
  return request.delete(`${AIASSISTANT_API.DELETE}${id}/`)
}

// 发送聊天信息
export const chat = (data: Types.ChatRequestParams): Promise<Types.ChatResponseParams> => {
  return request.post(AIASSISTANT_API.CHAT, data, { timeout: 180 * 1000 })
}

// 获取会话信息
export const getMessages = (conversation_id: number): Promise<Types.MessagesResponstParams> => {
  return request.get(`${AIASSISTANT_API.MESSAGES}${conversation_id}/`)
}
