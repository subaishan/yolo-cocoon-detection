<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import { useAuthStore } from '@/stores/modules/auth/'
import { User, Lock, Message, Iphone } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

// 定义控制变量
const isRegister = ref(1) //判定是否为注册表单
const form = ref() // 接受组件对象

const passwordError = ref(false)
const emailExists = ref(false) // 判定邮箱是否存在
const phoneExists = ref(false) // 判定手机号是否被绑定
const errorMessage = ref('')

const userInfo = ref(null)

// 登陆form数据对象
const loginModel = ref({
  username: '',
  password: '',
})

// 注册form数据对象
const registerModel = ref({
  password1: '',
  password2: '',
  email: '',
  nickname: '',
  phone: '',
  avatar: null,
})

// 处理头像更改的情况
const handleAvatarChange = () => {
  return
}

// 校验规则
const logRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 6, max: 35, message: '用户名长度在6-35个字符之间', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9@.+]+$/, message: '用户名只能包含字母、数字和.+@', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value && passwordError.value) {
          callback(new Error('账号或密码错误'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, max: 15, message: '密码长度在8-15个字符之间', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value && passwordError.value) {
          callback(new Error('账号或密码错误'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
})

const regRules = reactive({
  password1: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, max: 15, message: '密码长度在8-15个字符之间', trigger: 'blur' },
  ],
  password2: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { min: 8, max: 15, message: '密码长度在8-15个字符之间', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerModel.value.password1) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: ['blur', 'change'] },
    {
      validator: (rule, value, callback) => {
        if (value && emailExists.value) {
          callback(new Error('该邮箱已注册'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
  nickname: [{ max: 15, message: '昵称长度不能超过15个字符', trigger: 'blur' }],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value && phoneExists.value) {
          callback(new Error('该手机号已注册'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
})

// 登陆
const login = async () => {
  try {
    passwordError.value = false
    await authStore.loginAction({
      username: loginModel.value.username,
      password: loginModel.value.password,
    })
    router.push('home') // 跳转到首页
  } catch (errors) {
    handleLoginError(errors)
  }
}

// 注册
const register = async () => {
  try {
    emailExists.value = false
    phoneExists.value = false

    userInfo.value = await authStore.registerAction(registerModel.value)
    console.log(userInfo.value)
    isRegister.value = 3
  } catch (errors) {
    handleRegisterError(errors)
  }
}

const handleRegisterError = (errors) => {
  const defaultMsg = '注册失败'

  const { status, data } = errors
  switch (status) {
    case 409:
      if (data?.errors?.email?.code == 'email_exists') {
        emailExists.value = true
        console.log('设置ture')
        form.value.validateField('email')
      }
      if (data?.errors?.phone?.code == 'phone_exists') {
        phoneExists.value = true
        form.value.validateField('phone')
      }
      ElMessage.error(defaultMsg)
      break
    case 429:
      ElMessage.error('尝试次数过多,请稍后再试')
      break
    default:
      ElMessage.error(defaultMsg)
  }
}

const handleLoginError = (errors) => {
  passwordError.value = true
  const defaultMsg = '登陆失败'

  const { status, data } = errors
  switch (status) {
    case 401:
      if (data?.errors?.user?.code == 'not_find') {
        form.value.validateField('username')
        form.value.validateField('password')
      } else {
        ElMessage.error(defaultMsg)
      }

      break
    case 429:
      ElMessage.error('尝试次数过多,请稍后再试')
      break
    default:
      ElMessage.error(defaultMsg)
  }
}

//切换的时候重置表单
watch(isRegister, () => {
  loginModel.value = {
    username: '',
    password: '',
  }
  registerModel.value = {
    password1: '',
    password2: '',
    email: '',
    nickname: '',
    phone: '',
    avatar: null,
  }
  passwordError.value = false
  errorMessage.value = ''
  phoneExists.value = false
  emailExists.value = false
})
</script>

<template>
  <el-row class="login-page">
    <el-col :span="24" :offset="12" class="form">
      <h1 style="margin-bottom: 100px; font-size: 50px">智慧桑蚕平虫害监测平台</h1>
      <!-- 注册表单 -->
      <el-form
        :model="registerModel"
        ref="form"
        large="large"
        class="login-container"
        :rules="regRules"
        autocomplete="off"
        v-if="isRegister == 2"
      >
        <el-form-item>
          <h1>注册</h1>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="registerModel.email"
            placeholder="请输入邮箱"
            :prefix-icon="Message"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password1">
          <el-input
            :prefix-icon="Lock"
            type="password"
            placeholder="请输入密码"
            v-model="registerModel.password1"
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="password2">
          <el-input
            v-model="registerModel.password2"
            placeholder="请输入确认密码"
            :prefix-icon="Lock"
            type="password"
          ></el-input>
        </el-form-item>
        <el-form-item label="网名" prop="nickname">
          <el-input
            v-model="registerModel.nickname"
            placeholder="请输入名称"
            type="text"
            :prefix-icon="User"
          ></el-input>
        </el-form-item>
        <el-form-item label="手机" prop="phone">
          <el-input
            v-model="registerModel.phone"
            placeholder="请输入手机号"
            :prefix-icon="Iphone"
          ></el-input>
        </el-form-item>
        <el-form-item label="头像" prop="avatar">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :auto-upload="false"
            :on-change="handleAvatarChange"
            accept="image/*"
          >
            <img v-if="registerModel.avatar" :src="registerModel.avatar" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <el-button @click="register" class="button" type="success" auto-insert-space>
            注册
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-link type="info" target="_blank" :underline="false" @click="isRegister = 1"
            >返回</el-link
          >
        </el-form-item>
      </el-form>
      <!--登陆表单-->
      <el-form
        ref="form"
        :model="loginModel"
        class="login-container"
        size="large"
        :rules="logRules"
        autocomplete="off"
        v-else-if="isRegister == 1"
      >
        <el-form-item label="账号" prop="username">
          <el-input
            placeholder="请输入用户名或邮箱"
            v-model="loginModel.username"
            :prefix-icon="User"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginModel.password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            type="password"
          ></el-input>
        </el-form-item>
        <el-form-item class="flex">
          <div class="flex">
            <el-checkbox>记住我</el-checkbox>
            <el-link type="info" :underline="false">忘记密码？</el-link>
          </div>
        </el-form-item>
        <!--  -->
        <el-form-item>
          <el-button @click="login" class="button" type="success" auto-insert-space>
            登录
          </el-button>
        </el-form-item>
        <!--  -->
        <el-form-item class="flex">
          <el-link type="info" :underline="false" @click="isRegister = 2"> 注册 → </el-link>
        </el-form-item>
      </el-form>

      <el-form ref="form" :mode="UserInfoModel" size="large" v-else-if="isRegister == 3">
        <el-form-item label="用户名">注册成功,用户名为 {{ userInfo.username }} </el-form-item>
        <el-form-item class="flex">
          <el-link type="info" :underline="false" @click="isRegister = 1"> 返回登陆 </el-link>
        </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>

<style scoped></style>
