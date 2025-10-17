<template>
  <div class="details-container" data-aos="fade-up" data-aos-duration="600">
    <div class="details-content">
      <!-- Заголовок и мета-информация в одну строку -->
      <div class="details-header">
        <div class="header-main">
          <h3 class="details-title">{{ title }}</h3>
          <p class="details-description">{{ description }}</p>
        </div>
        
        <div class="header-meta">
          <div class="meta-grid">
            <div class="meta-item">
              <div class="meta-icon">⏱️</div>
              <div class="meta-content">
                <span class="meta-label">Длительность</span>
                <span class="meta-value">{{ duration }}</span>
              </div>
            </div>
            <div class="meta-item">
              <div class="meta-icon">👥</div>
              <div class="meta-content">
                <span class="meta-label">Участники</span>
                <span class="meta-value">{{ participants }}</span>
              </div>
            </div>
            <div class="meta-item">
              <div class="meta-icon">💰</div>
              <div class="meta-content">
                <span class="meta-label">Призовой фонд</span>
                <span class="meta-value">{{ prize }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Особенности в компактном виде -->
      <div class="details-features">
        <h4 class="features-title">Ключевые особенности</h4>
        <div class="features-grid">
          <div 
            v-for="(feature, index) in features" 
            :key="index"
            class="feature-item"
            data-aos="fade-right"
            :data-aos-delay="index * 100"
          >
            <div class="feature-icon-wrapper">
              <div class="feature-icon">{{ feature.icon }}</div>
            </div>
            <div class="feature-content">
              <h5 class="feature-title">{{ feature.title }}</h5>
              <p class="feature-text">{{ feature.text }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Кнопки действий -->
      <div class="details-actions">
        <button class="details-btn primary">
          <span>Принять участие</span>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <button class="details-btn secondary">
          <span>Подробнее о правилах</span>
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
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  duration: {
    type: String,
    default: ''
  },
  participants: {
    type: String,
    default: ''
  },
  prize: {
    type: String,
    default: ''
  },
  features: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.details-container {
  width: 100%;
  height: 100%;
}

.details-content {
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-2xl);
  padding: var(--spacing-2xl);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.details-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-primary);
}

.details-header {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-2xl);
  margin-bottom: var(--spacing-xl);
  align-items: start;
}

.header-main {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.details-title {
  font-size: 1.75rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin: 0;
  line-height: 1.2;
  background: linear-gradient(135deg, var(--color-text) 0%, var(--color-text-muted) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.details-description {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--color-text);
  margin: 0;
  opacity: 0.9;
}

.header-meta {
  display: flex;
  justify-content: flex-end;
}

.meta-grid {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  min-width: 200px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--color-primary-soft);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-primary-muted);
}

.meta-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.meta-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.meta-label {
  font-size: 0.8rem;
  font-weight: var(--font-weight-medium);
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.meta-value {
  font-size: 0.95rem;
  font-weight: var(--font-weight-semibold);
  color: var(--color-primary);
}

.details-features {
  flex: 1;
  margin-bottom: var(--spacing-xl);
}

.features-title {
  font-size: 1.25rem;
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin: 0 0 var(--spacing-lg) 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-md);
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: var(--color-bg-muted);
  border-radius: var(--border-radius-xl);
  border: 1px solid var(--color-border);
  transition: all var(--transition-normal);
  height: fit-content;
}

.feature-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary);
}

.feature-icon-wrapper {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-primary);
  border-radius: var(--border-radius-lg);
  font-size: 1.2rem;
}

.feature-content {
  flex: 1;
}

.feature-title {
  font-size: 1rem;
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin: 0 0 var(--spacing-xs) 0;
}

.feature-text {
  font-size: 0.85rem;
  line-height: 1.4;
  color: var(--color-text-muted);
  margin: 0;
}

.details-actions {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
  justify-content: center;
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--color-border);
  margin-top: auto;
}

.details-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-2xl);
  border: none;
  border-radius: var(--border-radius-lg);
  font-weight: var(--font-weight-medium);
  font-size: 1rem;
  cursor: pointer;
  transition: all var(--transition-normal);
  text-decoration: none;
}

.details-btn.primary {
  background: var(--gradient-primary);
  color: var(--color-text-inverted);
  box-shadow: var(--shadow-md);
}

.details-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.details-btn.secondary {
  background: transparent;
  color: var(--color-text);
  border: 2px solid var(--color-border);
}

.details-btn.secondary:hover {
  background: var(--color-bg-muted);
  border-color: var(--color-border-hover);
}

/* Адаптивность */
@media (max-width: 968px) {
  .details-header {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
  }
  
  .header-meta {
    justify-content: flex-start;
  }
  
  .meta-grid {
    flex-direction: row;
    flex-wrap: wrap;
    width: 100%;
  }
  
  .meta-item {
    flex: 1;
    min-width: 150px;
  }
}

@media (max-width: 768px) {
  .details-content {
    padding: var(--spacing-xl);
  }
  
  .details-title {
    font-size: 1.5rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .details-actions {
    flex-direction: column;
  }
  
  .details-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .details-content {
    padding: var(--spacing-lg);
  }
  
  .meta-grid {
    flex-direction: column;
  }
  
  .meta-item {
    width: 100%;
  }
  
  .feature-item {
    padding: var(--spacing-md);
  }
}

/* Темная тема */
[data-theme='dark'] .details-content {
  background: var(--color-bg-elevated);
  border-color: var(--color-border-strong);
}

[data-theme='dark'] .feature-item {
  background: var(--color-bg-muted);
  border-color: var(--color-border-strong);
}

[data-theme='dark'] .meta-item {
  background: var(--color-primary-muted);
}
</style>