import { ref } from 'vue'
import { defineStore } from 'pinia'
import { login, register, logout, refreshTokenAPI } from '@/api/auth/index'
import type { LoginParams, RegisterParams, UserInfo } from './types'
import { jwtDecode } from 'jwt-decode'

interface JwtPayload {
  exp: number
  iat: number
  jti: string
  token_type: string
  user_id: string
}

/**
 *  认证的Store, 后续可以优化token刷新的逻辑
 */
export const useAuthStore = defineStore(
  'auth',
  () => {
    // State
    const access_token = ref<string | null>(localStorage.getItem('access_token'))
    const refresh = ref<string | null>(localStorage.getItem('refresh'))
    const userInfo = ref<UserInfo | null>(null)
    const refreshTimeout = ref<number | null>(null)
    const refreshTokenTimeout = ref<number>(0)

    const getUserInfo = () => {
      return userInfo.value
    }

    const getAccessToken = () => {
      return access_token.value
    }

    // 解析 JWT 获取过期时间
    const getTokenExpiration = (token: string): number => {
      try {
        const decoded = jwtDecode<JwtPayload>(token)
        return decoded.exp
      } catch (e) {
        console.error('Invalid token', e)
        return 0
      }
    }

    // 计算剩余事件(秒)
    const getRemainingTime = (exp: number): number => {
      return Math.max(0, exp - Math.floor(Date.now() / 1000))
    }

    // 设置tokens 并持久化
    const setToken = (tokens: { access_token: string; refresh?: string }) => {
      access_token.value = tokens.access_token

      // 持久化到 localStorage
      localStorage.setItem('access_token', tokens.access_token)

      if (tokens.refresh) {
        refresh.value = tokens.refresh
        localStorage.setItem('refresh', tokens.refresh)
        refreshTokenTimeout.value = getTokenExpiration(tokens.refresh)
      }

      // 设置自动刷新
      const exp = getTokenExpiration(tokens.access_token)
      scheduleRefresh(getRemainingTime(exp))
    }

    // 自动刷新逻辑
    const scheduleRefresh = (remainingTime: number) => {
      if (refreshTimeout.value) {
        clearTimeout(refreshTimeout.value)
      }

      if (remainingTime <= 0) {
        resetState()
        return
      }

      // 在 token 过期前5分钟刷新
      const refreshTime = Math.max(0, remainingTime - 300) * 1000
      refreshTimeout.value = window.setTimeout(refreshToken, refreshTime)
    }

    // 刷新toekn
    const refreshToken = async () => {
      try {
        if (getRemainingTime(refreshTokenTimeout.value) <= 1000) {
          resetState()
          return
        }

        const res = await refreshTokenAPI({ refresh: refresh.value })

        setToken({
          access_token: res.access,
        })
      } catch (error) {
        console.log('刷新token失败', error)
        resetState()
      }
    }

    // Actions
    const loginAction = async (params: LoginParams) => {
      try {
        const res = await login(params)
        setToken(res.token)
        userInfo.value = res.userInfo
        return true
      } catch (error) {
        resetState()
        throw error
      }
    }

    const registerAction = async (params: RegisterParams) => {
      try {
        const res = await register(params)
        return res.userInfo
      } catch (error) {
        throw error
      }
    }

    const logoutAction = async (router) => {
      await logout()
      resetState()
      router.push('/login')
    }

    // 初始化检查
    const init = () => {
      if (access_token.value) {
        const exp = getTokenExpiration(access_token.value)
        const remainingTime = getRemainingTime(exp)

        if (remainingTime > 0) {
          scheduleRefresh(remainingTime)
        } else {
          refreshToken()
        }
      }
    }

    // 重置状态
    const resetState = () => {
      access_token.value = null
      refresh.value = null
      userInfo.value = null

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')

      if (refreshTimeout.value) {
        clearTimeout(refreshTimeout.value)
        refreshTimeout.value = null
      }
    }

    // 初始化
    init()

    return {
      access_token,
      refresh,
      userInfo,
      getAccessToken,
      getUserInfo,
      loginAction,
      registerAction,
      logoutAction,
      resetState,
    }
  },
  {
    persist: true,
  },
)
