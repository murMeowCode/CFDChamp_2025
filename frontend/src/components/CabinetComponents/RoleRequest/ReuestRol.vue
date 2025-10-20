<template>
  <section class="role-requests-section" data-aos="fade-down">
    <div class="section-header">
      <h2 class="cyber-heading">Запросы на повышение роли</h2>
      <div class="requests-stats cyber-dynamic">
        <span class="stats-text">Активные: {{ activeRequestsCount }}</span>
      </div>
    </div>

    <!-- Список запросов -->
    <div class="requests-list">
      <div
        v-for="request in requests"
        :key="request.id"
        class="request-item pending"
        data-aos="fade-right"
      >
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
          <div class="request-meta">
            <span class="request-id cyber-mono">#{{ request.id.slice(0, 8) }}</span>
          </div>
        </div>

        <div class="request-actions" v-if="request.status === 'pending'">
          <button class="action-btn cancel-btn cyber-dynamic" @click="cancelRequest(request.id)">
            <span class="btn-icon">✕</span>
            <span>Отменить</span>
          </button>
        </div>
      </div>
    </div>
    <DynamicDialog />
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import DynamicDialog from 'primevue/dynamicdialog'
import { useRequestsStore } from '@/stores/useRequestStore'
import { storeToRefs } from 'pinia'

const { getRequests: requests } = storeToRefs(useRequestsStore())

// Методы
const getStatusText = (status) => {
  const statusMap = {
    pending: 'На рассмотрении',
    approved: 'Одобрено',
    rejected: 'Отклонено',
  }
  return statusMap[status] || status
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

const cancelRequest = (requestId) => {
  requests.value = requests.value.filter((req) => req.id !== requestId)
}

const createNewRequest = async (requestData) => {
  const newRequest = {
    id: 'req_' + Date.now(),
    currentRole: 'Текущая роль', // Здесь должна быть текущая роль пользователя
    targetRole: requestData.targetRole,
    status: 'pending',
    reason: requestData.reason,
    createdAt: new Date(),
  }

  requests.value.unshift(newRequest)
}

// Показ модального окна
const showModal = async () => {
  const result = await showRoleRequestDialog()
  if (result) {
    await createNewRequest(result)
  }
}

onMounted(() => {
  // Здесь можно загрузить реальные данные с API
  console.log(requests)
})
</script>

<style scoped>
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
}

.request-meta {
  display: flex;
  gap: var(--spacing-lg);
  font-size: 0.8rem;
}

.request-date {
  color: var(--color-text-muted);
}

.request-id {
  color: var(--color-text-muted);
}

.request-actions {
  display: flex;
  justify-content: flex-end;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-md);
  border: none;
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
  font-size: 0.9rem;
  font-weight: var(--font-weight-medium);
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
}

/* Состояние пустого списка */
.empty-state {
  text-align: center;
  padding: var(--spacing-2xl);
  color: var(--color-text-muted);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
  opacity: 0.5;
}

.empty-title {
  margin-bottom: var(--spacing-sm);
  color: var(--color-text-muted);
}

.empty-description {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

/* Кнопка нового запроса */
.new-request-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  border: 1px solid var(--color-primary-muted);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
  font-weight: var(--font-weight-semibold);
  justify-content: center;
}

.new-request-btn:hover {
  background: var(--color-primary-muted);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
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

  .request-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }

  .request-meta {
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .request-actions {
    justify-content: flex-start;
    width: 100%;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
