import NotFound from '@/components/NotFound/NotFound.vue'
import MyLogin from '@/views/Auth/MyLogin.vue'
import MyRegistration from '@/views/Auth/MyRegistration.vue'
import Mycabinet from '@/views/Cabinet/Mycabinet.vue'
import MyForgotPassword from '@/views/Forgot/MyForgotPassword.vue'
import Home from '@/views/Home/Home.vue'
import One from '@/views/One/One.vue'
import Three from '@/views/Three/Three.vue'
import Two from '@/views/Two/Two.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/one',
      name: 'one',
      component: One,
    },
    {
      path: '/two',
      name: 'two',
      component: Two,
    },
    {
      path: '/three',
      name: 'three',
      component: Three,
    },
    {
      path: '/authentification',
      name: 'auth',
      component: MyRegistration,
    },
    {
      path: '/login',
      name: 'login',
      component: MyLogin,
    },
    {
      path: '/profile',
      name: 'profile',
      component: Mycabinet,
    },
    {
      path: '/forgot-password',
      name: 'forgot',
      component: MyForgotPassword,
    },
    {
      path: '/:any(.*)',
      name: 'e404',
      component: NotFound,
    },
  ],
})

export default router
