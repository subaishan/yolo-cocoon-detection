import axios from 'axios'
import { useAuthStore } from '@/stores/modules/auth'
import { AUTH_API } from './constants'

// 创建axios实例
const service = axios.create({
  // 公共接口
  baseURL: 'http://localhost:8000/',
  timeout: 10 * 1000, // 超时时间
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.access_token) {
      config.headers.Authorization = `Bearer ${authStore.access_token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// 设置cross跨域 并设置访问权限 允许跨域携带cookie信息,使用JWT可关闭
// service.defaults.withCredentials = false

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // 非2xx状态码进入
    const { config, response } = error

    // 处理网络错误（如超时）的情况
    if (!response) {
      console.error('网络错误:', error.message, error.code)
      return Promise.reject({
        message: error.message,
        code: error.code,
        isAxiosError: true,
        isNetworkError: true, // 添加一个标识表示是网络错误
      })
    }

    // 如果是登录接口且返回401，不进行统一跳转
    if (config.url === AUTH_API.LOGIN && response.status === 401) {
      return Promise.reject({
        status: response.status,
        data: response.data,
        isAxiosError: true,
      })
    }

    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.resetState()
    }
    console.log(error)
    console.log(response)
    return Promise.reject({
      status: response.status,
      data: response.data,
      isAxiosError: true,
    })
  },
)
export default service
