<template>
  <OneDash
    :title="dashboardTitle"
    :stats="statsData"
    :charts="chartsData"
    :tables="tablesData"
    :loading="isLoading"
  >
    <!-- Слот для графиков -->
    <template #chart-bar="{ data }">
      <!-- Передаем data, а не chartsData -->
      <BarChart :data="data" :title="data.title" />
    </template>

    <!-- Слот для таблиц -->
    <template #table-users="{ data }">
      <UsersTable 
        :data="data" 
        @add-user="handleAddUser"
        @edit-user="handleEditUser"
        @delete-user="handleDeleteUser"
      />
    </template>

    <!-- Кастомный контент -->
    <template #custom>
      <div class="recent-activity">
        <div class="custom-header">
          <h3>Последняя активность</h3>
          <div class="header-actions">
            <button class="btn btn-accent" @click="addTestActivity">
              <i class="fas fa-plus"></i>
              Тест
            </button>
            <button class="btn btn-primary" @click="refreshData" :disabled="isLoading">
              <i class="fas fa-sync-alt" :class="{ 'fa-spin': isLoading }"></i>
              Обновить
            </button>
          </div>
        </div>
        <ActivityTimeline :activities="activities" />
      </div>
    </template>
  </OneDash>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import OneDash from './OneDash.vue'
import LineChart from '@/components/Charts/LineChart.vue'
import BarChart from '@/components/Charts/BarChart.vue'
import UsersTable from '../Charts/UsersTable.vue'
import ActivityTimeline from '../Charts/ActivityTimeline.vue'
import { useApiGet } from '@/utils/api/useApiGet'
import { api8000, api8001 } from '@/utils/apiUrl/urlApi'

const { useGet } = useApiGet()

// Refs
const dashboardTitle = ref('Обзор системы')
const activities = ref([])
const lastUpdated = ref(null)

// API запросы
// Запрос для статистики
const {
  data: statsResponse,
  isPending: statsLoading,
  error: statsError,
  // Убираем execute и refresh, так как useGet автоматически выполняет запрос
} = useGet(
  `${api8000}/statistics/dashboard/overview`,
  {},
  {
    withCredentials: true,
  }
  // Убираем { immediate: false } - пусть запрос выполняется автоматически
)

// Запрос для графиков и таблиц
const {
  data: chartsTablesResponse,
  isPending: chartsTablesLoading,
  error: chartsTablesError,
  // Убираем execute и refresh
} = useGet(
  `${api8001}/generate/dashboard/generations`,
  {},
  {
    withCredentials: true,
  }
  // Убираем { immediate: false } - пусть запрос выполняется автоматически
)

// Computed свойства для данных
const statsData = computed(() => {
  if (!statsResponse.value) return getDefaultStats()
  
  const apiStats = statsResponse.value
  
  // Создаем массив только с нужными полями
  const requiredStats = []
  
  // Обрабатываем avg_sequence_length
  if (apiStats.avg_sequence_length !== undefined) {
    requiredStats.push({
      value: typeof apiStats.avg_sequence_length === 'number' 
        ? apiStats.avg_sequence_length.toFixed(2) 
        : apiStats.avg_sequence_length.toString(),
      label: 'Средняя длина последовательности',
      icon: 'fas fa-ruler',
      type: getTypeByValue(apiStats.avg_sequence_length)
    })
  }
  
  // Обрабатываем avg_success_rate
  if (apiStats.avg_success_rate !== undefined) {
    requiredStats.push({
      value: typeof apiStats.avg_success_rate === 'number' 
        ? `${(apiStats.avg_success_rate * 100).toFixed(1)}%`
        : apiStats.avg_success_rate.toString(),
      label: 'Средняя успешность тестов',
      icon: 'fas fa-chart-line',
      type: getTypeByValue(apiStats.avg_success_rate)
    })
  }
  
  // Обрабатываем total_sequences
  if (apiStats.total_sequences !== undefined) {
    requiredStats.push({
      value: apiStats.total_sequences?.toString() || '0',
      label: 'Всего последовательностей',
      icon: 'fas fa-list-ol',
      type: getTypeByValue(apiStats.total_sequences)
    })
  }
  
  
  
  // Если нет нужных данных, возвращаем дефолтные
  return requiredStats.length > 0 ? requiredStats : getDefaultStats()
})

// В computed свойствах добавьте преобразование данных для гистограммы
const chartsData = computed(() => {
  if (!chartsTablesResponse.value) return getDefaultCharts()
  
  const apiData = chartsTablesResponse.value
  
  // Преобразуем bit_distribution в формат для гистограммы
  const bitDistributionChart = {
    title: 'Распределение битов по длинам последовательностей',
    type: 'bar',
    data: transformBitDistribution(apiData.bit_distribution)
  }
  
  // Добавляем другие графики если есть
  const otherCharts = apiData.charts || []
  
  return [bitDistributionChart, ...otherCharts]
})

// Функция для преобразования bit_distribution в формат Chart.js
const transformBitDistribution = (bitDistribution) => {
  if (!bitDistribution || !Array.isArray(bitDistribution)) {
    return getDefaultChartData('bar')
  }
  
  const labels = bitDistribution.map(item => item.length_range)
  const avgOnesData = bitDistribution.map(item => item.avg_ones)
  const avgZerosData = bitDistribution.map(item => item.avg_zeros)
  
  console.log('📊 Данные для гистограммы:', {
    labels,
    avgOnesData,
    avgZerosData
  })
  
  return {
    labels,
    datasets: [
      {
        label: 'Среднее количество 1',
        data: avgOnesData,
        backgroundColor: '#4299e1', // Синий для единиц
        borderColor: '#4299e1',
        borderWidth: 1,
        borderRadius: 4,
        barPercentage: 0.6, // Ширина столбцов
        categoryPercentage: 0.8 // Расстояние между группами
      },
      {
        label: 'Среднее количество 0',
        data: avgZerosData,
        backgroundColor: '#e53e3e', // Красный для нулей
        borderColor: '#e53e3e',
        borderWidth: 1,
        borderRadius: 4,
        barPercentage: 0.6,
        categoryPercentage: 0.8
      }
    ]
  }
}

const tablesData = computed(() => {
  if (!chartsTablesResponse.value) return getDefaultTables()
  
  const apiTables = chartsTablesResponse.value.tables || []
  if (Array.isArray(apiTables)) {
    return apiTables.map(table => ({
      title: table.title || 'Таблица',
      type: table.type || 'users',
      data: table.data || {}
    }))
  }
  
  return getDefaultTables()
})

const isLoading = computed(() => statsLoading.value || chartsTablesLoading.value)

const error = computed(() => statsError.value || chartsTablesError.value)

// Watchers для обработки данных
watch(statsResponse, (newData) => {
  if (newData) {
    console.log('📊 Статистика загружена:', newData)
    lastUpdated.value = new Date().toLocaleString('ru-RU')
    addActivity({
      user: 'Система',
      action: 'статистика обновлена',
      type: 'success'
    })
  }
})

watch(chartsTablesResponse, (newData) => {
  if (newData) {
    console.log('📈 Графики и таблицы загружены:', newData)
    addActivity({
      user: 'Система',
      action: 'графики и таблицы обновлены',
      type: 'success'
    })
  }
})

watch([statsError, chartsTablesError], ([statsErr, chartsErr]) => {
  if (statsErr || chartsErr) {
    console.error('❌ Ошибки загрузки:', { statsErr, chartsErr })
    addActivity({
      user: 'Система',
      action: 'ошибка загрузки данных',
      type: 'danger',
      details: statsErr?.message || chartsErr?.message
    })
  }
})

// Methods
const refreshData = () => {
  // Перезагружаем страницу для простоты, или можно пересоздать компонент
  window.location.reload()
}

const handleAddUser = (userData) => {
  console.log('Добавить пользователя:', userData)
  addActivity({
    user: 'Система',
    action: 'добавлен новый пользователь',
    type: 'success',
    details: `Пользователь: ${userData.name}`
  })
}

const handleEditUser = (user) => {
  console.log('Редактировать пользователя:', user)
  addActivity({
    user: 'Администратор',
    action: 'отредактировал профиль пользователя',
    type: 'info',
    details: `Пользователь: ${user.name}`
  })
}

const handleDeleteUser = (user) => {
  console.log('Удалить пользователя:', user)
  addActivity({
    user: 'Администратор',
    action: 'удалил пользователя',
    type: 'danger',
    details: `Пользователь: ${user.name}`
  })
}

const addTestActivity = () => {
  addActivity({
    user: 'Тестовая система',
    action: 'выполнено тестовое действие',
    type: 'warning',
    details: 'Это тестовая активность для демонстрации'
  })
}

const addActivity = (activity) => {
  activities.value.unshift({
    id: Date.now(),
    time: 'только что',
    ...activity
  })
  
  // Ограничиваем количество записей
  if (activities.value.length > 10) {
    activities.value = activities.value.slice(0, 10)
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
    traffic: 'fas fa-network-wired',
    total_users: 'fas fa-users',
    total_income: 'fas fa-dollar-sign',
    success_rate: 'fas fa-chart-line',
    errors_today: 'fas fa-exclamation-triangle',
    default: 'fas fa-chart-bar'
  }
  return icons[type] || icons.default
}

const getTypeByValue = (value) => {
  if (typeof value === 'number') {
    if (value > 80) return 'success'
    if (value > 50) return 'warning'
    return 'danger'
  }
  return 'default'
}

const formatLabel = (key) => {
  const labels = {
    total_users: 'Всего пользователей',
    total_income: 'Общий доход',
    success_rate: 'Успешных операций',
    errors_today: 'Ошибок сегодня',
    users: 'Пользователи',
    revenue: 'Доход',
    success: 'Успешные операции',
    error: 'Ошибки'
  }
  return labels[key] || key.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}

// Дефолтные данные
const getDefaultStats = () => [
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

const getDefaultCharts = () => [
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

const getDefaultTables = () => [
  {
    title: 'Последние пользователи',
    type: 'users',
    data: {
      users: []
    }
  }
]

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

// Lifecycle
onMounted(() => {
  // Запросы выполняются автоматически через useGet
  console.log('🚀 Dashboard компонент загружен, запросы выполняются автоматически')
})
</script>
<style scoped>
.actions-container {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.header-actions {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.btn {
  padding: 10px 16px;
  border: 1px solid;
  border-radius: var(--border-radius-md);
  font-size: 14px;
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all var(--transition-normal);
  font-family: 'Rajdhani', 'Exo 2', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.btn-primary {
  background: var(--color-vanilla-light);
  color: var(--color-midnight);
  border-color: var(--color-midnight);
  box-shadow: var(--shadow-md);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-secondary {
  background: var(--color-vanilla-light);
  color: var(--color-midnight);
  border-color: var(--color-vanilla-dark);
  box-shadow: var(--shadow-sm);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--color-vanilla);
  border-color: var(--color-midnight-light);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-accent {
  background: var(--color-midnight-medium);
  color: var(--color-vanilla);
  border-color: var(--color-midnight-medium);
  box-shadow: var(--shadow-sm);
}

.btn-accent:hover:not(:disabled) {
  background: var(--color-midnight-light);
  border-color: var(--color-midnight-light);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.last-updated {
  font-size: 12px;
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: var(--color-primary-soft);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-border);
  font-family: 'Share Tech Mono', monospace;
}

.recent-activity {
  margin-top: var(--spacing-xl);
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-indigo);
  border: 1px solid var(--color-border);
}

.custom-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
}

.custom-header h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 1.25rem;
  font-weight: var(--font-weight-semibold);
  font-family: 'Orbitron', sans-serif;
  text-transform: uppercase;
  letter-spacing: 1px;
  background: var(--color-accent);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Адаптивность */
@media (max-width: 768px) {
  .actions-container {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-sm);
  }
  
  .custom-header {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .btn {
    justify-content: center;
  }
}

/* Анимации */
.btn {
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background:  rgba(255,255,255,0.2);
  transition: left var(--transition-slow);
}

.btn:hover::before {
  left: 100%;
}

/* Специфичные стили для состояний */
.btn:active {
  transform: translateY(0);
}

.btn-primary:active {
  background: var(--color-midnight);
}

/* Иконки */
.btn i {
  font-size: 0.9em;
  transition: transform var(--transition-fast);
}

.btn:hover:not(:disabled) i {
  transform: scale(1.1);
}

.fa-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Стили для disabled состояний */
.btn:disabled {
  background: var(--color-bg-muted);
  color: var(--color-text-muted);
  border-color: var(--color-border);
  box-shadow: none;
}
</style>