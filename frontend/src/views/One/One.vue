<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import BtnStar from '@/components/BTN/BtnStar.vue'
import MyRandom from '@/components/Random/MyRandom.vue'

const visibleComponents = ref([])
const isAnimating = ref(false)
const videoRef = ref(null)
const isVideoLoaded = ref(false)
const isVideoPlaying = ref(false)
const currentProgress = ref(0) // Добавляем отдельный счетчик прогресса

// Массив для отслеживания занятых позиций
const occupiedPositions = ref([])

// Функция для проверки пересечения позиций
const isPositionOccupied = (newPos, existingPositions) => {
  const newLeft = parseInt(newPos.left)
  const newTop = parseInt(newPos.top)
  const componentWidth = 300
  const componentHeight = 200
  
  for (const pos of existingPositions) {
    const existingLeft = parseInt(pos.left)
    const existingTop = parseInt(pos.top)
    
    // Проверяем пересечение по осям X и Y
    const horizontalOverlap = 
      newLeft < existingLeft + componentWidth && 
      newLeft + componentWidth > existingLeft
      
    const verticalOverlap = 
      newTop < existingTop + componentHeight && 
      newTop + componentHeight > existingTop
      
    if (horizontalOverlap && verticalOverlap) {
      return true
    }
  }
  return false
}

// Функция для получения случайной позиции без наложения
const getRandomPosition = () => {
  const containerWidth = 1200
  const containerHeight = 600
  const componentWidth = 300
  const componentHeight = 200
  
  const maxLeft = containerWidth - componentWidth
  const maxTop = containerHeight - componentHeight
  
  let attempts = 0
  const maxAttempts = 100
  
  while (attempts < maxAttempts) {
    const left = Math.max(0, Math.floor(Math.random() * maxLeft))
    const top = Math.max(0, Math.floor(Math.random() * maxTop))
    
    const newPosition = {
      left: left + 'px',
      top: top + 'px'
    }
    
    if (!isPositionOccupied(newPosition, occupiedPositions.value)) {
      occupiedPositions.value.push(newPosition)
      return newPosition
    }
    
    attempts++
  }
  
  console.warn('Не удалось найти свободную позицию после', maxAttempts, 'попыток')
  return {
    left: (containerWidth / 2 - componentWidth / 2) + 'px',
    top: (containerHeight / 2 - componentHeight / 2) + 'px'
  }
}

// Управление видео
const startVideo = async () => {
  if (videoRef.value && !isVideoPlaying.value) {
    try {
      await videoRef.value.play()
      isVideoPlaying.value = true
      console.log('Видео запущено')
    } catch (error) {
      console.log('Ошибка воспроизведения видео:', error)
      isVideoPlaying.value = false
    }
  }
}

const stopVideo = () => {
  if (videoRef.value && isVideoPlaying.value) {
    videoRef.value.pause()
    videoRef.value.currentTime = 0
    isVideoPlaying.value = false
    console.log('Видео остановлено')
  }
}

const onVideoLoad = () => {
  isVideoLoaded.value = true
  console.log('Видео загружено')
}

const onVideoError = () => {
  console.error('Ошибка загрузки видео')
  isVideoLoaded.value = false
}

const showMultipleRandom = async () => {
  if (isAnimating.value) return
  
  await startVideo()
  
  isAnimating.value = true
  visibleComponents.value = []
  occupiedPositions.value = []
  currentProgress.value = 0 // Сбрасываем прогресс
  
  const totalComponents = 10
  
  for (let i = 0; i < totalComponents; i++) {
    // Обновляем прогресс при начале показа нового компонента
    currentProgress.value = i + 1
    
    if (i > 0) {
      // Ждем исчезновения предыдущего компонента
      await new Promise(resolve => {
        const checkDisappearance = () => {
          if (visibleComponents.value.length === 0 || 
              !visibleComponents.value[visibleComponents.value.length - 1].visible) {
            resolve()
          } else {
            setTimeout(checkDisappearance, 100)
          }
        }
        checkDisappearance()
      })
      
      await new Promise(resolve => setTimeout(resolve, 500))
    }
    
    const newComponent = {
      id: Date.now() + i,
      visible: true,
      position: getRandomPosition(),
      title: `Компонент ${i + 1}`,
      description: `Это описание для компонента ${i + 1}`,
      features: [
        `Функция ${i + 1}.1`,
        `Функция ${i + 1}.2`,
        `Функция ${i + 1}.3`,
        `Функция ${i + 1}.4`
      ],
      timer: null
    }
    
    visibleComponents.value.push(newComponent)
    
    newComponent.timer = setTimeout(() => {
      const index = visibleComponents.value.findIndex(comp => comp.id === newComponent.id)
      if (index !== -1) {
        visibleComponents.value[index].visible = false
        
        setTimeout(() => {
          const removeIndex = visibleComponents.value.findIndex(comp => comp.id === newComponent.id)
          if (removeIndex !== -1) {
            const positionIndex = occupiedPositions.value.findIndex(pos => 
              pos.left === newComponent.position.left && pos.top === newComponent.position.top
            )
            if (positionIndex !== -1) {
              occupiedPositions.value.splice(positionIndex, 1)
            }
            visibleComponents.value.splice(removeIndex, 1)
          }
        }, 600)
      }
    }, 3000)
  }
  
  // Ждем завершения последней анимации
  await new Promise(resolve => setTimeout(resolve, 4000))
  
  // Сбрасываем прогресс при завершении
  currentProgress.value = 0
  isAnimating.value = false
  stopVideo()
}

// Останавливаем анимацию принудительно
const pauseAnimation = () => {
  if (isAnimating.value) {
    isAnimating.value = false
    currentProgress.value = 0 // Сбрасываем прогресс
    
    visibleComponents.value.forEach(component => {
      if (component.timer) {
        clearTimeout(component.timer)
      }
    })
    
    visibleComponents.value = []
    occupiedPositions.value = []
    stopVideo()
  }
}

// Жизненный цикл
onMounted(() => {
  console.log('Компонент монтирован - видео готово к запуску')
})

onUnmounted(() => {
  pauseAnimation()
  if (videoRef.value) {
    videoRef.value.src = ''
  }
})
</script>

<template>
  <div class="one" data-aos="zoom-in">
    <div class="random-container">
      <!-- Видеофон -->
      <div class="video-background">
        <video
          ref="videoRef"
          muted
          loop
          playsinline
          preload="metadata" 
          @loadeddata="onVideoLoad"
          @error="onVideoError"
          class="background-video"
          :class="{ 'video-playing': isVideoPlaying }"
        >
          <source src="@/assets/Space.mp4" type="video/mp4">
          <div class="video-fallback">
            Ваш браузер не поддерживает видео
          </div>
        </video>
        
        <!-- Состояние когда видео не играет -->
        <div v-if="!isVideoPlaying && !isAnimating" class="video-idle-state">
          <div class="idle-message">
            <h3>Готов к генерации</h3>
            <p>Нажмите кнопку ниже чтобы запустить анимацию</p>
            <p class="animation-info">Компоненты будут появляться по одному и исчезать через 3 секунды</p>
          </div>
        </div>
      </div>
      
      <!-- Компоненты поверх видео -->
      <TransitionGroup name="stagger">
        <MyRandom 
          v-for="component in visibleComponents" 
          :key="component.id"
          :title="component.title"
          :description="component.description"
          :features="component.features"
          :class="['random-item', { 'visible': component.visible }]"
          :style="component.position"
        />
      </TransitionGroup>
      
      <!-- Индикатор загрузки видео -->
      <div v-if="!isVideoLoaded && !isVideoPlaying" class="video-loading">
        Загрузка фона...
      </div>
      
      <!-- Счетчик и прогресс -->
      <div v-if="isAnimating" class="animation-progress">
        <div class="progress-text">
          Прогресс: {{ currentProgress }}/10
        </div>
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            :style="{ width: (currentProgress / 10) * 100 + '%' }"
          ></div>
        </div>
        <div class="progress-details">
          <span class="detail-item">Текущий: {{ currentProgress }}</span>
          <span class="detail-item">Видимых: {{ visibleComponents.filter(c => c.visible).length }}</span>
        </div>
      </div>
    </div>
    
    <div class="controls">
      <BtnStar 
        variant="secondary" 
        :text="isAnimating ? `Генерация... (${currentProgress}/10)` : 'Запустить последовательность'" 
        size="medium"
        :disabled="isAnimating"
        @click="showMultipleRandom"
      />
      
      <BtnStar 
        v-if="isAnimating"
        variant="outline" 
        text="Остановить" 
        size="small"
        @click="pauseAnimation"
        class="stop-button"
      />
    </div>
    
    <!-- Дополнительная информация -->
    <div v-if="isAnimating" class="animation-stats">
      <div class="stat-item">
        <span class="stat-label">Текущий компонент:</span>
        <span class="stat-value">{{ currentProgress }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Видимых на экране:</span>
        <span class="stat-value">{{ visibleComponents.filter(c => c.visible).length }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Всего показано:</span>
        <span class="stat-value">{{ currentProgress }}/10</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.one {
  position: relative;
  min-height: 70vh;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.random-container {
  position: relative;
  width: 90vw;
  height: 75vh;
  border: 2px dashed rgba(99, 102, 241, 0.5);
  border-radius: 12px;
  margin: 20px 0;
  background: rgba(99, 102, 241, 0.05);
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

/* Стили для видеофона */
.video-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  overflow: hidden;
}

.background-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

/* Состояние ожидания */
.video-idle-state {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  background: rgba(12, 12, 46, 0.9);
}

.idle-message {
  text-align: center;
  color: white;
  padding: 20px;
  max-width: 80%;
}

.idle-message h3 {
  margin-bottom: 10px;
  font-size: 24px;
  color: #6366f1;
}

.animation-info {
  font-size: 14px !important;
  opacity: 0.6 !important;
  margin-top: 10px !important;
}

/* Улучшенный прогресс анимации */
.animation-progress {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(0, 0, 0, 0.85);
  color: white;
  padding: 12px 16px;
  border-radius: 10px;
  z-index: 4;
  min-width: 180px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.progress-text {
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 6px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  transition: width 0.5s ease;
  border-radius: 3px;
}

.progress-details {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  opacity: 0.7;
}

.detail-item {
  padding: 2px 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

/* Статистика анимации */
.animation-stats {
  display: flex;
  gap: 20px;
  margin-top: 15px;
  padding: 15px 20px;
  background: rgba(99, 102, 241, 0.08);
  border-radius: 12px;
  border: 1px solid rgba(99, 102, 241, 0.15);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.stat-value {
  font-size: 16px;
  font-weight: 700;
  color: #6366f1;
}

/* Стили для компонентов */
.random-item {
  position: absolute;
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
  width: 300px;
  height: 200px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  max-width: calc(100% - 20px);
  max-height: calc(100% - 20px);
}

.random-item.visible {
  z-index: 3;
  box-shadow: 
    0 0 20px rgba(99, 102, 241, 0.6),
    0 0 40px rgba(99, 102, 241, 0.3);
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(99, 102, 241, 0.5);
}

/* Управляющие кнопки */
.controls {
  display: flex;
  gap: 15px;
  align-items: center;
  margin-top: 20px;
}

.stop-button {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.stop-button:hover {
  background: rgba(239, 68, 68, 0.2);
}

/* Анимации */
.stagger-enter-active {
  animation: slide-in 0.6s ease-out both;
}

.stagger-leave-active {
  animation: slide-out 0.6s ease-in both;
  position: absolute !important;
}

@keyframes slide-in {
  0% {
    opacity: 0;
    transform: scale(0.8) translateY(20px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes slide-out {
  0% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
  100% {
    opacity: 0;
    transform: scale(0.8) translateY(-20px);
  }
}

/* Адаптивность */
@media (max-width: 768px) {
  .animation-stats {
    flex-direction: column;
    gap: 10px;
  }
  
  .animation-progress {
    min-width: 160px;
    padding: 10px 12px;
  }
  
  .progress-details {
    flex-direction: column;
    gap: 2px;
  }
}
</style>