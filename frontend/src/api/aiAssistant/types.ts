export interface CreateRequestParams {
  title: string
}

export interface CreateResponseParams {
  id: number
  title: string
}

export interface ListResponseParams {
  count: number
  next: string
  previous: string
  results: {
    id: number
    title: string
  }[]
}

export interface UpdateRequestParams {
  title: string
}

export interface UpdateResponseParams {
  title: string
}

export interface ChatRequestParams {
  message: {
    role: string
    content: string
  }[]
  conversation_id: number
}

export interface ChatResponseParams {
  message: string
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

export interface MessagesResponstParams {
  count: number
  next: string
  previous: string
  results: {
    content: MessageContent
  }[]
}
