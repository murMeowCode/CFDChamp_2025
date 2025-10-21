import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApiGet } from '@/utils/api/useApiGet'

const { useGet } = useApiGet()

export const useDashboardStore = defineStore('dashboard', () => {
  // State
  const loading = ref(false)
  const statsData = ref([])
  const chartsData = ref([])
  const tablesData = ref([])
  const recentActivities = ref([])
  const lastUpdated = ref(null)
  const error = ref(null)

  // Getters
  const getStats = computed(() => statsData.value)
  const getCharts = computed(() => chartsData.value)
  const getTables = computed(() => tablesData.value)
  const getActivities = computed(() => recentActivities.value)
  const getLastUpdated = computed(() => lastUpdated.value)
  const isLoading = computed(() => loading.value)
  const getError = computed(() => error.value)

  // API Queries
  const {
    data: dashboardData,
    isPending: isDashboardLoading,
    isSuccess: isDashboardSuccess,
    error: dashboardError,
    execute: fetchDashboardData
  } = useGet(
    `http://192.168.1.128:8000/statistics/dashboard`
  )

  // Обработка данных с сервера
  const processDashboardData = (apiData) => {
    try {
      // Предполагаемая структура ответа API
      // Адаптируйте под реальную структуру вашего API
      const { stats, charts, tables, activities } = apiData

      // Обработка статистики
      statsData.value = stats?.map(item => ({
        value: item.value?.toString() || '0',
        label: item.label || 'Неизвестно',
        icon: getIconByType(item.type),
        type: getTypeByValue(item.value),
        trend: item.trend ? {
          value: item.trend.value,
          direction: item.trend.direction
        } : undefined
      })) || []

      // Обработка графиков
      chartsData.value = charts?.map(chart => ({
        title: chart.title || 'График',
        type: chart.type || 'line',
        data: chart.data || getDefaultChartData(chart.type)
      })) || []

      // Обработка таблиц
      tablesData.value = tables?.map(table => ({
        title: table.title || 'Таблица',
        type: table.type || 'users',
        data: table.data || {}
      })) || []

      // Обработка активностей
      recentActivities.value = activities?.map(activity => ({
        id: activity.id || Date.now(),
        user: activity.user || 'Система',
        action: activity.action || 'действие',
        time: formatTime(activity.timestamp),
        type: activity.type || 'info',
        details: activity.details
      })) || []

      lastUpdated.value = new Date().toLocaleString('ru-RU')

    } catch (err) {
      console.error('Ошибка обработки данных:', err)
      error.value = 'Ошибка обработки данных с сервера'
      loadFallbackData()
    }
  }

  // Вспомогательные функции
  const getIconByType = (type) => {
    const icons = {
      users: 'fas fa-users',
      revenue: 'fas fa-dollar-sign',
      success: 'fas fa-chart-line',
      error: 'fas fa-exclamation-triangle',
      orders: 'fas fa-shopping-cart',
      traffic: 'fas fa-network-wired'
    }
    return icons[type] || 'fas fa-chart-bar'
  }

  const getTypeByValue = (value) => {
    if (typeof value === 'number') {
      if (value > 80) return 'success'
      if (value > 50) return 'warning'
      return 'danger'
    }
    return 'default'
  }

  const getDefaultChartData = (type) => {
    if (type === 'bar') {
      return {
        labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
        datasets: [
          {
            label: 'Данные',
            data: [0, 0, 0, 0, 0, 0],
            backgroundColor: '#4299e1'
          }
        ]
      }
    }
    
    return {
      labels: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
      datasets: [
        {
          label: 'Данные',
          data: [0, 0, 0, 0, 0, 0, 0],
          borderColor: '#4299e1',
          backgroundColor: 'rgba(66, 153, 225, 0.1)'
        }
      ]
    }
  }

  const formatTime = (timestamp) => {
    if (!timestamp) return 'недавно'
    
    const now = new Date()
    const time = new Date(timestamp)
    const diffMs = now - time
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    
    if (diffMins < 1) return 'только что'
    if (diffMins < 60) return `${diffMins} минут назад`
    if (diffHours < 24) return `${diffHours} часов назад`
    
    return time.toLocaleDateString('ru-RU')
  }

  // Fallback данные при ошибке API
  const loadFallbackData = () => {
    console.log('Загрузка fallback данных...')
    
    statsData.value = [
      {
        value: '0',
        label: 'Всего пользователей',
        icon: 'fas fa-users',
        type: 'default'
      },
      {
        value: '₽0',
        label: 'Общий доход',
        icon: 'fas fa-dollar-sign',
        type: 'default'
      },
      {
        value: '0%',
        label: 'Успешных операций',
        icon: 'fas fa-chart-line',
        type: 'default'
      },
      {
        value: '0',
        label: 'Ошибок сегодня',
        icon: 'fas fa-exclamation-triangle',
        type: 'default'
      }
    ]

    chartsData.value = [
      {
        title: 'Трафик за неделю',
        type: 'line',
        data: getDefaultChartData('line')
      },
      {
        title: 'Доход по месяцам',
        type: 'bar',
        data: getDefaultChartData('bar')
      }
    ]

    tablesData.value = [
      {
        title: 'Последние пользователи',
        type: 'users',
        data: {
          users: []
        }
      }
    ]

    recentActivities.value = [
      {
        id: 1,
        user: 'Система',
        action: 'данные временно недоступны',
        time: 'только что',
        type: 'warning',
        details: 'Используются локальные данные'
      }
    ]

    lastUpdated.value = new Date().toLocaleString('ru-RU')
  }

  // Actions
  const fetchData = async () => {
    loading.value = true
    error.value = null
    
    try {
      await fetchDashboardData()
    } catch (err) {
      console.error('Ошибка в fetchData:', err)
      error.value = err.message || 'Ошибка загрузки данных'
    } finally {
      loading.value = false
    }
  }

  const exportData = () => {
    const dataToExport = {
      stats: statsData.value,
      charts: chartsData.value,
      tables: tablesData.value,
      activities: recentActivities.value,
      exportedAt: new Date().toISOString(),
      source: 'dashboard-export'
    }
    
    try {
      const dataStr = JSON.stringify(dataToExport, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      const link = document.createElement('a')
      link.href = url
      link.download = `dashboard-export-${new Date().getTime()}.json`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      
      addActivity({
        user: 'Система',
        action: 'экспортировал данные dashboard',
        type: 'success'
      })
    } catch (err) {
      console.error('Ошибка экспорта:', err)
      addActivity({
        user: 'Система',
        action: 'ошибка экспорта данных',
        type: 'danger',
        details: err.message
      })
    }
  }

  const addActivity = (activity) => {
    recentActivities.value.unshift({
      id: Date.now(),
      time: 'только что',
      ...activity
    })
    
    // Ограничиваем количество записей
    if (recentActivities.value.length > 10) {
      recentActivities.value = recentActivities.value.slice(0, 10)
    }
  }

  // Инициализация начальных данных
  const initializeData = () => {
    fetchData()
  }

  // Сброс ошибки
  const clearError = () => {
    error.value = null
  }

  return {
    // State
    loading,
    statsData,
    chartsData,
    tablesData,
    recentActivities,
    lastUpdated,
    error,
    
    // Getters
    getStats,
    getCharts,
    getTables,
    getActivities,
    getLastUpdated,
    isLoading,
    getError,
    
    // Actions
    fetchData,
    exportData,
    addActivity,
    initializeData,
    clearError
  }
})