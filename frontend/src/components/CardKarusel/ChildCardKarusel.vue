<template>
  <div
    :class="['carousel-card', { active: active }]"
    :style="cardStyle"
    data-aos="fade-up"
    :data-aos-duration="600"
    @click="$emit('card-click')"
  >
    <div class="card-glow"></div>

    <div class="card-header">
      <div class="card-image" v-if="img">
        <img :src="img" :alt="title" />
        <div class="image-overlay"></div>
      </div>
      <div class="card-top" v-else>
        <div class="pattern"></div>
      </div>

      <div class="card-badge" v-if="active">
        <span>🔥 Активно</span>
      </div>
    </div>

    <div class="card-body">
      <div class="card-content">
        <div class="card-meta">
          <div class="meta-dot"></div>
          <span class="meta-text">Премиум</span>
        </div>

        <h3 class="card-title">{{ title }}</h3>
        <p class="card-subtitle" v-if="subtitle">{{ subtitle }}</p>

        <div class="card-features">
          <div class="feature">
            <div class="feature-icon">⭐</div>
            <span>Экспертный уровень</span>
          </div>
          <div class="feature">
            <div class="feature-icon">👥</div>
            <span>Командный формат</span>
          </div>
        </div>
      </div>

      <div class="card-actions" v-if="active">
        <button class="action-btn primary">Участвовать</button>
        <button class="action-btn secondary">Подробнее</button>
      </div>
    </div>

    <div class="card-glow-effect" v-if="active"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  title: {
    type: String,
    default: '',
  },
  subtitle: {
    type: String,
    default: '',
  },
  img: {
    type: String,
    default: '',
  },
  active: {
    type: Boolean,
    default: false,
  },
  cardStyle: {
    type: Object,
    default: () => ({}),
  },
})

// Emits
defineEmits(['card-click'])
</script>

<style scoped>
.carousel-card {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 420px; /* Увеличил ширину */
  height: 480px; /* Увеличил высоту */
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-2xl);
  overflow: hidden;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--color-border);
  transition: all var(--transition-slow) cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  max-width: 90vw; /* Ограничиваем максимальную ширину */
  max-height: 90vh; /* Ограничиваем максимальную высоту */
  transform-origin: center;
  will-change: transform;
}

.carousel-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--border-radius-2xl);
  padding: 2px;
  background: var(--gradient-primary);
  mask:
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  mask-composite: subtract;
  opacity: 0;
  transition: opacity var(--transition-normal);
  z-index: 2;
}

.carousel-card.active::before {
  opacity: 1;
}

.carousel-card:hover {
  box-shadow: var(--shadow-2xl);
  transform: translateY(-8px) scale(1.02);
}

.carousel-card.active {
  transform: translateY(-12px) scale(1.05);
  border-color: transparent;
}

.carousel-card.active:hover {
  transform: translateY(-12px) scale(1.08);
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: var(--gradient-primary);
  opacity: 0;
  transition: opacity var(--transition-normal);
  border-radius: var(--border-radius-2xl);
}

.carousel-card.active .card-glow {
  opacity: 0.03;
}

.card-header {
  width: 100%;
  height: 200px; /* Фиксированная высота заголовка */
  position: relative;
  overflow: hidden;
  flex-shrink: 0; /* Запрещаем сжатие */
}

.card-top {
  width: 100%;
  height: 100%;
  background: var(--gradient-primary);
  position: relative;
}

.pattern {
  width: 100%;
  height: 100%;
  background:
    radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
}

.card-image {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.3) 100%);
}

.carousel-card:hover .card-image img {
  transform: scale(1.08);
}

.card-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  background: var(--color-primary);
  color: var(--color-text-inverted);
  padding: 8px 16px;
  border-radius: var(--border-radius-full);
  font-size: 0.8rem;
  font-weight: var(--font-weight-semibold);
  box-shadow: var(--shadow-md);
  backdrop-filter: var(--backdrop-blur);
  max-width: calc(100% - 32px);
  z-index: 3;
}

.card-body {
  height: calc(100% - 200px); /* Высота рассчитывается от оставшегося пространства */
  padding: 0.8rem;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
  overflow: hidden;
  min-height: 280px; /* Минимальная высота для контента */
}

.card-content {
  flex: 0.9;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  overflow: hidden;
  min-height: 0; /* Позволяет контенту сжиматься */
}

.card-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xs);
  flex-shrink: 0; /* Запрещаем сжатие */
}

.meta-dot {
  width: 8px;
  height: 8px;
  border-radius: var(--border-radius-full);
  background: var(--color-primary);
  animation: pulse 2s infinite;
  flex-shrink: 0;
}

.meta-text {
  font-size: 0.8rem;
  font-weight: var(--font-weight-medium);
  color: var(--color-primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex-shrink: 0;
}

.card-title {
  font-size: 1.5rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin: 0;
  line-height: 1.3;
  background: linear-gradient(135deg, var(--color-text) 0%, var(--color-text-muted) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex-shrink: 0; /* Запрещаем сжатие заголовка */
}

.card-subtitle {
  font-size: 1rem;
  color: var(--color-text-muted);
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex-shrink: 0; /* Запрещаем сжатие подзаголовка */
}

.card-features {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin-top: 0; /* Прижимаем к низу */
  flex-shrink: 0;
}

.feature {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 0.9rem;
  color: var(--color-text-muted);
  flex-shrink: 0;
}

.feature-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-soft);
  border-radius: var(--border-radius-full);
  font-size: 0.8rem;
  flex-shrink: 0;
}

.card-actions {
  display: flex;
  gap: var(--spacing-md);
  margin-top: 0;
  flex-shrink: 0; /* Запрещаем сжатие кнопок */
}

.action-btn {
  flex: 1;
  padding: var(--spacing-md) var(--spacing-lg);
  border: none;
  border-radius: var(--border-radius-lg);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-normal);
  font-size: 0.9rem;
  min-height: 44px; /* Минимальная высота для accessibility */
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.action-btn.primary {
  background: var(--gradient-primary);
  color: var(--color-text-inverted);
  box-shadow: var(--shadow-md);
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.action-btn.secondary {
  background: transparent;
  color: var(--color-text);
  border: 2px solid var(--color-border);
}

.action-btn.secondary:hover {
  background: var(--color-bg-muted);
  border-color: var(--color-border-hover);
}

.card-glow-effect {
  position: absolute;
  inset: -8px;
  border-radius: var(--border-radius-2xl);
  box-shadow:
    0 0 60px 15px rgba(59, 130, 246, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  pointer-events: none;
  z-index: 0;
}

/* Анимации */
@keyframes pulse {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* Адаптивность */
@media (max-width: 1400px) {
  .carousel-card {
    width: 380px;
    height: 440px;
  }

  .card-body {
    padding: var(--spacing-lg);
  }
}

@media (max-width: 1200px) {
  .carousel-card {
    width: 350px;
    height: 420px;
  }

  .card-title {
    font-size: 1.4rem;
  }

  .card-body {
    padding: var(--spacing-lg);
    min-height: 260px;
  }
}

@media (max-width: 968px) {
  .carousel-card {
    width: 320px;
    height: 390px;
  }

  .card-header {
    height: 180px;
  }

  .card-body {
    height: calc(100% - 180px);
    padding: var(--spacing-md);
    min-height: 210px;
  }

  .card-title {
    font-size: 1.3rem;
  }

  .card-subtitle {
    font-size: 0.95rem;
  }

  .card-actions {
    flex-direction: column;
    gap: var(--spacing-sm);
    margin-top: var(--spacing-md);
  }

  .action-btn {
    min-height: 40px;
    padding: var(--spacing-sm) var(--spacing-md);
  }
}

@media (max-width: 768px) {
  .carousel-card {
    width: 300px;
    height: 370px;
  }

  .card-header {
    height: 160px;
  }

  .card-body {
    height: calc(100% - 160px);
    min-height: 210px;
  }

  .card-title {
    font-size: 1.2rem;
  }

  .card-features {
    gap: var(--spacing-xs);
  }

  .feature {
    font-size: 0.85rem;
  }

  .feature-icon {
    width: 20px;
    height: 20px;
  }
}

@media (max-width: 640px) {
  .carousel-card {
    width: 280px;
    height: 350px;
  }

  .card-header {
    height: 150px;
  }

  .card-body {
    height: calc(100% - 150px);
    padding: var(--spacing-sm);
    min-height: 200px;
  }

  .card-title {
    font-size: 1.1rem;
  }

  .card-subtitle {
    font-size: 0.9rem;
  }

  .card-features {
    display: none; /* Скрываем фичи на очень маленьких экранах */
  }
}

@media (max-width: 480px) {
  .carousel-card {
    width: 260px;
    height: 330px;
  }

  .card-header {
    height: 140px;
  }

  .card-body {
    height: calc(100% - 140px);
    min-height: 190px;
  }

  .card-actions {
    margin-top: var(--spacing-sm);
  }
}

/* Темная тема */
[data-theme='dark'] .carousel-card {
  background: var(--color-bg-elevated);
  border-color: var(--color-border-strong);
}

[data-theme='dark'] .feature-icon {
  background: var(--color-primary-muted);
}
</style>
