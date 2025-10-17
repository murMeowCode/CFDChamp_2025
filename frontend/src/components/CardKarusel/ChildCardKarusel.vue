<template>
  <div 
    :class="['carousel-card', { 'active': active }]"
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
        
        <!-- Skeleton loader как fallback -->
        <div class="skeleton-content" v-if="!title && !subtitle">
          <div class="line" style="width: 100%"></div>
          <div class="line" style="width: 90%"></div>
          <div class="line" style="width: 70%"></div>
          <div class="line" style="width: 80%"></div>
          <div class="line" style="width: 50%"></div>
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
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  img: {
    type: String,
    default: ''
  },
  active: {
    type: Boolean,
    default: false
  },
  cardStyle: {
    type: Object,
    default: () => ({})
  }
})

// Emits
defineEmits(['card-click'])
</script>

<style scoped>
.carousel-card {
  position: relative;
  width: 480px;
  height: 520px;
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-2xl);
  overflow: hidden;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--color-border);
  transition: all var(--transition-slow) cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.carousel-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--border-radius-2xl);
  padding: 2px;
  background: var(--gradient-primary);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
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
  height: 45%;
  position: relative;
  overflow: hidden;
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
    radial-gradient(circle at 20% 80%, rgba(255,255,255,0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255,255,255,0.05) 0%, transparent 50%);
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
  background: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.3) 100%);
}

.carousel-card:hover .card-image img {
  transform: scale(1.08);
}

.card-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  background: var(--color-primary);
  color: var(--color-text-inverted);
  padding: 8px 16px;
  border-radius: var(--border-radius-full);
  font-size: 0.8rem;
  font-weight: var(--font-weight-semibold);
  box-shadow: var(--shadow-md);
  backdrop-filter: var(--backdrop-blur);
}

.card-body {
  height: 55%;
  padding: var(--spacing-xl);
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.card-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}

.meta-dot {
  width: 8px;
  height: 8px;
  border-radius: var(--border-radius-full);
  background: var(--color-primary);
  animation: pulse 2s infinite;
}

.meta-text {
  font-size: 0.8rem;
  font-weight: var(--font-weight-medium);
  color: var(--color-primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-title {
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

.card-subtitle {
  font-size: 1.1rem;
  color: var(--color-text-muted);
  margin: 0;
  line-height: 1.5;
}

.card-features {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-md);
}

.feature {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 0.9rem;
  color: var(--color-text-muted);
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
}

.skeleton-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  flex: 1;
  justify-content: space-between;
}

.line {
  height: 16px;
  background: var(--color-bg-muted);
  border-radius: var(--border-radius-full);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.line::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  animation: shimmer 2s infinite;
}

.card-actions {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xl);
}

.action-btn {
  flex: 1;
  padding: var(--spacing-md) var(--spacing-lg);
  border: none;
  border-radius: var(--border-radius-lg);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-normal);
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
  inset: 0;
  border-radius: var(--border-radius-2xl);
  box-shadow: 
    0 0 80px 20px rgba(59, 130, 246, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  pointer-events: none;
  z-index: 0;
}

/* Анимации */
@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

/* Адаптивность */
@media (max-width: 1200px) {
  .carousel-card {
    width: 420px;
    height: 460px;
  }
  
  .card-title {
    font-size: 1.5rem;
  }
}

@media (max-width: 768px) {
  .carousel-card {
    width: 340px;
    height: 380px;
  }
  
  .card-body {
    padding: var(--spacing-lg);
  }
  
  .card-title {
    font-size: 1.3rem;
  }
  
  .card-subtitle {
    font-size: 1rem;
  }
  
  .card-actions {
    flex-direction: column;
    gap: var(--spacing-sm);
  }
}

@media (max-width: 480px) {
  .carousel-card {
    width: 280px;
    height: 320px;
  }
  
  .card-body {
    padding: var(--spacing-md);
  }
  
  .card-title {
    font-size: 1.1rem;
  }
  
  .card-features {
    display: none;
  }
  
  .line {
    height: 12px;
  }
}

/* Темная тема */
[data-theme='dark'] .carousel-card {
  background: var(--color-bg-elevated);
  border-color: var(--color-border-strong);
}

[data-theme='dark'] .line {
  background: var(--color-bg-muted);
}

[data-theme='dark'] .feature-icon {
  background: var(--color-primary-muted);
}
</style>