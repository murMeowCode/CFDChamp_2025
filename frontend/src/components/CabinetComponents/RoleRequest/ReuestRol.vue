<template>
  <section v-if="requests && requests.requests && requests.requests.length !== 0" class="role-requests-section" data-aos="fade-down">
    <div class="section-header">
      <h2 class="cyber-heading">Запросы на повышение роли</h2>
      <div class="requests-stats cyber-dynamic">
        <span class="stats-text">Активные: {{ activeRequestsCount }}</span>
      </div>
    </div>

    <!-- Список запросов -->
    <div class="requests-list">
      <div
        v-for="request in requests.requests"
        :key="request.id"
        class="request-item pending"
        data-aos="fade-right"
      >
        <!-- Заголовок карточки с пользователем -->
        <div class="request-user-header">
          <div class="user-avatar">
            <div class="avatar-placeholder">
              {{ getInitials(request.username) }}
            </div>
            <div class="user-status" :class="getUserStatus(request.status)"></div>
          </div>
          <div class="user-info">
            <div class="username-wrapper">
              <span class="username cyber-heading">@{{ request.username }}</span>
              <div class="user-badges">
                <span class="role-badge futurism-elegant">{{ request.current_role }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="request-header">
          <div class="request-role-info">
            <span class="current-role cyber-dynamic">{{ request.current_role }}</span>
            <span class="arrow-icon">➞</span>
            <span class="target-role cyber-mono">{{ request.requested_role }}</span>
          </div>
          <div class="request-status" :class="request.status">
            <span class="status-dot"></span>
            <span class="status-text">{{ getStatusText(request.status) }}</span>
          </div>
        </div>

        <div class="request-details">
          <p class="request-reason futurism-elegant" v-if="request.reason">
            "{{ request.reason }}"
          </p>
        </div>

        <div class="request-actions" v-if="request.status === 'pending'">
          <!-- Кнопка принятия с лоадером -->
          <button 
            class="action-btn success-btn cyber-dynamic" 
            @click="approveRequest(request.id)"
            :disabled="loadingStates[request.id]?.approving"
          >
            <template v-if="loadingStates[request.id]?.approving">
              <div class="button-loader">
                <div class="loader-spinner"></div>
              </div>
              <span>Принимаем...</span>
            </template>
            <template v-else>
              <span class="btn-icon">✓</span>
              <span>Принять</span>
            </template>
          </button>

          <!-- Кнопка отклонения с лоадером -->
          <button 
            class="action-btn cancel-btn cyber-dynamic" 
            @click="rejectRequest(request.id)"
            :disabled="loadingStates[request.id]?.rejecting"
          >
            <template v-if="loadingStates[request.id]?.rejecting">
              <div class="button-loader">
                <div class="loader-spinner"></div>
              </div>
              <span>Отклоняем...</span>
            </template>
            <template v-else>
              <span class="btn-icon">✕</span>
              <span>Отклонить</span>
            </template>
          </button>
        </div>

        <!-- Лоадер поверх карточки -->
        <div v-if="loadingStates[request.id]?.global" class="card-loader-overlay">
          <div class="cyber-loader">
            <div class="loader-core"></div>
            <div class="loader-orbit"></div>
            <div class="loader-particles">
              <div class="particle"></div>
              <div class="particle"></div>
              <div class="particle"></div>
              <div class="particle"></div>
            </div>
          </div>
          <span class="loader-text cyber-mono">Обработка...</span>
        </div>
      </div>
    </div>

    <!-- Глобальный лоадер для всех операций -->
    <div v-if="globalLoading" class="global-loader">
      <div class="cyber-loader large">
        <div class="loader-core"></div>
        <div class="loader-orbit"></div>
        <div class="loader-particles">
          <div class="particle"></div>
          <div class="particle"></div>
          <div class="particle"></div>
          <div class="particle"></div>
        </div>
      </div>
      <span class="loader-text cyber-mono">Обновление данных...</span>
    </div>

    <DynamicDialog />
  </section>

  <!-- Состояние когда нет запросов -->
  <section v-else-if="requests && (!requests.requests || requests.requests.length === 0)" class="role-requests-section empty-state" data-aos="fade-down">
    <div class="empty-state-content">
      <div class="empty-icon">📭</div>
      <h3 class="cyber-heading">Нет активных запросов</h3>
      <p class="cyber-mono">На данный момент нет запросов на повышение роли</p>
    </div>
  </section>

  <!-- Лоадер загрузки данных -->
  <section v-else class="role-requests-section loading-state" data-aos="fade-down">
    <div class="loading-content">
      <div class="cyber-loader large">
        <div class="loader-core"></div>
        <div class="loader-orbit"></div>
        <div class="loader-particles">
          <div class="particle"></div>
          <div class="particle"></div>
          <div class="particle"></div>
          <div class="particle"></div>
        </div>
      </div>
      <span class="loader-text cyber-mono">Загрузка запросов...</span>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import DynamicDialog from 'primevue/dynamicdialog'
import { useRequestsStore } from '@/stores/useRequestStore'
import { storeToRefs } from 'pinia'
import { useApiMutations } from '@/utils/api/useApiMutation'
import { useNotificationsStore } from '@/stores/useToastStore'
import { api8000 } from '@/utils/apiUrl/urlApi'
import axios from 'axios'
import { useAuthStore } from '@/stores/useAuthStore'

const { getRequests } = storeToRefs(useRequestsStore())
const reques = useRequestsStore()
const notifications = useNotificationsStore()
const { getTokenAccsess } = storeToRefs(useAuthStore())

// Состояния загрузки для каждого запроса
const loadingStates = reactive({})
const globalLoading = ref(false)
const isLoadingRequests = ref(true)

// Computed properties
const activeRequestsCount = computed(() => {
  return requests.value?.requests?.filter(req => req.status === 'pending').length || 0
})

// Безопасный computed для requests
const requests = computed(() => {
  return getRequests.value || { requests: [] }
})

// Методы
const getStatusText = (status) => {
  const statusMap = {
    pending: 'На рассмотрении',
    approved: 'Одобрено',
    rejected: 'Отклонено',
  }
  return statusMap[status] || status
}

const getInitials = (username) => {
  if (!username) return '??'
  return username.substring(0, 2).toUpperCase()
}

const getUserStatus = (status) => {
  const statusMap = {
    pending: 'active',
    approved: 'online',
    rejected: 'offline'
  }
  return statusMap[status] || 'offline'
}

// Функции для управления состоянием загрузки
const setLoadingState = (requestId, type, isLoading) => {
  if (!loadingStates[requestId]) {
    loadingStates[requestId] = {}
  }
  loadingStates[requestId][type] = isLoading
}

const approveRequest = async (requestId) => {
  try {
    setLoadingState(requestId, 'approving', true)
    setLoadingState(requestId, 'global', true)
    
    const response = await axios.post(
      `${api8000}/role-change/${requestId}/approve`,
      {},
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getTokenAccsess.value}`
        }
      }
    )
    
    console.log('✅ Запрос принят:', response.data)
    notifications.success('Вы успешно приняли заявку на повышение роли')
    reques.removeRequests()
    // Обновляем данные после успешного действия
    await updateRequestsData()
    
  } catch (error) {
    console.error('❌ Ошибка принятия запроса:', error)
    
    if (error.response?.status === 404) {
      notifications.error('Запрос не найден или уже обработан')
    } else {
      notifications.error('Произошла ошибка при принятии заявки')
    }
  } finally {
    setLoadingState(requestId, 'approving', false)
    setLoadingState(requestId, 'global', false)
  }
}

const rejectRequest = async (requestId) => {
  try {
    setLoadingState(requestId, 'rejecting', true)
    setLoadingState(requestId, 'global', true)
    
    const response = await axios.post(
      `${api8000}/role-change/${requestId}/reject`,
      {},
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getTokenAccsess.value}`
        }
      }
    )

    console.log('✅ Запрос отклонен:', response.data)
    reques.removeRequests()
    notifications.success('Заявка на повышение роли отклонена')
    
    // Обновляем данные после успешного действия
    await updateRequestsData()
    
  } catch (error) {
    console.error('❌ Ошибка отклонения запроса:', error)
    
    if (error.response?.status === 404) {
      notifications.error('Запрос не найден или уже обработан')
    } else {
      notifications.error('Произошла ошибка при отклонении заявки')
    }
  } finally {
    setLoadingState(requestId, 'rejecting', false)
    setLoadingState(requestId, 'global', false)
  }
}

const updateRequestsData = async () => {
  try {
    globalLoading.value = true
    // Здесь можно добавить логику обновления данных запросов
    // Например, повторный запрос к API или обновление store
  } catch (error) {
    console.error('Ошибка обновления данных:', error)
  } finally {
    globalLoading.value = false
  }
}

onMounted(async () => {
  try {
    isLoadingRequests.value = true
    // Здесь можно добавить загрузку данных, если они еще не загружены
    console.log('Requests loaded:', requests.value)
  } catch (error) {
    console.error('Ошибка загрузки запросов:', error)
  } finally {
    isLoadingRequests.value = false
  }
})
</script>
<style scoped>
.button-loader {
  display: flex;
  align-items: center;
  justify-content: center;
}

.loader-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 8px;
}

/* Киберпанк лоадер */
.cyber-loader {
  position: relative;
  width: 40px;
  height: 40px;
  margin: 0 auto;
}

.cyber-loader.large {
  width: 60px;
  height: 60px;
}

.loader-core {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 12px;
  height: 12px;
  background: var(--color-primary);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: pulse-core 2s ease-in-out infinite;
  box-shadow: 0 0 10px var(--color-primary);
}

.loader-orbit {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  border: 2px solid transparent;
  border-top: 2px solid var(--color-primary);
  border-radius: 50%;
  animation: spin-orbit 1.5s linear infinite;
}

.loader-particles {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: var(--color-primary);
  border-radius: 50%;
  animation: particle-rotate 2s linear infinite;
}

.particle:nth-child(1) { top: 0; left: 50%; transform: translateX(-50%); animation-delay: 0s; }
.particle:nth-child(2) { top: 50%; right: 0; transform: translateY(-50%); animation-delay: 0.5s; }
.particle:nth-child(3) { bottom: 0; left: 50%; transform: translateX(-50%); animation-delay: 1s; }
.particle:nth-child(4) { top: 50%; left: 0; transform: translateY(-50%); animation-delay: 1.5s; }

/* Лоадер поверх карточки */
.card-loader-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(4px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-lg);
  z-index: 10;
}

/* Глобальный лоадер */
.global-loader {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(8px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loader-text {
  margin-top: 16px;
  color: var(--color-primary);
  font-size: 0.9rem;
  text-align: center;
}

/* Анимации */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes spin-orbit {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

@keyframes pulse-core {
  0%, 100% { 
    transform: translate(-50%, -50%) scale(1);
    box-shadow: 0 0 10px var(--color-primary);
  }
  50% { 
    transform: translate(-50%, -50%) scale(1.2);
    box-shadow: 0 0 20px var(--color-primary), 0 0 30px var(--color-primary);
  }
}

@keyframes particle-rotate {
  0% { 
    opacity: 1;
    transform: rotate(0deg) translateX(20px) rotate(0deg);
  }
  100% { 
    opacity: 0.5;
    transform: rotate(360deg) translateX(20px) rotate(-360deg);
  }
}

/* Стили для disabled кнопок */
.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.action-btn:disabled:hover {
  transform: none !important;
  box-shadow: none !important;
}

/* Остальные стили остаются без изменений */
.role-requests-section {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-2xl);
  padding: var(--spacing-2xl);
  margin: var(--spacing-xl) var(--spacing-2xl);
  box-shadow:
    0 10px 40px rgba(0, 0, 0, 0.1),
    0 2px 15px rgba(0, 0, 0, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  position: relative;
}

.request-item {
  position: relative;
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  transition: all var(--transition-normal);
  overflow: hidden;
}




.role-requests-section {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-2xl);
  padding: var(--spacing-2xl);
  margin: var(--spacing-xl) var(--spacing-2xl);
  box-shadow:
    0 10px 40px rgba(0, 0, 0, 0.1),
    0 2px 15px rgba(0, 0, 0, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--color-primary);
}

.requests-stats {
  padding: var(--spacing-xs) var(--spacing-md);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  border-radius: var(--border-radius-full);
  font-size: 0.9rem;
  font-weight: var(--font-weight-semibold);
}

/* Список запросов */
.requests-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.request-item {
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.request-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: var(--color-border);
  transition: background-color var(--transition-normal);
}

.request-item.pending::before {
  background: var(--color-warning);
}

.request-item.approved::before {
  background: var(--color-success);
}

.request-item.rejected::before {
  background: var(--color-error);
}

.request-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary-muted);
}

/* Заголовок пользователя */
.request-user-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
}

.user-avatar {
  position: relative;
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 50px;
  height: 50px;
  border-radius: var(--border-radius-full);
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-inverted);
  font-weight: var(--font-weight-bold);
  font-size: 1.1rem;
  box-shadow: var(--shadow-sm);
  border: 2px solid var(--color-bg);
}

.user-status {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  border-radius: var(--border-radius-full);
  border: 2px solid var(--color-bg);
  box-shadow: 0 0 0 1px var(--color-border);
}

.user-status.online {
  background: var(--color-success);
}

.user-status.active {
  background: var(--color-warning);
  animation: pulse 2s infinite;
}

.user-status.offline {
  background: var(--color-error);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.user-info {
  flex: 1;
  min-width: 0;
}

.username-wrapper {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xs);
  flex-wrap: wrap;
}

.username {
  font-size: 1.2rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-badges {
  display: flex;
  gap: var(--spacing-xs);
  flex-wrap: wrap;
}

.level-badge {
  padding: 2px 8px;
  background: var(--color-primary-soft);
  color: var(--color-primary);
  border-radius: var(--border-radius-full);
  font-size: 0.7rem;
  font-weight: var(--font-weight-bold);
  border: 1px solid var(--color-primary-muted);
}

.role-badge {
  padding: 2px 8px;
  background: var(--color-bg-muted);
  color: var(--color-text-muted);
  border-radius: var(--border-radius-full);
  font-size: 0.7rem;
  border: 1px solid var(--color-border);
}

.request-meta {
  display: flex;
  gap: var(--spacing-md);
  font-size: 0.8rem;
}

.request-date {
  color: var(--color-text-muted);
}

.request-id {
  color: var(--color-text-light);
  font-family: 'Share Tech Mono', monospace;
}

/* Остальные стили остаются без изменений */
.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.request-role-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.current-role {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.arrow-icon {
  color: var(--color-primary);
  font-size: 1.2rem;
}

.target-role {
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
  font-size: 1.1rem;
}

.request-status {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-full);
  font-size: 0.8rem;
  font-weight: var(--font-weight-semibold);
}

.request-status.pending {
  background: var(--color-warning-soft);
  color: var(--color-warning);
}

.request-status.approved {
  background: var(--color-success-soft);
  color: var(--color-success);
}

.request-status.rejected {
  background: var(--color-error-soft);
  color: var(--color-error);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: var(--border-radius-full);
  background: currentColor;
}

.request-details {
  margin-bottom: var(--spacing-md);
}

.request-reason {
  color: var(--color-text);
  font-style: italic;
  margin-bottom: var(--spacing-sm);
  line-height: 1.4;
  padding: var(--spacing-sm);
  background: var(--color-bg-muted);
  border-radius: var(--border-radius-md);
  border-left: 3px solid var(--color-primary);
}

.request-actions {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: flex-end;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
  font-size: 0.9rem;
  font-weight: var(--font-weight-medium);
  min-width: 120px;
  justify-content: center;
}

.success-btn {
  background: var(--color-success-soft);
  color: var(--color-success);
  border: 1px solid var(--color-success-muted);
}

.success-btn:hover {
  background: var(--color-success);
  color: var(--color-text-inverted);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.cancel-btn {
  background: var(--color-error-soft);
  color: var(--color-error);
  border: 1px solid var(--color-error-muted);
}

.cancel-btn:hover {
  background: var(--color-error);
  color: var(--color-text-inverted);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

.btn-icon {
  font-size: 1.1rem;
  font-weight: bold;
}

/* Адаптивность */
@media (max-width: 768px) {
  .role-requests-section {
    margin: var(--spacing-lg) var(--spacing-md);
    padding: var(--spacing-lg);
  }

  .section-header {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: flex-start;
  }

  .request-user-header {
    flex-direction: column;
    align-items: flex-start;
    text-align: center;
    gap: var(--spacing-sm);
  }

  .user-info {
    width: 100%;
    text-align: center;
  }

  .username-wrapper {
    justify-content: center;
  }

  .request-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }

  .request-actions {
    justify-content: stretch;
    width: 100%;
  }

  .action-btn {
    flex: 1;
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .user-badges {
    justify-content: center;
  }
  
  .request-meta {
    flex-direction: column;
    gap: var(--spacing-xs);
    align-items: center;
  }
}
</style>