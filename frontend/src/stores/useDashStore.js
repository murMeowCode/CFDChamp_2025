import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useDashboardStore = defineStore('dashboard', () => {
  // State
  const loading = ref(false)
  const statsData = ref([])
  const chartsData = ref([])
  const tablesData = ref([])
  const recentActivities = ref([])
  const lastUpdated = ref(null)

  // Getters
  const getStats = computed(() => statsData.value)
  const getCharts = computed(() => chartsData.value)
  const getTables = computed(() => tablesData.value)
  const getActivities = computed(() => recentActivities.value)
  const getLastUpdated = computed(() => lastUpdated.value)
  const isLoading = computed(() => loading.value)

  // Actions
  const fetchData = async () => {
    loading.value = true
    try {
      // Имитация API запроса
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Обновляем данные
      statsData.value = [
        {
          value: '1,356',
          label: 'Всего пользователей',
          icon: 'fas fa-users',
          type: 'success',
          trend: {
            value: '+15%',
            direction: 'up'
          }
        },
        {
          value: '₽135,670',
          label: 'Общий доход',
          icon: 'fas fa-dollar-sign',
          type: 'default',
          trend: {
            value: '+10%',
            direction: 'up'
          }
        },
        {
          value: '92%',
          label: 'Успешных операций',
          icon: 'fas fa-chart-line',
          type: 'success'
        },
        {
          value: '18',
          label: 'Ошибок сегодня',
          icon: 'fas fa-exclamation-triangle',
          type: 'danger',
          trend: {
            value: '-8%',
            direction: 'down'
          }
        }
      ]

      chartsData.value = [
        {
          title: 'Трафик за неделю',
          type: 'line',
          data: {
            labels: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
            datasets: [
              {
                label: 'Трафик',
                data: [70, 65, 85, 75, 60, 50, 45],
                borderColor: '#4299e1',
                backgroundColor: 'rgba(66, 153, 225, 0.1)'
              }
            ]
          }
        },
        {
          title: 'Доход по месяцам',
          type: 'bar',
          data: {
            labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
            datasets: [
              {
                label: 'Доход',
                data: [13000, 20000, 16000, 26000, 23000, 32000],
                backgroundColor: '#48bb78'
              },
              {
                label: 'Расход',
                data: [8500, 12500, 10500, 15500, 13500, 19000],
                backgroundColor: '#f56565'
              }
            ]
          }
        }
      ]

      tablesData.value = [
        {
          title: 'Последние пользователи',
          type: 'users',
          data: {
            users: [
              {
                id: 1,
                name: 'Иван Петров',
                email: 'ivan@example.com',
                avatar: '',
                status: 'active',
                joinDate: '2024-01-15',
                activity: 85
              },
              {
                id: 2,
                name: 'Мария Сидорова',
                email: 'maria@example.com',
                avatar: '',
                status: 'active',
                joinDate: '2024-01-10',
                activity: 92
              },
              {
                id: 3,
                name: 'Алексей Козлов',
                email: 'alexey@example.com',
                avatar: '',
                status: 'active',
                joinDate: '2024-01-05',
                activity: 65
              }
            ]
          }
        }
      ]

      recentActivities.value = [
        {
          id: 1,
          user: 'Иван Петров',
          action: 'создал заказ #12345',
          time: '5 минут назад',
          type: 'success',
          details: 'Сумма заказа: ₽15,000'
        },
        {
          id: 2,
          user: 'Мария Сидорова',
          action: 'обновила профиль компании',
          time: '12 минут назад',
          type: 'info'
        },
        {
          id: 3,
          user: 'Алексей Козлов',
          action: 'добавил новый товар',
          time: '25 минут назад',
          type: 'success',
          details: 'Товар "Премиум пакет"'
        }
      ]

      lastUpdated.value = new Date().toLocaleString('ru-RU')
      
    } catch (error) {
      console.error('Ошибка загрузки данных:', error)
      throw error
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
      exportedAt: new Date().toISOString()
    }
    
    // Создаем и скачиваем файл
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

  return {
    // State
    loading,
    statsData,
    chartsData,
    tablesData,
    recentActivities,
    lastUpdated,
    
    // Getters
    getStats,
    getCharts,
    getTables,
    getActivities,
    getLastUpdated,
    isLoading,
    
    // Actions
    fetchData,
    exportData,
    addActivity,
    initializeData
  }
})