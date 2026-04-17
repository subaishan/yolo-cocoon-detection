import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import APPLayout from '@/components/APPLayout.vue'
import LoginView from '@/views/LoginView.vue'
import DashBoard from '@/views/DashBoard.vue'
import { useAuthStore } from '@/stores/modules/auth'
import component from 'element-plus/es/components/tree-select/src/tree-select-option.mjs'

const routes = [
  {
    path: '/',
    component: APPLayout,
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        path: 'home',
        name: 'home',
        component: () => import('@/views/HomeView.vue'),
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('@/views/DashBoard.vue'),
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: 'diseasedetection',
        name: 'diseasedetection',
        component: () => import('@/views/DiseaseDetection/DiseaseDetection.vue'),
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: 'detectionhistory',
        name: 'detectionhistory',
        component: () => import('@/views/DiseaseDetection/DetectionHistory.vue'),
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: 'assistantchat',
        name: 'assistantchat',
        component: () => import('@/views/Assistant/AssistantChat.vue'),
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: 'assistanthistory/:conversationId/:isCreate?',
        name: 'assistanthistory',
        component: () => import('@/views/Assistant/AssistantHistory.vue'),
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: 'about',
        name: 'about',
        component: () => import('@/views/AboutView.vue'),
        meta: {
          requiresAuth: true,
        },
      },
    ],
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: {
      requiresAuth: false,
    },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.access_token) {
    next('/login')
  } else {
    next()
  }
})

export default router
