import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useUserStore } from './useUserStore'
import { useApiMutations } from '@/utils/api/useApiMutation'
import { apiLogin, apiRegistr } from '@/main'

export const useAuthStore = defineStore('auth', () => {
  const accsesstoken = ref(localStorage.getItem('jwtTokenAccsess'))
  const refreshtoken = ref(localStorage.getItem('jwtTokenRefresh'))
  const userStore = useUserStore()

  // Добавляем мутации
  const { usePost } = useApiMutations()

  // Мутация для регистрации
  const registerMutation = usePost(apiRegistr, {
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
  const loginMutation = usePost(apiLogin, {
    onSuccess: (data) => {
      console.log('✅ Логин успешен:', data.tokens)

      if (data.tokens.access_token && data.tokens.refresh_token) {
        setAccsessToken(data.tokens.access_token)
        setRefreshToken(data.tokens.refresh_token)
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
    console.log(newToken,'token')
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

  try {
    const response = await fetch('http://10.0.219.6:8000/auth/refresh', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${refreshtoken.value}`
      },
      body: JSON.stringify({
        refresh_token: refreshtoken.value
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    
    // Предполагаем, что API возвращает новые токены в таком формате
    if (data.access_token && data.refresh_token) {
      setAccsessToken(data.access_token)
      setRefreshToken(data.refresh_token)
      console.log('✅ Токены успешно обновлены')
      return true
    } else {
      throw new Error('Неверный формат ответа от сервера')
    }
    
  } catch (error) {
    console.error('❌ Ошибка обновления токенов:', error)
    stopTokenRefresh()
    
    // Можно добавить логику для выхода пользователя при неудачном обновлении
    // logoutUser()
    
    return false
  }
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
