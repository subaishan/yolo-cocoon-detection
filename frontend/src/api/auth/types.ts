// 登录参数
export interface LoginParams {
  username: string
  password: string
  captcha?: string // 可选验证码
}

// 登录响应
export interface LoginResponse {
  success: boolean
  message: string
  userInfo: {
    username: string
    nickname: string
    avatar: string
  }
  token: {
    access_token: string
    refresh: string
  }
}

// 注册参数
export interface RegisterParams {
  email: string
  password1: string
  password2: string
  nickname: string
  phone?: string
}

// 注册响应
export interface RegisterResponse {
  success: boolean
  message: string
  userInfo: {
    username: string
    nickname: string
  }
}
export interface refreshTokenParams {
  refresh: string | null
}

export interface refreshTokenResponse {
  access: string
  refresh: string
}

export interface getTokenParams {
  username: string
  password: string
}
