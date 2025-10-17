<template>
  <div class="carousel-container">
    <div class="carousel-frame">
      <button 
        class="carousel-nav carousel-nav-prev" 
        @click="prevCard"
        aria-label="Предыдущая карточка"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M15 18L9 12L15 6" :stroke="navColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      
      <div class="carousel-cards">
        <div 
          v-for="(card, index) in cards" 
          :key="card.id"
          :class="['card', `card-${index + 1}`, { 'active': currentIndex === index }]"
          :style="getCardStyle(index)"
          data-aos="fade-up"
          :data-aos-duration="500"
          :data-aos-delay="index * 100"
        >
          <div class="card-top"></div>
          <div class="card-content">
            <div class="line" style="width: 100%"></div>
            <div class="line" style="width: 90%"></div>
            <div class="line" style="width: 70%"></div>
            <div class="line" style="width: 80%"></div>
            <div class="line" style="width: 50%"></div>
          </div>
        </div>
      </div>

      <button 
        class="carousel-nav carousel-nav-next" 
        @click="nextCard"
        aria-label="Следующая карточка"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M9 18L15 12L9 6" :stroke="navColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>

    <div class="carousel-indicators">
      <button
        v-for="(card, index) in cards"
        :key="`indicator-${card.id}`"
        :class="['indicator', { 'active': currentIndex === index }]"
        @click="goToCard(index)"
        :aria-label="`Перейти к карточке ${index + 1}`"
      ></button>
    </div>
  </div>
</template>

<script setup>
import { AOS } from 'aos'
import { ref, computed, onMounted, watch } from 'vue'

// Реактивные данные
const currentIndex = ref(1) // Начинаем с центральной карточки
const translateDistance = ref(120)

// Данные карточек
const cards = ref([
  { id: 1, content: 'Card 1' },
  { id: 2, content: 'Card 2' },
  { id: 3, content: 'Card 3' }
])

// Вычисляемые свойства
const navColor = computed(() => {
  return getComputedStyle(document.documentElement).getPropertyValue('--color-text-inverted').trim() || '#ffffff'
})

// Методы
const nextCard = () => {
 
  currentIndex.value = (currentIndex.value + 1) % cards.value.length
}

const prevCard = () => {
 
  currentIndex.value = currentIndex.value === 0 ? cards.value.length - 1 : currentIndex.value - 1
}

const goToCard = (index) => {

  currentIndex.value = index
}

const getCardStyle = (index) => {
  const diff = index - currentIndex.value
  const scale = diff === 0 ? 1 : 0.85
  const translateX = diff * translateDistance.value
  const zIndex = diff === 0 ? 3 : 2 - Math.abs(diff)
  const opacity = Math.max(0.6, 1 - Math.abs(diff) * 0.3)

  return {
    transform: `translateX(${translateX}px) scale(${scale})`,
    zIndex: zIndex,
    opacity: opacity
  }
}

// Хуки жизненного цикла
onMounted(() => {
  // Инициализируем AOS если еще не инициализирована
  if (typeof AOS !== 'undefined') {
    AOS.init({
      duration: 500,
      once: false,
      mirror: true
    })
  }
})

// Наблюдатель за изменением currentIndex для обновления AOS
watch(currentIndex, () => {
  if (typeof AOS !== 'undefined') {
    // Небольшая задержка для обновления после смены карточки
    setTimeout(() => {
      AOS.refresh()
    }, 50)
  }
})
</script>

<style scoped>
.carousel-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xl);
  padding: var(--spacing-2xl) 0;
}

.carousel-frame {
  position: relative;
  width: 100%;
  max-width: 500px;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-cards {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  position: absolute;
  width: 280px;
  height: 240px;
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--color-border);
  transition: all var(--transition-slow) cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.card:hover {
  box-shadow: var(--shadow-xl);
  transform: translateY(-5px) scale(1.02);
}

.card.active:hover {
  transform: translateY(-5px) scale(1.05);
}

.card-top {
  width: 100%;
  height: 20%;
  background: var(--color-primary);
  position: relative;
  overflow: hidden;
}

.card-top::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
}

.card-content {
  padding: 16% 12%;
  height: 80%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.line {
  height: 12px;
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

.card:hover .line {
  background: var(--color-border);
}

.card.active .line {
  background: var(--color-primary-soft);
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  border: none;
  border-radius: var(--border-radius-full);
  background: var(--color-primary);
  color: var(--color-text-inverted);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-md);
  z-index: 10;
}

.carousel-nav:hover {
  background: var(--color-primary-hover);
  transform: translateY(-50%) scale(1.1);
  box-shadow: var(--shadow-lg);
}

.carousel-nav:active {
  transform: translateY(-50%) scale(0.95);
}

.carousel-nav-prev {
  left: -24px;
}

.carousel-nav-next {
  right: -24px;
}

.carousel-nav:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: translateY(-50%) scale(1);
}

.carousel-nav:disabled:hover {
  background: var(--color-primary);
  transform: translateY(-50%) scale(1);
}

.carousel-indicators {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.indicator {
  width: 12px;
  height: 12px;
  border-radius: var(--border-radius-full);
  border: none;
  background: var(--color-border);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.indicator:hover {
  background: var(--color-primary);
  transform: scale(1.2);
}

.indicator.active {
  background: var(--color-primary);
  transform: scale(1.2);
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

/* Анимации переключения карточек */
.card {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Адаптивность */
@media (max-width: 768px) {
  .carousel-frame {
    max-width: 400px;
    height: 280px;
  }
  
  .card {
    width: 240px;
    height: 200px;
  }
  
  .translate-distance {
    transform: translateX(100px);
  }
  
  .carousel-nav {
    width: 40px;
    height: 40px;
  }
  
  .carousel-nav-prev {
    left: -20px;
  }
  
  .carousel-nav-next {
    right: -20px;
  }
}

@media (max-width: 480px) {
  .carousel-container {
    padding: var(--spacing-lg) 0;
  }
  
  .carousel-frame {
    max-width: 320px;
    height: 250px;
  }
  
  .card {
    width: 200px;
    height: 180px;
  }
  
  .carousel-nav {
    width: 36px;
    height: 36px;
  }
  
  .carousel-nav-prev {
    left: -18px;
  }
  
  .carousel-nav-next {
    right: -18px;
  }
  
  .card-content {
    padding: 12% 10%;
  }
  
  .line {
    height: 10px;
  }
}

/* Темная тема */
[data-theme='dark'] .card {
  background: var(--color-bg-elevated);
  border-color: var(--color-border-strong);
}

[data-theme='dark'] .line {
  background: var(--color-bg-muted);
}

[data-theme='dark'] .card:hover .line {
  background: var(--color-border-hover);
}

[data-theme='dark'] .card.active .line {
  background: var(--color-primary-muted);
}

[data-theme='dark'] .indicator {
  background: var(--color-border-strong);
}
</style>