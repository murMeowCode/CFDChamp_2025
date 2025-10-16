import { defineStore } from 'pinia'
import { push } from 'notivue'

export const useUseNotificationsStore = defineStore('notifications', () => {
  
  // Успешные уведомления
  const success = (message, title = 'Успешно') => {
    push.success({
      title,
      message,
      duration: 3000
    })
  }

  // Ошибки
  const error = (message, title = 'Ошибка') => {
    push.error({
      title,
      message,
      duration: 5000
    })
  }

  // Предупреждения
  const warning = (message, title = 'Внимание') => {
    push.warning({
      title,
      message,
      duration: 4000
    })
  }

  // Информационные
  const info = (message, title = 'Информация') => {
    push.info({
      title,
      message,
      duration: 4000
    })
  }

  // Загрузка
  const loading = (message, title = 'Загрузка') => {
    return push.promise({
      title,
      message,
      duration: 0 // Бесконечно пока не вызовем success/error
    })
  }

  const api = {
    success: (message = 'Операция выполнена успешно') => success(message),
    error: (message = 'Произошла ошибка') => error(message),
    loading: (message = 'Выполняется запрос...') => loading(message)
  }

  return {
    success,
    error,
    warning,
    info,
    loading,
    api
  }
})