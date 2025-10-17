<template>
  <div class="details-container" data-aos="fade-up" data-aos-duration="600">
    <div class="details-content">
      <div class="details-header">
        <h3 class="details-title">{{ title }}</h3>
        <div class="details-meta">
          <div class="meta-item">
            <div class="meta-icon">⏱️</div>
            <span class="meta-text">{{ duration }}</span>
          </div>
          <div class="meta-item">
            <div class="meta-icon">👥</div>
            <span class="meta-text">{{ participants }}</span>
          </div>
          <div class="meta-item">
            <div class="meta-icon">💰</div>
            <span class="meta-text">{{ prize }}</span>
          </div>
        </div>
      </div>

      <div class="details-body">
        <p class="details-description">{{ description }}</p>
        
        <div class="details-features">
          <div class="feature-grid">
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
                <h4 class="feature-title">{{ feature.title }}</h4>
                <p class="feature-text">{{ feature.text }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="details-actions">
          <button class="details-btn primary">
            <span>Принять участие</span>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button class="details-btn secondary">
            <span>Подробнее</span>
          </button>
        </div>
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
  max-width: 800px;
  margin: 0 auto;
  padding: var(--spacing-2xl) 0;
}

.details-content {
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-2xl);
  padding: var(--spacing-2xl);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
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
  display: flex;
  justify-content: between;
  align-items: flex-start;
  margin-bottom: var(--spacing-xl);
  gap: var(--spacing-xl);
}

.details-title {
  font-size: 2rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin: 0;
  flex: 1;
  background: linear-gradient(135deg, var(--color-text) 0%, var(--color-text-muted) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.details-meta {
  display: flex;
  gap: var(--spacing-lg);
  flex-shrink: 0;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-primary-soft);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-primary-muted);
}

.meta-icon {
  font-size: 0.9rem;
}

.meta-text {
  font-size: 0.9rem;
  font-weight: var(--font-weight-medium);
  color: var(--color-primary);
}

.details-body {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2xl);
}

.details-description {
  font-size: 1.1rem;
  line-height: 1.7;
  color: var(--color-text);
  margin: 0;
  padding: var(--spacing-lg);
  background: var(--color-bg-muted);
  border-radius: var(--border-radius-xl);
  border-left: 4px solid var(--color-primary);
}

.details-features {
  margin: var(--spacing-xl) 0;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
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
  font-size: 1.1rem;
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin: 0 0 var(--spacing-xs) 0;
}

.feature-text {
  font-size: 0.9rem;
  line-height: 1.5;
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
@media (max-width: 768px) {
  .details-container {
    padding: var(--spacing-xl) var(--spacing-md);
  }
  
  .details-content {
    padding: var(--spacing-xl);
  }
  
  .details-header {
    flex-direction: column;
    gap: var(--spacing-lg);
  }
  
  .details-title {
    font-size: 1.5rem;
  }
  
  .details-meta {
    justify-content: center;
    width: 100%;
  }
  
  .feature-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
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
  
  .details-title {
    font-size: 1.3rem;
  }
  
  .details-meta {
    flex-direction: column;
    align-items: center;
  }
  
  .meta-item {
    width: 100%;
    justify-content: center;
  }
  
  .details-description {
    padding: var(--spacing-md);
    font-size: 1rem;
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

[data-theme='dark'] .details-description {
  background: var(--color-bg-muted);
}

[data-theme='dark'] .feature-item {
  background: var(--color-bg-muted);
  border-color: var(--color-border-strong);
}

[data-theme='dark'] .meta-item {
  background: var(--color-primary-muted);
}
</style>