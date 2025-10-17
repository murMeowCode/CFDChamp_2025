<template>
  <div class="carousel-container">
    <!-- Карусель карточек -->
    <div class="carousel-frame">
      <button 
        class="carousel-nav carousel-nav-prev" 
        @click="prevCard"
        aria-label="Предыдущая карточка"
      >
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
          <path d="M15 18L9 12L15 6" :stroke="navColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      
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

      <button 
        class="carousel-nav carousel-nav-next" 
        @click="nextCard"
        aria-label="Следующая карточка"
      >
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
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

    <!-- Детальная информация -->
    <CarouselDetails
      :title="currentCard.title"
      :description="currentCard.description"
      :duration="currentCard.duration"
      :participants="currentCard.participants"
      :prize="currentCard.prize"
      :features="currentCard.features"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import ChildCardKarusel from './ChildCardKarusel.vue'
import CarouselDetails from './CarouselDetails.vue'

// Реактивные данные
const currentIndex = ref(1)
const translateDistance = ref(200)

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
  const scale = diff === 0 ? 1 : 0.75
  const translateX = diff * translateDistance.value
  const zIndex = diff === 0 ? 3 : 2 - Math.abs(diff)
  const opacity = Math.max(0.4, 1 - Math.abs(diff) * 0.4)

  return {
    transform: `translateX(${translateX}px) scale(${scale})`,
    zIndex: zIndex,
    opacity: opacity
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
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-2xl);
  padding: var(--spacing-2xl) 0;
  position: relative;
}

/* Остальные стили остаются такими же как в предыдущей версии */
.carousel-frame {
  position: relative;
  width: 100%;
  max-width: 1200px;
  height: 600px;
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

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 64px;
  height: 64px;
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
  z-index: 10;
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
  transform: translateY(-50%) scale(1.15);
  box-shadow: var(--shadow-2xl);
}

.carousel-nav:active {
  transform: translateY(-50%) scale(0.95);
}

.carousel-nav-prev {
  left: -32px;
}

.carousel-nav-next {
  right: -32px;
}

.carousel-indicators {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
  padding: var(--spacing-lg);
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-2xl);
  backdrop-filter: var(--backdrop-blur);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-md);
}

.indicator {
  position: relative;
  width: 16px;
  height: 16px;
  border-radius: var(--border-radius-full);
  border: 2px solid var(--color-border);
  background: transparent;
  cursor: pointer;
  transition: all var(--transition-normal);
  overflow: hidden;
}

.indicator:hover {
  border-color: var(--color-primary);
  transform: scale(1.3);
}

.indicator.active {
  border-color: var(--color-primary);
  background: var(--color-primary);
  transform: scale(1.3);
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

/* Адаптивность */
@media (max-width: 1200px) {
  .carousel-frame {
    max-width: 1000px;
    height: 500px;
  }
}

@media (max-width: 768px) {
  .carousel-frame {
    max-width: 700px;
    height: 400px;
  }
  
  .carousel-nav {
    width: 52px;
    height: 52px;
  }
  
  .carousel-nav-prev {
    left: -20px;
  }
  
  .carousel-nav-next {
    right: -20px;
  }
  
  .carousel-indicators {
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
  }
  
  .indicator {
    width: 14px;
    height: 14px;
  }
}

@media (max-width: 480px) {
  .carousel-container {
    padding: var(--spacing-xl) 0;
  }
  
  .carousel-frame {
    max-width: 350px;
    height: 300px;
  }
  
  .carousel-nav {
    width: 44px;
    height: 44px;
  }
  
  .carousel-nav-prev {
    left: -15px;
  }
  
  .carousel-nav-next {
    right: -15px;
  }
  
  .carousel-indicators {
    padding: var(--spacing-sm);
  }
}
</style>