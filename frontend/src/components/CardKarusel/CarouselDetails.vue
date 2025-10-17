<template>
  <div class="details-container" data-aos="fade-up" data-aos-duration="600">
    <div class="details-content">
      <!-- Компактный заголовок и описание -->
      <div class="details-header">
        <h3 class="details-title">{{ title }}</h3>
        <p class="details-description">{{ description }}</p>
      </div>

      <!-- Мета-информация в одну строку -->
      <div class="meta-row">
        <div class="meta-item compact">
          <div class="meta-icon">⏱️</div>
          <div class="meta-content">
            <span class="meta-label">Длительность</span>
            <span class="meta-value">{{ duration }}</span>
          </div>
        </div>
        <div class="meta-item compact">
          <div class="meta-icon">👥</div>
          <div class="meta-content">
            <span class="meta-label">Участники</span>
            <span class="meta-value">{{ participants }}</span>
          </div>
        </div>
        <div class="meta-item compact">
          <div class="meta-icon">💰</div>
          <div class="meta-content">
            <span class="meta-label">Призы</span>
            <span class="meta-value">{{ prize }}</span>
          </div>
        </div>
      </div>

      <!-- Особенности в компактном горизонтальном виде -->
      <div class="features-horizontal">
        <h4 class="features-title">Что включено:</h4>
        <div class="features-scroll">
          <div
            v-for="(feature, index) in features"
            :key="index"
            class="feature-compact"
            data-aos="zoom-in"
            :data-aos-delay="index * 50"
          >
            <div class="feature-icon-small">{{ feature.icon }}</div>
            <div class="feature-text-compact">
              <span class="feature-title-small">{{ feature.title }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Кнопки действий в одну строку -->
      <div class="actions-row">
        <button class="action-btn primary">
          <span>Участвовать</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path
              d="M5 12H19M19 12L12 5M19 12L12 19"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
        <button class="action-btn outline">
          <span>Подробнее</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
// Props
defineProps({
  title: {
    type: String,
    default: '',
  },
  description: {
    type: String,
    default: '',
  },
  duration: {
    type: String,
    default: '',
  },
  participants: {
    type: String,
    default: '',
  },
  prize: {
    type: String,
    default: '',
  },
  features: {
    type: Array,
    default: () => [],
  },
})
</script>

<style scoped>
.details-container {
  width: 100%;
  max-width: 100%;
}

.details-content {
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-xl);
  padding: var(--spacing-xl);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  height: auto; /* Автоматическая высота */
  min-height: auto; /* Убираем фиксированную минимальную высоту */
}

.details-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradient-primary);
}

/* Заголовок и описание */
.details-header {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.details-title {
  font-size: 1.5rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin: 0;
  line-height: 1.2;
  background: linear-gradient(135deg, var(--color-text) 0%, var(--color-text-muted) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* Разрешаем 2 строки для заголовка */
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.details-description {
  font-size: 0.9rem;
  line-height: 1.4;
  color: var(--color-text-muted);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3; /* Увеличиваем до 3 строк для описания */
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Мета-информация в строку */
.meta-row {
  display: flex;
  gap: var(--spacing-md);
  justify-content: space-between;
}

.meta-item.compact {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-primary-soft);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-primary-muted);
  flex: 1;
  min-width: 0;
}

.meta-icon {
  font-size: 1rem;
  flex-shrink: 0;
}

.meta-content {
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;
  flex: 1;
}

.meta-label {
  font-size: 0.7rem;
  font-weight: var(--font-weight-medium);
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.meta-value {
  font-size: 0.85rem;
  font-weight: var(--font-weight-semibold);
  color: var(--color-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Горизонтальные особенности */
.features-horizontal {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.features-title {
  font-size: 0.9rem;
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.features-scroll {
  display: flex;
  gap: var(--spacing-sm);
  overflow-x: auto;
  padding: var(--spacing-xs) 0;
  scrollbar-width: thin;
  scrollbar-color: var(--color-border) transparent;
}

.features-scroll::-webkit-scrollbar {
  height: 4px;
}

.features-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.features-scroll::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 2px;
}

.feature-compact {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-bg-muted);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border);
  transition: all var(--transition-fast);
  flex-shrink: 0;
  white-space: nowrap;
}

.feature-compact:hover {
  transform: translateY(-1px);
  border-color: var(--color-primary);
  box-shadow: var(--shadow-sm);
}

.feature-icon-small {
  font-size: 0.9rem;
  flex-shrink: 0;
}

.feature-text-compact {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.feature-title-small {
  font-size: 0.8rem;
  font-weight: var(--font-weight-medium);
  color: var(--color-text);
  white-space: nowrap;
}

/* Кнопки действий */
.actions-row {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
  margin-top: auto;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border: none;
  border-radius: var(--border-radius-lg);
  font-weight: var(--font-weight-medium);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all var(--transition-normal);
  text-decoration: none;
  flex: 1;
  justify-content: center;
  min-height: 44px;
}

.action-btn.primary {
  background: var(--gradient-primary);
  color: var(--color-text-inverted);
  box-shadow: var(--shadow-sm);
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.action-btn.outline {
  background: transparent;
  color: var(--color-text);
  border: 1.5px solid var(--color-border);
}

.action-btn.outline:hover {
  background: var(--color-bg-muted);
  border-color: var(--color-primary);
  transform: translateY(-1px);
}

/* ========== АДАПТИВНОСТЬ ========== */

/* Десктоп */
@media (min-width: 1200px) {
  .details-content {
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* Планшеты */
@media (max-width: 968px) {
  .details-content {
    padding: var(--spacing-lg);
    gap: var(--spacing-md);
    margin: 0 var(--spacing-md); /* Добавляем отступы по бокам */
    width: calc(100% - var(--spacing-md) * 2); /* Ширина минус отступы */
  }

  .details-title {
    font-size: 1.3rem;
    -webkit-line-clamp: 2; /* На планшетах тоже 2 строки */
  }

  .details-description {
    -webkit-line-clamp: 3; /* На планшетах 3 строки */
  }

  .meta-row {
    gap: var(--spacing-sm);
  }

  .meta-item.compact {
    padding: var(--spacing-xs) var(--spacing-sm);
  }

  .actions-row {
    gap: var(--spacing-sm);
  }

  .action-btn {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: 0.85rem;
  }
  .features-scroll {
    display: flex;
    flex-direction: column;
  }
}

/* Большие мобильные */
@media (max-width: 768px) {
  .details-content {
    padding: var(--spacing-md);
    margin: 0 var(--spacing-sm);
    width: calc(100% - var(--spacing-sm) * 2);
    border-radius: var(--border-radius-lg); /* Чуть меньше скругление на мобилках */
  }

  .details-title {
    font-size: 1.2rem;
    -webkit-line-clamp: 2;
  }

  .details-description {
    font-size: 0.85rem;
    -webkit-line-clamp: 3;
  }

  .meta-row {
    flex-wrap: wrap;
    gap: var(--spacing-sm);
  }

  .meta-item.compact {
    flex: 1 1 calc(50% - var(--spacing-sm));
    min-width: 120px;
  }

  .features-scroll {
    gap: var(--spacing-xs);
  }

  .feature-compact {
    padding: var(--spacing-xs) var(--spacing-sm);
    white-space: normal; /* Разрешаем перенос текста */
    min-width: 140px;
  }

  .feature-title-small {
    white-space: normal;
    font-size: 0.75rem;
    text-align: center;
  }
  .features-scroll {
    display: flex;
    flex-direction: column;
  }
}

/* Мобильные устройства */
@media (max-width: 640px) {
  .details-content {
    padding: var(--spacing-md);
    margin: 0 var(--spacing-xs);
    width: calc(100% - var(--spacing-xs) * 2);
    gap: var(--spacing-md);
  }

  .details-header {
    gap: var(--spacing-xs);
  }

  .details-title {
    font-size: 1.1rem;
    -webkit-line-clamp: 2;
  }

  .details-description {
    font-size: 0.8rem;
    -webkit-line-clamp: 3;
    line-height: 1.3;
  }

  .meta-item.compact {
    flex: 1 1 100%; /* На маленьких экранах - полная ширина */
    margin-bottom: var(--spacing-xs);
  }

  .meta-row {
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .features-horizontal {
    gap: var(--spacing-xs);
  }

  .features-title {
    font-size: 0.8rem;
  }

  .actions-row {
    flex-direction: column;
    gap: var(--spacing-sm);
    margin-top: var(--spacing-md);
  }

  .action-btn {
    width: 100%;
    min-height: 48px; /* Увеличиваем для удобства касания */
    font-size: 0.9rem;
  }

  .feature-compact {
    min-width: 130px;
    flex-direction: column;
    gap: var(--spacing-xs);
    text-align: center;
    padding: var(--spacing-sm);
  }

  .feature-icon-small {
    font-size: 1rem;
  }
  .features-scroll {
    display: flex;
    flex-direction: column;
  }
}

/* Маленькие мобильные */
@media (max-width: 480px) {
  .details-content {
    padding: var(--spacing-md) var(--spacing-sm);
    margin: 0 var(--spacing-xs);
    width: calc(100% - var(--spacing-xs) * 2);
  }

  .details-title {
    font-size: 1.1rem;
    -webkit-line-clamp: 2;
  }

  .details-description {
    font-size: 0.8rem;
    -webkit-line-clamp: 4; /* На самых маленьких экранах разрешаем 4 строки */
  }

  .meta-label {
    font-size: 0.65rem;
  }

  .meta-value {
    font-size: 0.8rem;
  }

  .features-title {
    font-size: 0.8rem;
  }

  .feature-compact {
    min-width: 120px;
    padding: var(--spacing-xs) var(--spacing-sm);
  }

  .feature-title-small {
    font-size: 0.7rem;
    line-height: 1.2;
  }
}

/* Очень маленькие экраны */
@media (max-width: 360px) {
  .details-content {
    padding: var(--spacing-sm);
    margin: 0 8px;
    width: calc(100% - 16px);
  }

  .details-title {
    font-size: 1rem;
  }

  .details-description {
    font-size: 0.75rem;
  }

  .meta-item.compact {
    padding: 8px 10px;
  }

  .feature-compact {
    min-width: 110px;
    padding: 6px 8px;
  }
  .features-scroll {
    display: flex;
    flex-direction: column;
  }
}

/* Темная тема */
[data-theme='dark'] .details-content {
  background: var(--color-bg-elevated);
  border-color: var(--color-border-strong);
}

[data-theme='dark'] .feature-compact {
  background: var(--color-bg-muted);
  border-color: var(--color-border-strong);
}

[data-theme='dark'] .meta-item.compact {
  background: var(--color-primary-muted);
  border-color: var(--color-primary-soft);
}
</style>
