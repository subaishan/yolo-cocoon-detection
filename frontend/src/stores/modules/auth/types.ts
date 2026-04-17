// API 相关类型
export interface LoginParams {
  username: string
  password: string
  rememberMe?: boolean
}

export interface RegisterParams {
  email: string
  password1: string
  password2: string
  nickname: string
  phone: string
}

export interface AuthResponse {
  userInfo: {
    username: string
    nickname: string
  }
  token: {
    access_token: string
    refresh: string
  }
}

// Store 状态类型
export interface UserInfo {
  username: string
  nickname: string
  avatar: string
}


