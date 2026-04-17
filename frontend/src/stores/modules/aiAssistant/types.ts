export interface CreateRequestParams {
  title: string
}

export interface UpdateRequestParams {
  title: string
}

export interface ChatRequestParams {
  message: MessageContent[]
  conversation_id: number
}

export interface MessageContent {
  role: 'user' | 'assistant'
  content: string
  audio?: string | null
  refusal?: string | null
  tool_calls?: string[] | null
  annotations?: string[] | null
  function_call?: string | null
}
