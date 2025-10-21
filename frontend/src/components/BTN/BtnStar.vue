<template>
  <button 
    class="stellar-button"
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="handleClick"
    @mousedown="createRipple"
    ref="buttonRef"
  >
    <!-- Фоновые звезды -->
    <div class="stellar-bg">
      <div 
        v-for="i in starCount" 
        :key="i"
        class="star"
        :style="getStarStyle(i)"
      />
    </div>

    <!-- Содержимое кнопки -->
    <span class="button-content" :class="{ 'content-hidden': loading }">
      <slot>
        {{ text }}
      </slot>
    </span>

    <!-- Лоадер -->
    <div v-if="loading" class="stellar-loader">
      <div 
        v-for="n in 3" 
        :key="n"
        class="orbiting-dot" 
        :style="`--delay: ${(n-1)*0.2}s`"
      />
    </div>

    <!-- Эффект свечения -->
    <div class="glow-effect" :style="{ background: glowColor }" />
    
    <!-- Эффект риппла -->
    <div v-if="ripple.visible" class="ripple-effect" :style="rippleStyle" />
  </button>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'

const props = defineProps({
  text: {
    type: String,
    default: 'Космическая кнопка'
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'ghost'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  color: {
    type: String,
    default: '#6366f1'
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  }
})

const emit = defineEmits(['click'])

const buttonRef = ref(null)
const starCount = 8

const ripple = reactive({
  visible: false,
  x: 0,
  y: 0
})

// Computed свойства
const buttonClasses = computed(() => [
  `stellar-button--${props.variant}`,
  `stellar-button--${props.size}`,
  {
    'stellar-button--loading': props.loading,
    'stellar-button--disabled': props.disabled
  }
])

const glowColor = computed(() => {
  const colors = {
    primary: `radial-gradient(circle, ${props.color}40 0%, transparent 70%)`,
    secondary: 'radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%)',
    ghost: 'radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%)'
  }
  return colors[props.variant]
})

const rippleStyle = computed(() => ({
  left: `${ripple.x}px`,
  top: `${ripple.y}px`,
  background: props.variant === 'ghost' 
    ? 'rgba(255, 255, 255, 0.3)' 
    : `${props.color}40`
}))

// Методы
const getStarStyle = (index) => {
  const angle = (index / starCount) * Math.PI * 2
  const distance = 20 + Math.random() * 30
  return {
    left: `calc(50% + ${Math.cos(angle) * distance}px)`,
    top: `calc(50% + ${Math.sin(angle) * distance}px)`,
    animationDelay: `${index * 0.3}s`,
    opacity: 0.3 + Math.random() * 0.7
  }
}

const handleClick = (event) => {
  if (!props.loading && !props.disabled) {
    emit('click', event)
  }
}

const createRipple = (event) => {
  if (props.loading || props.disabled) return
  
  const button = buttonRef.value
  const rect = button.getBoundingClientRect()
  
  ripple.x = event.clientX - rect.left
  ripple.y = event.clientY - rect.top
  ripple.visible = true
  
  setTimeout(() => {
    ripple.visible = false
  }, 600)
}
</script>

<style scoped>
.stellar-button {
  position: relative;
  border: none;
  border-radius: 12px;
  font-family: 'Segoe UI', system-ui, sans-serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  background: transparent;
  color: white;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  backdrop-filter: blur(10px);
}

/* Размеры */
.stellar-button--small {
  padding: 8px 16px;
  font-size: 0.875rem;
  min-height: 36px;
}

.stellar-button--medium {
  padding: 12px 24px;
  font-size: 1rem;
  min-height: 44px;
}

.stellar-button--large {
  padding: 16px 32px;
  font-size: 1.125rem;
  min-height: 52px;
}

/* Варианты */
.stellar-button--primary {
  background: linear-gradient(135deg, v-bind('props.color') 0%, #4f46e5 100%);
  box-shadow: 
    0 4px 20px v-bind('props.color + "40"'),
    0 0 0 1px rgba(255, 255, 255, 0.1);
}

.stellar-button--secondary {
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.stellar-button--ghost {
  background: transparent;
  color: v-bind('props.color');
  border: 1px solid v-bind('props.color + "40"');
}

/* Состояния */
.stellar-button:hover:not(.stellar-button--disabled):not(.stellar-button--loading) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px v-bind('props.color + "60"'),
    0 0 0 1px rgba(255, 255, 255, 0.2);
}

.stellar-button:active:not(.stellar-button--disabled):not(.stellar-button--loading) {
  transform: translateY(0);
}

.stellar-button--disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.stellar-button--loading {
  cursor: wait;
}

/* Фоновые звезды */
.stellar-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.star {
  position: absolute;
  width: 2px;
  height: 2px;
  background: white;
  border-radius: 50%;
  animation: twinkle 3s infinite ease-in-out;
  transform: translate(-50%, -50%);
}

@keyframes twinkle {
  0%, 100% { 
    opacity: 0.3; 
    transform: translate(-50%, -50%) scale(0.8); 
  }
  50% { 
    opacity: 1; 
    transform: translate(-50%, -50%) scale(1.2); 
  }
}

/* Контент */
.button-content {
  position: relative;
  z-index: 2;
  transition: opacity 0.3s ease;
}

.content-hidden {
  opacity: 0;
}

/* Лоадер */
.stellar-loader {
  position: absolute;
  display: flex;
  gap: 4px;
  z-index: 2;
}

.orbiting-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: currentColor;
  animation: orbit 1.5s infinite ease-in-out;
  animation-delay: var(--delay);
}

@keyframes orbit {
  0%, 100% { 
    transform: translateY(0px); 
    opacity: 0.3;
  }
  50% { 
    transform: translateY(-6px); 
    opacity: 1;
  }
}

/* Эффекты */
.glow-effect {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.stellar-button:hover:not(.stellar-button--disabled):not(.stellar-button--loading) .glow-effect {
  opacity: 1;
}

.ripple-effect {
  position: absolute;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  transform: translate(-50%, -50%) scale(0);
  animation: ripple 0.6s ease-out;
  pointer-events: none;
}

@keyframes ripple {
  to {
    transform: translate(-50%, -50%) scale(10);
    opacity: 0;
  }
}

/* Анимация пульсации для primary кнопки */
.stellar-button--primary:not(.stellar-button--disabled):not(.stellar-button--loading) {
  animation: gentle-pulse 4s infinite ease-in-out;
}

@keyframes gentle-pulse {
  0%, 100% { 
    box-shadow: 
      0 4px 20px v-bind('props.color + "40"'),
      0 0 0 1px rgba(255, 255, 255, 0.1);
  }
  50% { 
    box-shadow: 
      0 4px 30px v-bind('props.color + "60"'),
      0 0 0 1px rgba(255, 255, 255, 0.15);
  }
}
</style>