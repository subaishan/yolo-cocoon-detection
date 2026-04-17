<!-- src/components/HeaderCon.vue -->
<template>
  <div class="header-Con">
    <div class="header-left">
      <h1>智慧桑蚕病虫害监测平台</h1>
    </div>
    <div class="header-right">
      <el-dropdown trigger="click" @command="handleCommand">
        <div class="user-avatar">
          <div class="user-info">
            <el-avatar :size="36" :src="userInfo.avatar"></el-avatar>
            <span class="user-name">{{ userInfo.nickname }}</span>
          </div>
        </div>

        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">个人中心</el-dropdown-item>
            <el-dropdown-item command="setting">系统设置</el-dropdown-item>
            <el-dropdown-item command="logout" :icon="SwitchButton" @@click.prevent="logout">
              退出登陆
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { SwitchButton } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/modules/auth/'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()
const userInfo = authStore.getUserInfo()

const handleCommand = async (command) => {
  if (command === 'logout') {
    await logout()
  }
}

const logout = async () => {
  try {
    await authStore.logoutAction(router)
  } catch (errors) {
    router.push('login')
    const data = errors.data
    const defaultMsg = data?.errors || '退出失败'
    ElMessage.error(defaultMsg)
  }
}
</script>

<style scoped>
.header-Con {
  background-color: var(--color-header-bg);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0px;
  height: 60px;
}

.header-left {
  display: flex;
  align-items: center;

  h1 {
    padding-left: 20px;
    margin: 0;
    font-size: 25px;
    font-weight: 500;
    color: var(--color-header-title);
  }
}

.header-right {
  padding-right: 20px;
  .user-avatar {
    cursor: pointer;

    .user-info {
      display: flex;
      align-items: center;
      gap: 8px;

      .user-name {
        font-size: 20px;
        font-weight: 500;
        color: var(--color-header-avatar);
      }

      .el-icon--right {
        margin-left: 4px;
        transition: transform 0.3s;
      }
    }

    &:hover {
      .el-icon--right {
        transform: rotate(180deg);
      }
    }
  }
}
</style>
