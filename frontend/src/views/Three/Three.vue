<script setup>
import { ref, provide } from 'vue'
import ContainerGenerate from '@/components/Generate/ContainerGenerate.vue';
import MyTest from '@/components/Test/MyTest.vue';
import TestResultsVisualization from '@/components/Test/TestResultsVisualization.vue';

// Данные тестов, которые будут передаваться в правую колонку
const tests = ref([
  {
    id: 1,
    name: 'ПРОВЕРКА ДЛИНЫ',
    description: 'Верификация корректности длины последовательности',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null
  },
  {
    id: 2,
    name: 'ТЕСТ ЭНТРОПИИ',
    description: 'Анализ случайности и энтропии последовательности',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null
  },
  {
    id: 3,
    name: 'СТАТИСТИЧЕСКИЙ АНАЛИЗ',
    description: 'Проверка статистических свойств',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null
  },
  {
    id: 4,
    name: 'ПРОВЕРКА УНИКАЛЬНОСТИ',
    description: 'Анализ уникальности символов',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null
  }
])

const isAnalyzing = ref(false)
const analysisComplete = ref(false)

// Функции для управления тестами
const startTests = () => {
  isAnalyzing.value = true
  analysisComplete.value = false
  
  // Сбрасываем тесты перед запуском
  tests.value.forEach(test => {
    test.status = 'pending'
    test.progress = 0
    test.duration = null
    test.result = null
  })
}

const updateTestProgress = (testId, progress, status = 'running') => {
  const test = tests.value.find(t => t.id === testId)
  if (test) {
    test.progress = progress
    test.status = status
  }
}

const completeTest = (testId, result, isSuccess = true) => {
  const test = tests.value.find(t => t.id === testId)
  if (test) {
    test.status = isSuccess ? 'success' : 'error'
    test.result = result
    test.progress = 100
  }
}

const completeAllTests = () => {
  analysisComplete.value = true
  isAnalyzing.value = false
}

const resetAnalysis = () => {
  tests.value.forEach(test => {
    test.status = 'pending'
    test.progress = 0
    test.duration = null
    test.result = null
  })
  analysisComplete.value = false
  isAnalyzing.value = false
}

// Передаем функции в дочерние компоненты
provide('testControls', {
  tests,
  startTests,
  updateTestProgress,
  completeTest,
  completeAllTests,
  resetAnalysis
})
</script>

<template>
  <div class="two-column-layout" data-aos="zoom-in">
    <!-- Левая колонка - управление генерацией -->
    <div class="column left-column">
      <div class="left-column-content">
        <ContainerGenerate class="left-component"/>
        <MyTest class="left-component"/>
      </div>
    </div>
    
    <!-- Правая колонка - отображение тестов -->
    <div class="column right-column">
      <TestResultsVisualization 
        :tests="tests"
        :is-analyzing="isAnalyzing"
        :analysis-complete="analysisComplete"
        @repeat-analysis="resetAnalysis"
      />
    </div>
  </div>
</template>

<style scoped>
.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-2xl);
  align-items: start;
  min-height: 80vh;
  padding: var(--spacing-xl);
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
}

.column {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: fit-content;
}

/* Левая колонка - компоненты в строку */
.left-column {
  max-width: 900px;
  display: flex;
  justify-self: end;
}

.left-column-content {
  display: flex;
  flex-direction: row;
  gap: var(--spacing-xl);
  width: 100%;
  align-items: stretch;
}

.left-component {
  flex: 1;
  min-width: 0; /* Для корректного сжатия */
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-xl);
  transition: all var(--transition-normal);
  display: flex;
  flex-direction: column;
}

.left-component:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

/* Правая колонка */
.right-column {
  max-width: 600px;
  justify-self: start;
}

.right-column > * {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
  min-height: 600px;
  padding: var(--spacing-xl);
}

.right-column > *:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

/* Декоративная линия разделения */
.two-column-layout::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 1px;
  height: 80%;
  background: var(--color-border);
  opacity: 0.4;
}

/* Анимация появления */
.left-column {
  animation: slideInLeft 0.6s ease-out;
}

.right-column {
  animation: slideInRight 0.6s ease-out;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Адаптивность для планшетов */
@media (max-width: 1200px) {
  .two-column-layout {
    grid-template-columns: 1fr;
    gap: var(--spacing-xl);
    padding: var(--spacing-lg);
    min-height: auto;
  }
  
  .left-column,
  .right-column {
    max-width: 100%;
    justify-self: center;
  }
  
  .left-column-content {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .two-column-layout::before {
    display: none;
  }
  
  .right-column > * {
    min-height: auto;
  }
  
  /* Изменяем анимацию для мобильных */
  .left-column,
  .right-column {
    animation: fadeInUp 0.6s ease-out;
  }
  
  .right-column {
    animation-delay: 0.1s;
  }
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .two-column-layout {
    padding: var(--spacing-md);
    gap: var(--spacing-lg);
  }
  
  .left-column-content {
    flex-direction: column;
    gap: var(--spacing-lg);
  }
  
  .left-component {
    padding: var(--spacing-lg);
  }
  
  .right-column > * {
    padding: var(--spacing-lg);
  }
}

/* Для очень маленьких экранов */
@media (max-width: 480px) {
  .two-column-layout {
    padding: var(--spacing-sm);
    gap: var(--spacing-md);
  }
  
  .left-component {
    padding: var(--spacing-md);
  }
  
  .right-column > * {
    padding: var(--spacing-md);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Дополнительные стили для лучшего визуального разделения */
.left-component:first-child {
  border-left: 3px solid var(--color-primary);
}

.left-component:last-child {
  border-left: 3px solid var(--color-accent);
}

/* Выравнивание контента внутри компонентов */
.left-component > * {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Гарантируем одинаковую высоту компонентов в строке */
.left-column-content {
  align-items: stretch;
}
</style>