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
            <path d="M15 18L9 12L15 6" :stroke="navColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
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
            <path d="M9 18L15 12L9 6" :stroke="navColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>

      <!-- Индикаторы -->
      <div class="carousel-indicators">
        <button
          v-for="(card, index) in cards"
          :key="`indicator-${card.id}`"
          :class="['indicator', { 'active': currentIndex === index }]"
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

// Реактивные данные
const currentIndex = ref(1)
const translateDistance = ref(140) // Уменьшил расстояние для компактной карусели

// Данные карточек с полной информацией
const cards = ref([
  { 
    id: 1, 
    title: 'CFDChamp Pro Series', 
    subtitle: 'Элитные соревнования с призовым фондом до $50,000',
    img: '/images/tournament.jpg',
    description: 'Премиальная серия турниров для профессиональных трейдеров. Участвуйте в еженедельных соревнованиях, демонстрируйте свои навыки и соревнуйтесь с лучшими трейдерами со всего мира. Каждый турнир предлагает уникальные условия и вызовы.',
    duration: '2 недели',
    participants: '500+ участников',
    prize: '$50,000',
    features: [
      {
        icon: '🎯',
        title: 'Профессиональная аналитика',
        text: 'Доступ к премиум инструментам анализа рынка'
      },
      {
        icon: '📊',
        title: 'Реальные-time данные',
        text: 'Работа с актуальными рыночными данными'
      },
      {
        icon: '🏆',
        title: 'Эксклюзивные награды',
        text: 'Уникальные призы и признание в сообществе'
      },
      {
        icon: '👨‍💼',
        title: 'Менторская поддержка',
        text: 'Консультации от опытных профессионалов'
      }
    ]
  },
  { 
    id: 2, 
    title: 'Командные баталии', 
    subtitle: 'Объединяйтесь с командой и покоряйте вершины вместе',
    img: '/images/team-battle.jpg',
    description: 'Командные соревнования где стратегия и координация решают все. Соберите команду единомышленников, разрабатывайте совместные стратегии и соревнуйтесь с другими командами за звание лучшей торговой команды сезона.',
    duration: '1 месяц',
    participants: '200 команд',
    prize: '$25,000',
    features: [
      {
        icon: '🤝',
        title: 'Командная стратегия',
        text: 'Совместная разработка торговых подходов'
      },
      {
        icon: '📈',
        title: 'Синхронная торговля',
        text: 'Координация действий в реальном времени'
      },
      {
        icon: '🎮',
        title: 'Тактические сессии',
        text: 'Совместные обсуждения и планирование'
      },
      {
        icon: '🌟',
        title: 'Лидерборды команд',
        text: 'Рейтинги и статистика командных результатов'
      }
    ]
  },
  { 
    id: 3, 
    title: 'Образовательная платформа', 
    subtitle: 'Мастер-классы от профессионалов индустрии',
    img: '/images/education.jpg',
    description: 'Комплексная образовательная программа для трейдеров всех уровней. От начинающих до продвинутых стратегий. Интерактивные курсы, вебинары с экспертами и практические задания помогут вам совершенствовать свои навыки.',
    duration: 'Постоянно',
    participants: '1000+ студентов',
    prize: 'Сертификаты',
    features: [
      {
        icon: '📚',
        title: 'Структурированные курсы',
        text: 'Пошаговое обучение от основ до продвинутых техник'
      },
      {
        icon: '🎥',
        title: 'Экспертные вебинары',
        text: 'Прямые эфиры с успешными трейдерами'
      },
      {
        icon: '🛠️',
        title: 'Практические задания',
        text: 'Реальные кейсы и торговые симуляции'
      },
      {
        icon: '📱',
        title: 'Мобильное обучение',
        text: 'Доступ к материалам с любого устройства'
      }
    ]
  },
  { 
    id: 4, 
    title: 'Еженедельные турниры', 
    subtitle: 'Быстрые соревнования для всех уровней',
    img: '/images/weekly-tournament.jpg',
    description: 'Регулярные турниры с быстрыми результатами. Идеально подходят для начинающих и опытных трейдеров, желающих проверить свои навыки в сжатые сроки.',
    duration: '1 неделя',
    participants: '300+ участников',
    prize: '$10,000',
    features: [
      {
        icon: '⚡',
        title: 'Быстрый старт',
        text: 'Начните участвовать сразу после регистрации'
      },
      {
        icon: '📅',
        title: 'Регулярность',
        text: 'Новые турниры каждую неделю'
      },
      {
        icon: '🎯',
        title: 'Разные форматы',
        text: 'Разнообразные условия и правила'
      },
      {
        icon: '📊',
        title: 'Мгновенные результаты',
        text: 'Быстрое подведение итогов'
      }
    ]
  }
])

// Вычисляемые свойства
const navColor = computed(() => {
  return getComputedStyle(document.documentElement).getPropertyValue('--color-text-inverted').trim() || '#ffffff'
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
  const scale = diff === 0 ? 1 : 0.75 // Уменьшил масштаб неактивных карточек
  const translateX = diff * translateDistance.value
  const zIndex = diff === 0 ? 3 : 2 - Math.abs(diff)
  const opacity = Math.max(0.5, 1 - Math.abs(diff) * 0.4)
  
  // Добавляем blur для неактивных карточек
  const blur = diff === 0 ? '0px' : '3px'

  return {
    transform: `translate(calc(-50% + ${translateX}px), -50%) scale(${scale})`,
    zIndex: zIndex,
    opacity: opacity,
    filter: `blur(${blur})`
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
      mirror: true
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
}

.carousel-section {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-xl) 0;
  background: var(--color-bg);
  position: relative;
  z-index: 1;
}

.carousel-frame {
  position: relative;
  width: 100%;
  max-width: 1200px;
  height: 375px; /* Уменьшил на 25% с 500px до 375px */
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  padding: 0 100px;
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
  box-shadow: var(--shadow-lg);
  z-index: 20;
  backdrop-filter: var(--backdrop-blur);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.carousel-nav::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--border-radius-full);
  padding: 2px;
  background: var(--gradient-primary);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: subtract;
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.carousel-nav:hover::before {
  opacity: 1;
}

.carousel-nav:hover {
  background: var(--color-primary-hover);
  transform: translateY(-50%) scale(1.1);
  box-shadow: var(--shadow-xl);
}

.carousel-nav:active {
  transform: translateY(-50%) scale(0.95);
}

.carousel-nav-prev {
  left: 20px;
}

.carousel-nav-next {
  right: 20px;
}

.carousel-indicators {
  display: flex;
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
  max-width: 1000px;
  margin: 0 auto;
  padding: var(--spacing-xl) var(--spacing-lg);
  background: var(--color-bg);
  position: relative;
  z-index: 2;
}

@keyframes pulse {
  0%, 100% {
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
@media (max-width: 1200px) {
  .carousel-frame {
    max-width: 1000px;
    height: 350px;
    padding: 0 80px;
  }
  
  .details-section {
    max-width: 900px;
    padding: var(--spacing-lg) var(--spacing-md);
  }
  
  .carousel-nav {
    width: 44px;
    height: 44px;
  }
  
  .carousel-nav-prev {
    left: 15px;
  }
  
  .carousel-nav-next {
    right: 15px;
  }
}

/* Планшеты */
@media (max-width: 968px) {
  .carousel-section {
    padding: var(--spacing-lg) 0;
    gap: var(--spacing-md);
  }
  
  .carousel-frame {
    max-width: 800px;
    height: 320px;
    padding: 0 70px;
  }
  
  .carousel-nav {
    width: 40px;
    height: 40px;
  }
  
  .carousel-nav-prev {
    left: 10px;
  }
  
  .carousel-nav-next {
    right: 10px;
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
    padding: var(--spacing-lg) var(--spacing-md);
  }
}

/* Большие мобильные */
@media (max-width: 768px) {
  .carousel-section {
    padding: var(--spacing-md) 0;
  }
  
  .carousel-frame {
    max-width: 100%;
    height: 280px;
    padding: 0 60px;
  }
  
  .carousel-nav {
    width: 36px;
    height: 36px;
  }
  
  .carousel-nav-prev {
    left: 8px;
  }
  
  .carousel-nav-next {
    right: 8px;
  }
  
  .translate-distance {
    transform: translateX(100px);
  }
  
  .details-section {
    padding: var(--spacing-md);
    max-width: 100%;
  }
}

/* Мобильные устройства */
@media (max-width: 640px) {
  .carousel-frame {
    height: 250px;
    padding: 0 50px;
  }
  
  .carousel-nav {
    width: 32px;
    height: 32px;
  }
  
  .carousel-nav-prev {
    left: 5px;
  }
  
  .carousel-nav-next {
    right: 5px;
  }
  
  .carousel-indicators {
    padding: 10px 12px;
  }
  
  .indicator {
    width: 8px;
    height: 8px;
  }
}

/* Маленькие мобильные */
@media (max-width: 480px) {
  .carousel-container {
    min-height: auto;
  }
  
  .carousel-section {
    padding: var(--spacing-sm) 0;
    gap: var(--spacing-sm);
  }
  
  .carousel-frame {
    height: 220px;
    padding: 0 40px;
  }
  
  .carousel-nav {
    width: 28px;
    height: 28px;
  }
  
  .carousel-nav svg {
    width: 16px;
    height: 16px;
  }
  
  .carousel-indicators {
    padding: 8px 10px;
    gap: 8px;
  }
  
  .indicator {
    width: 6px;
    height: 6px;
    border-width: 1px;
  }
  
  .details-section {
    padding: var(--spacing-sm);
  }
}

/* Очень маленькие экраны */
@media (max-width: 360px) {
  .carousel-frame {
    height: 200px;
    padding: 0 30px;
  }
  
  .carousel-nav {
    width: 24px;
    height: 24px;
  }
  
  .carousel-nav svg {
    width: 14px;
    height: 14px;
  }
}
</style>