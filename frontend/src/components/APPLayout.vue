<!-- src/components/APPLayout.vue -->
<template>
  <div class="common-layout">
    <el-container>
      <el-header><HeaderCon /></el-header>
      <el-container>
        <el-aside width="200px"><SideNav /></el-aside>
        <el-main>
          <div class="router-view-container">
            <router-view />
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import HeaderCon from './HeaderCon.vue'
import SideNav from './SideNav.vue'
</script>

<style>
.common-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.common-layout .el-container {
  flex: 1;
  height: calc(100vh - 60px); /* 减去头部高度 */
}

.common-layout .el-header {
  padding: 0px;
  height: 60px !important; /* 固定头部高度 */
  flex-shrink: 0;
}

.common-layout .el-aside {
  background-color: var(--el-menu-bg-color);
  border-right: 1px solid var(--el-border-color-light);
  height: 100%;
}

.common-layout .el-main {
  padding: 0px;
  background-color: var(--el-bg-color-page);
  overflow: hidden; /* 防止溢出 */
}

.common-layout .router-view-container {
  height: 100%;
  width: 100%;
  overflow: hidden;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
