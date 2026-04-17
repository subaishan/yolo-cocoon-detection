// 后端路径常量
export const AUTH_API = {
  LOGIN: '/accounts/login/',
  REGISTER: '/accounts/register/',
  LOGOUT: '/accounts/logout/',
  GET_TOKEN: '/accounts/token/',
  REFRESH_TOKEN: '/accounts/token/refresh/',
} as const

export const AIASSISTANT_API = {
  CREATE: 'ai/chat/create/',
  LIST: 'ai/chat/list/',
  UPDATE: 'ai/chat/update/',
  DELETE: 'ai/chat/delete/',
  CHAT: 'ai/chat/',
  MESSAGES: 'ai/chat/list/messages/',
}

export const IMAGEDETECTION_API = {
  CREATE: 'detection/create/',
  LIST: 'detection/list/',
  DELETE: 'detection/delete/',
  RETRIEVE: 'detection/retrieve/',
}
