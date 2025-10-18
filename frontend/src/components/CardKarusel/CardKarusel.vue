<template>
  <div class="carousel-container">
    <!-- Карусель карточек -->
    <div class="carousel-section">
      <div class="carousel-frame">
        <button
          class="carousel-nav carousel-nav-prev"
          @click="prevCard"
          aria-label="Предыдущая карточка"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path
              d="M15 18L9 12L15 6"
              :stroke="navColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>

        <div class="carousel-cards-wrapper">
          <div class="carousel-cards">
            <ChildCardKarusel
              v-for="(card, index) in cards"
              :key="card.id"
              :title="card.title"
              :subtitle="card.subtitle"
              :img="card.img"
              :active="currentIndex === index"
              :card-style="getCardStyle(index)"
              @card-click="goToCard(index)"
            />
          </div>
        </div>

        <button
          class="carousel-nav carousel-nav-next"
          @click="nextCard"
          aria-label="Следующая карточка"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path
              d="M9 18L15 12L9 6"
              :stroke="navColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
      </div>

      <!-- Индикаторы -->
      <div class="carousel-indicators">
        <button
          v-for="(card, index) in cards"
          :key="`indicator-${card.id}`"
          :class="['indicator', { active: currentIndex === index }]"
          @click="goToCard(index)"
          :aria-label="`Перейти к карточке ${index + 1}`"
        >
          <div class="indicator-progress" v-if="currentIndex === index"></div>
        </button>
      </div>
    </div>

    <!-- Детальная информация -->
    <div class="details-section">
      <CarouselDetails
        :title="currentCard.title"
        :description="currentCard.description"
        :duration="currentCard.duration"
        :participants="currentCard.participants"
        :prize="currentCard.prize"
        :features="currentCard.features"
      />

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import ChildCardKarusel from './ChildCardKarusel.vue'
import CarouselDetails from './CarouselDetails.vue'

import { storeToRefs } from 'pinia'
import { useCardStoreData } from '@/stores/useCardStoreData'

// Реактивные данные
const currentIndex = ref(1)
const translateDistance = ref(140)
const { getData: cards } = storeToRefs(useCardStoreData())

// Вычисляемые свойства
const navColor = computed(() => {
  return (
    getComputedStyle(document.documentElement).getPropertyValue('--color-text-inverted').trim() ||
    '#ffffff'
  )
})

const currentCard = computed(() => {
  return cards.value[currentIndex.value]
})

// Методы
const nextCard = () => {
  currentIndex.value = (currentIndex.value + 1) % cards.value.length
  refreshAOS()
}

const prevCard = () => {
  currentIndex.value = currentIndex.value === 0 ? cards.value.length - 1 : currentIndex.value - 1
  refreshAOS()
}

const goToCard = (index) => {
  currentIndex.value = index
  refreshAOS()
}

const getCardStyle = (index) => {
  const diff = index - currentIndex.value
  const scale = diff === 0 ? 1 : 0.75
  const translateX = diff * translateDistance.value
  const zIndex = diff === 0 ? 3 : 2 - Math.abs(diff)
  const opacity = Math.max(0.3, 1 - Math.abs(diff) * 0.4)
  const blur = diff === 0 ? '0px' : '3px'

  // Скрываем карточки, которые слишком далеко
  const display = Math.abs(diff) > 1 ? 'none' : 'block'

  return {
    transform: `translate(calc(-50% + ${translateX}px), -50%) scale(${scale})`,
    zIndex: zIndex,
    opacity: opacity,
    filter: `blur(${blur})`,
    display: display,
  }
}

const refreshAOS = () => {
  if (typeof AOS !== 'undefined') {
    setTimeout(() => {
      AOS.refresh()
    }, 50)
  }
}

// Хуки жизненного цикла
onMounted(() => {
  if (typeof AOS !== 'undefined') {
    AOS.init({
      duration: 500,
      once: false,
      mirror: true,
    })
  }
})

// Наблюдатель за изменением currentIndex
watch(currentIndex, refreshAOS)
</script>

<style scoped>
.carousel-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 0;
  position: relative;
  overflow: hidden; /* Добавляем чтобы содержимое не выходило за пределы */
}

.carousel-section {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-xl) var(--spacing-md); /* Добавляем боковые паддинги */
  background: var(--color-bg);
  position: relative;
  z-index: 1;
  width: 100%;
  box-sizing: border-box;
}

.carousel-frame {
  position: relative;
  width: 100%;
  max-width: 1400px;
  height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  padding: 0 80px;
  box-sizing: border-box;
}

.carousel-cards-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: visible;
}

.carousel-cards {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Правильное позиционирование карточек с blur эффектом */
.carousel-cards > * {
  position: absolute;
  top: 50%;
  left: 50%;
  transform-origin: center;
  transition: all var(--transition-slow) cubic-bezier(0.4, 0, 0.2, 1);
  filter: blur(0px);
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 56px;
  height: 56px;
  border: none;
  border-radius: var(--border-radius-full);
  background: var(--color-primary);
  color: var(--color-text-inverted);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-xl);
  z-index: 50;
  backdrop-filter: var(--backdrop-blur);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.carousel-nav::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--border-radius-full);
  padding: 2px;
  background: var(--gradient-primary);
  mask:
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  mask-composite: subtract;
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.carousel-nav:hover::before {
  opacity: 1;
}

.carousel-nav:hover {
  background: var(--color-primary-hover);
  transform: translateY(-50%) scale(1.15);
  box-shadow: var(--shadow-2xl);
}

.carousel-nav:active {
  transform: translateY(-50%) scale(0.95);
}

.carousel-nav-prev {
  left: 10px;
}

.carousel-nav-next {
  right: 10px;
}

.carousel-indicators {
  display: flex;
  margin-top: 2rem;
  gap: var(--spacing-md);
  align-items: center;
  padding: var(--spacing-md);
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-xl);
  backdrop-filter: var(--backdrop-blur);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-md);
  z-index: 10;
  position: relative;
}

.indicator {
  position: relative;
  width: 12px;
  height: 12px;
  border-radius: var(--border-radius-full);
  border: 2px solid var(--color-border);
  background: transparent;
  cursor: pointer;
  transition: all var(--transition-normal);
  overflow: hidden;
}

.indicator:hover {
  border-color: var(--color-primary);
  transform: scale(1.2);
}

.indicator.active {
  border-color: var(--color-primary);
  background: var(--color-primary);
  transform: scale(1.2);
}

.indicator-progress {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--gradient-primary);
  border-radius: var(--border-radius-full);
  animation: pulse 2s infinite;
}

.details-section {
  flex: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-xl) var(--spacing-md); /* Добавляем боковые паддинги */
  background: var(--color-bg);
  position: relative;
  z-index: 2;
  box-sizing: border-box;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

/* ========== АДАПТИВНОСТЬ ========== */

/* Большие планшеты и маленькие десктопы */
@media (max-width: 1400px) {
  .carousel-frame {
    max-width: 1200px;
    height: 450px;
    padding: 0 70px;
  }

  .carousel-nav {
    width: 52px;
    height: 52px;
  }

  .carousel-nav-prev {
    left: 15px;
  }

  .carousel-nav-next {
    right: 15px;
  }
}

/* Средние десктопы */
@media (max-width: 1200px) {
  .carousel-frame {
    max-width: 1000px;
    height: 420px;
    padding: 0 60px;
  }

  .details-section {
    max-width: 1000px;
    padding: var(--spacing-lg) var(--spacing-md);
  }

  .carousel-nav {
    width: 48px;
    height: 48px;
  }

  .carousel-nav-prev {
    left: 10px;
  }

  .carousel-nav-next {
    right: 10px;
  }
}

/* Планшеты */
@media (max-width: 968px) {
  .carousel-section {
    padding: var(--spacing-lg) var(--spacing-sm);
    gap: var(--spacing-md);
  }

  .carousel-frame {
    max-width: 800px;
    height: 380px;
    padding: 0 50px;
  }

  .carousel-nav {
    width: 44px;
    height: 44px;
  }

  .carousel-nav-prev {
    left: 5px;
  }

  .carousel-nav-next {
    right: 5px;
  }

  .carousel-indicators {
    padding: var(--spacing-sm);
    gap: var(--spacing-sm);
  }

  .indicator {
    width: 10px;
    height: 10px;
  }

  .details-section {
    max-width: 800px;
    padding: var(--spacing-lg) var(--spacing-sm);
  }
}

/* Большие мобильные */
@media (max-width: 768px) {
  .carousel-section {
    padding: var(--spacing-md) var(--spacing-sm);
  }

  .carousel-frame {
    max-width: 100%;
    height: 350px;
    padding: 0 40px;
  }

  .carousel-nav {
    width: 40px;
    height: 40px;
  }

  .carousel-nav-prev {
    left: 2px;
  }

  .carousel-nav-next {
    right: 2px;
  }

  .details-section {
    padding: var(--spacing-md) var(--spacing-sm);
    max-width: 100%;
  }
}

/* Мобильные устройства */
@media (max-width: 640px) {
  .carousel-container {
    overflow-x: hidden; /* Предотвращаем горизонтальный скролл */
  }

  .carousel-section {
    padding: var(--spacing-md) var(--spacing-xs);
  }

  .carousel-frame {
    height: 320px;
    padding: 0 30px;
  }

  .carousel-nav {
    width: 36px;
    height: 36px;
  }

  .carousel-nav-prev {
    left: 5px; /* Увеличиваем отступ вместо отрицательного */
  }

  .carousel-nav-next {
    right: 5px; /* Увеличиваем отступ вместо отрицательного */
  }

  .carousel-indicators {
    padding: 12px 14px;
    margin-top: 1.5rem;
  }

  .indicator {
    width: 8px;
    height: 8px;
  }

  .details-section {
    padding: var(--spacing-md) var(--spacing-xs);
  }
}

/* Маленькие мобильные */
@media (max-width: 480px) {
  .carousel-container {
    min-height: auto;
    overflow-x: hidden;
  }

  .carousel-section {
    padding: var(--spacing-sm) var(--spacing-xs);
    gap: var(--spacing-sm);
  }

  .carousel-frame {
    height: 300px;
    padding: 0 25px; /* Увеличиваем паддинг для кнопок */
  }

  .carousel-nav {
    width: 32px;
    height: 32px;
  }

  .carousel-nav svg {
    width: 18px;
    height: 18px;
  }

  .carousel-nav-prev {
    left: 8px; /* Фиксируем внутри контейнера */
  }

  .carousel-nav-next {
    right: 8px; /* Фиксируем внутри контейнера */
  }

  .carousel-indicators {
    padding: 10px 12px;
    gap: 10px;
    margin-top: 1rem;
  }

  .indicator {
    width: 7px;
    height: 7px;
    border-width: 1.5px;
  }

  .details-section {
    padding: var(--spacing-sm) var(--spacing-xs);
  }
}

/* Очень маленькие экраны */
@media (max-width: 360px) {
  .carousel-section {
    padding: var(--spacing-sm) var(--spacing-xs);
  }

  .carousel-frame {
    height: 280px;
    padding: 0 20px;
  }

  .carousel-nav {
    width: 28px;
    height: 28px;
  }

  .carousel-nav svg {
    width: 16px;
    height: 16px;
  }

  .carousel-nav-prev {
    left: 5px;
  }

  .carousel-nav-next {
    right: 5px;
  }

  .carousel-indicators {
    padding: 8px 10px;
  }
}

/* Экстремально маленькие экраны */
@media (max-width: 320px) {
  .carousel-frame {
    padding: 0 15px;
  }

  .carousel-nav {
    width: 26px;
    height: 26px;
  }

  .carousel-nav svg {
    width: 14px;
    height: 14px;
  }

  .carousel-nav-prev {
    left: 3px;
  }

  .carousel-nav-next {
    right: 3px;
  }
}
</style>