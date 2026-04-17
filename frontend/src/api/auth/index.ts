import request from '@/api/request'
import type {
  LoginParams,
  LoginResponse,
  RegisterParams,
  RegisterResponse,
  refreshTokenParams,
  getTokenParams,
  refreshTokenResponse,
} from './types'
import { AUTH_API } from '../constants'

// 用户登录
export const login = (data: LoginParams): Promise<LoginResponse> => {
  return request.post(AUTH_API.LOGIN, data)
}

// 用户注册
export const register = (data: RegisterParams): Promise<RegisterResponse> => {
  return request.post(AUTH_API.REGISTER, data)
}

// 用户登出
export const logout = () => {
  return request.post(AUTH_API.LOGOUT)
}

// 获得token
export const getTokenAPI = (data: getTokenParams) => {
  return request.post(AUTH_API.GET_TOKEN, data)
}

// token刷新
export const refreshTokenAPI = (data: refreshTokenParams): Promise<refreshTokenResponse> => {
  return request.post(AUTH_API.REFRESH_TOKEN, data)
}
