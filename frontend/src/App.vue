<script setup>
import MainHead from './components/Header/MainHead.vue'
import { Notivue, Notification } from 'notivue'
</script>

<template>
  <div class="app">
    <Notivue v-slot="item">
      <Notification 
        v-if="item && item.type"
        :item="item" 
        :theme="item.type"
        class="custom-notification"
      >
        <div class="notification-content">
          <div class="notification-icon">
            <i v-if="item.type === 'success'" class="pi pi-check-circle"></i>
            <i v-else-if="item.type === 'error'" class="pi pi-times-circle"></i>
            <i v-else-if="item.type === 'warning'" class="pi pi-exclamation-triangle"></i>
            <i v-else-if="item.type === 'info'" class="pi pi-info-circle"></i>
            <i v-else-if="item.type === 'promise'" class="pi pi-spinner pi-spin"></i>
          </div>
          <div class="notification-text">
            <div class="notification-title">{{ item.title || '' }}</div>
            <div class="notification-message">{{ item.message || '' }}</div>
          </div>
        </div>
      </Notification>
    </Notivue>
    
    <MainHead />
    <div class="page-container">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background-color: var(--color-bg);
}

.page-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Для мобильных устройств */
@media (max-width: 768px) {
  .page-container {
    padding: 1rem;
  }
}

/* КОМПАКТНЫЕ стили для уведомлений */
:global(.custom-notification) {
  border-radius: 8px; /* уменьшили радиус */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* уменьшили тень */
  border: 1px solid var(--color-border);
  background: var(--color-bg-elevated);
  padding: 0.75rem; /* уменьшили паддинг */
  min-width: 280px; /* уменьшили минимальную ширину */
  max-width: 350px; /* уменьшили максимальную ширину */
  font-size: 0.875rem; /* уменьшили базовый размер шрифта */
}

:global(.notification-content) {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem; /* уменьшили gap */
}

:global(.notification-icon) {
  font-size: 1rem; /* уменьшили иконки */
  margin-top: 0.1rem;
  flex-shrink: 0;
}

:global(.notification-icon .pi-check-circle) {
  color: var(--color-success);
}

:global(.notification-icon .pi-times-circle) {
  color: var(--color-error);
}

:global(.notification-icon .pi-exclamation-triangle) {
  color: var(--color-warning);
}

:global(.notification-icon .pi-info-circle) {
  color: var(--color-info);
}

:global(.notification-icon .pi-spinner) {
  color: var(--color-primary);
}

:global(.notification-text) {
  flex: 1;
  min-width: 0;
}

:global(.notification-title) {
  font-weight: 600;
  font-size: 0.8rem; /* уменьшили заголовок */
  color: var(--color-text);
  margin-bottom: 0.125rem; /* уменьшили отступ */
}

:global(.notification-message) {
  font-size: 0.75rem; /* уменьшили сообщение */
  color: var(--color-text-muted);
  line-height: 1.3; /* уменьшили межстрочный интервал */
}

/* Адаптивность для уведомлений */
@media (max-width: 768px) {
  :global(.custom-notification) {
    min-width: 250px;
    max-width: 300px;
    margin: 0.25rem;
    padding: 0.625rem;
  }
}
</style>