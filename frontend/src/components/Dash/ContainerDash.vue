<template>
  <OneDash
    :title="dashboardTitle"
    :stats="dashboardStore.getStats"
    :charts="dashboardStore.getCharts"
    :tables="dashboardStore.getTables"
    :loading="dashboardStore.isLoading"
  >


    <!-- Слот для графиков -->
    <template #chart-line="{ data }">
      <LineChart :data="data" />
    </template>

    <template #chart-bar="{ data }">
      <BarChart :data="data" />
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
          <button class="btn btn-accent" @click="addTestActivity">
            <i class="fas fa-plus"></i>
            Тест
          </button>
        </div>
        <ActivityTimeline :activities="dashboardStore.getActivities" />
      </div>
    </template>
  </OneDash>
</template>

<script>
import { onMounted } from 'vue'
import { useDashboardStore } from '@/stores/useDashStore'
import OneDash from './OneDash.vue'
import LineChart from '@/components/Charts/LineChart.vue'
import BarChart from '@/components/Charts/BarChart.vue'
import UsersTable from '../Charts/UsersTable.vue'
import ActivityTimeline from '../Charts/ActivityTimeline.vue'

export default {
  name: 'DashboardContainer',
  components: {
    OneDash,
    LineChart,
    BarChart,
    UsersTable,
    ActivityTimeline
  },
  setup() {
    const dashboardStore = useDashboardStore()
    const dashboardTitle = 'Обзор системы'

    const refreshData = async () => {
      try {
        await dashboardStore.fetchData()
        // Можно добавить уведомление об успехе
        console.log('Данные успешно обновлены')
      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
        // Можно показать уведомление об ошибке
      }
    }

    const handleAddUser = (userData) => {
      console.log('Добавить пользователя:', userData)
      dashboardStore.addActivity({
        user: 'Система',
        action: 'добавлен новый пользователь',
        type: 'success',
        details: `Пользователь: ${userData.name}`
      })
    }

    const handleEditUser = (user) => {
      console.log('Редактировать пользователя:', user)
      dashboardStore.addActivity({
        user: 'Администратор',
        action: 'отредактировал профиль пользователя',
        type: 'info',
        details: `Пользователь: ${user.name}`
      })
    }

    const handleDeleteUser = (user) => {
      console.log('Удалить пользователя:', user)
      dashboardStore.addActivity({
        user: 'Администратор',
        action: 'удалил пользователя',
        type: 'danger',
        details: `Пользователь: ${user.name}`
      })
    }

    const addTestActivity = () => {
      dashboardStore.addActivity({
        user: 'Тестовая система',
        action: 'выполнено тестовое действие',
        type: 'warning',
        details: 'Это тестовая активность для демонстрации'
      })
    }

    onMounted(() => {
      // Инициализируем данные при монтировании
      if (dashboardStore.getStats.length === 0) {
        dashboardStore.initializeData()
      }
    })

    return {
      dashboardStore,
      dashboardTitle,
      refreshData,
      handleAddUser,
      handleEditUser,
      handleDeleteUser,
      addTestActivity
    }
  }
}
</script>

<style scoped>
.actions-container {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  flex-wrap: wrap;
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
  
  .last-updated {
    order: -1;
    justify-content: center;
    text-align: center;
  }
  
  .custom-header {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: flex-start;
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

/* Стили для disabled состояний */
.btn:disabled {
  background: var(--color-bg-muted);
  color: var(--color-text-muted);
  border-color: var(--color-border);
  box-shadow: none;
}
</style>