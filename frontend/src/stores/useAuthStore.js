import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useUserStore } from './useUserStore'
import { useApiMutations } from '@/utils/api/useApiMutation'

export const useAuthStore = defineStore('auth', () => {
  const accsesstoken = ref(localStorage.getItem('jwtTokenAccsess'))
  const refreshtoken = ref(localStorage.getItem('jwtTokenRefresh'))
  const userStore = useUserStore()

  // Добавляем мутации
  const { usePost } = useApiMutations()

  // Мутация для регистрации
  const registerMutation = usePost('auth/register/', {
    onSuccess: (data) => {
      console.log('✅ Регистрация успешна:', data)

      // Если бэкенд возвращает токены при регистрации
      if (data.access && data.refresh) {
        setAccsessToken(data.access)
        setRefreshToken(data.refresh)
        startTokenRefresh()
      }

      // Если бэкенд возвращает данные пользователя
      if (data.user) {
        userStore.setUser(data.user)
      }
    },
    onError: (error) => {
      console.error('❌ Ошибка регистрации:', error)
    },
  })

  // Мутация для логина
  const loginMutation = usePost('auth/login/', {
    onSuccess: (data) => {
      console.log('✅ Логин успешен:', data)

      if (data.access && data.refresh) {
        setAccsessToken(data.access)
        setRefreshToken(data.refresh)
        startTokenRefresh()
      }

      if (data.user) {
        userStore.setUser(data.user)
      }
    },
    onError: (error) => {
      console.error('❌ Ошибка логина:', error)
    },
  })

  // Существующие функции
  function setAccsessToken(newToken) {
    accsesstoken.value = newToken
    localStorage.setItem('jwtTokenAccsess', newToken)
  }

  function setRefreshToken(newToken) {
    refreshtoken.value = newToken
    localStorage.setItem('jwtTokenRefresh', newToken)
  }

  function removeToken() {
    accsesstoken.value = null
    refreshtoken.value = null
    localStorage.removeItem('jwtTokenAccsess')
    localStorage.removeItem('jwtTokenRefresh')
  }

  let refreshInterval = null

  async function refreshTokens() {
    if (!accsesstoken.value || !refreshtoken.value) {
      stopTokenRefresh()
      return false
    }

    return new Promise((resolve) => {
      console.log('---------------------------------------------------')
      setAccsessToken('accsess' + Date.now())
      setRefreshToken('refresh' + Date.now())
      resolve(true)
    })
  }

  function startTokenRefresh() {
    if (refreshInterval) {
      clearInterval(refreshInterval)
    }
    refreshTokens().then(() => {
      refreshInterval = setInterval(refreshTokens, 30000)
    })
  }

  function stopTokenRefresh() {
    if (refreshInterval) {
      clearInterval(refreshInterval)
      refreshInterval = null
    }
  }

  // Авто-старт при наличии токенов
  if (accsesstoken.value && refreshtoken.value) {
    startTokenRefresh()
  } else {
    stopTokenRefresh()
  }

  function logout() {
    stopTokenRefresh()
    removeToken()
    userStore.removeUser()
  }

  // Новые методы с использованием мутаций
  const register = async (userData) => {
    return await registerMutation.mutateAsync(userData)
  }

  const login = async (credentials) => {
    return await loginMutation.mutateAsync(credentials)
  }

  // Старый метод login (оставляем для обратной совместимости)
  async function legacyLogin(url, formstate, mode) {
    return new Promise((resolve) => {
      setTimeout(() => {
        setAccsessToken('accsess')
        setRefreshToken('refresh')
        startTokenRefresh()
        resolve(true)
      }, 3000)
    })
  }

  // Вычисляемые свойства
  const getTokenAccsess = computed(() => accsesstoken.value)
  const getTokenRefresh = computed(() => refreshtoken.value)
  const isAuth = computed(() => !!accsesstoken.value && !!refreshtoken.value)

  // Добавляем computed для состояния мутаций
  const isRegisterLoading = computed(() => registerMutation.isPending.value)
  const isLoginLoading = computed(() => loginMutation.isPending.value)

  return {
    // Состояние
    logout,
    accsesstoken,
    refreshtoken,

    // Мутации (для прямого доступа в компонентах)
    registerMutation,
    loginMutation,

    // Методы
    setAccsessToken,
    removeToken,
    register,
    login,
    legacyLogin,
    setRefreshToken,

    // Геттеры
    getTokenAccsess,
    getTokenRefresh,
    isAuth,
    isRegisterLoading,
    isLoginLoading,
  }
})
