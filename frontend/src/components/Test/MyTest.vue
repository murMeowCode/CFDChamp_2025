<template>
  <div class="file-upload-container">
    <!-- Заголовок -->
    <!-- Основной контейнер -->
    <div class="upload-main">
      <!-- Зона загрузки файла -->
      <div 
        class="upload-zone"
        :class="{
          'drag-over': dragOver,
          'has-file': uploadedFile,
          'uploading': isUploading
        }"
        @drop="onDrop"
        @dragover="onDragOver"
        @dragleave="onDragLeave"
      >
        <div class="upload-content" v-if="!uploadedFile && !isUploading">
          <div class="upload-icon">📁</div>
          <h3 class="upload-title cyber-heading">ПЕРЕТАЩИТЕ ФАЙЛ СЮДА</h3>
          <p class="upload-description futurism-elegant">
            или нажмите для выбора файла
          </p>
          <input
            type="file"
            ref="fileInput"
            @change="onFileSelect"
            class="file-input"
            accept="*/*"
          />
          <button 
            class="cyber-button primary"
            @click="triggerFileInput"
          >
            <span class="button-icon">🔍</span>
            ВЫБРАТЬ ФАЙЛ
          </button>
        </div>

        <!-- Загруженный файл -->
        <div class="file-info" v-if="uploadedFile && !isUploading">
          <div class="file-icon">📄</div>
          <div class="file-details">
            <h4 class="file-name cyber-heading">{{ uploadedFile.name }}</h4>
            <p class="file-size cyber-mono">
              {{ formatFileSize(uploadedFile.size) }}
            </p>
          </div>
          <button 
            class="cyber-button accent"
            @click="startAnalysis"
            :disabled="!uploadedFile"
          >
            <span class="button-icon">⚡</span>
            НАЧАТЬ АНАЛИЗ
          </button>
        </div>

        <!-- Прогресс загрузки -->
        <div class="upload-progress" v-if="isUploading">
          <div class="progress-icon">🔄</div>
          <h4 class="progress-title cyber-heading">ЗАГРУЗКА ФАЙЛА</h4>
          <div class="progress-bar">
            <div 
              class="progress-fill"
              :style="{ width: uploadProgress + '%' }"
            ></div>
          </div>
          <p class="progress-percent cyber-mono">{{ Math.round(uploadProgress) }}%</p>
        </div>
      </div>

      <!-- Визуализация тестов -->
      <div class="tests-visualization" v-if="isAnalyzing">
        <div class="tests-header">
          <h3 class="cyber-heading">
            <span class="text-indigo-theme">ВЫПОЛНЕНИЕ ТЕСТОВ</span>
          </h3>
          <div class="tests-progress">
            <span class="progress-text cyber-mono">
              {{ completedTests }}/{{ totalTests }}
            </span>
            <div class="progress-circle">
              <svg width="60" height="60" viewBox="0 0 60 60">
                <circle
                  cx="30"
                  cy="30"
                  r="27"
                  stroke="var(--color-border)"
                  stroke-width="3"
                  fill="none"
                />
                <circle
                  cx="30"
                  cy="30"
                  r="27"
                  stroke="var(--color-primary)"
                  stroke-width="3"
                  fill="none"
                  stroke-linecap="round"
                  :stroke-dasharray="circumference"
                  :stroke-dashoffset="circumference - (testsProgress / 100) * circumference"
                  transform="rotate(-90 30 30)"
                />
              </svg>
              <span class="circle-percent cyber-mono">
                {{ Math.round(testsProgress) }}%
              </span>
            </div>
          </div>
        </div>

        <!-- Список тестов -->
        <div class="tests-list">
          <div
            v-for="test in tests"
            :key="test.id"
            class="test-item"
            :class="test.status"
          >
            <div class="test-icon">
              <span v-if="test.status === 'pending'">⏳</span>
              <span v-else-if="test.status === 'running'">⚡</span>
              <span v-else-if="test.status === 'success'">✅</span>
              <span v-else-if="test.status === 'error'">❌</span>
            </div>
            <div class="test-content">
              <div class="test-header">
                <span class="test-name cyber-mono">{{ test.name }}</span>
                <span class="test-duration cyber-mono" v-if="test.duration">
                  {{ test.duration }}мс
                </span>
              </div>
              <p class="test-description futurism-elegant">
                {{ test.description }}
              </p>
              <div 
                class="test-progress"
                v-if="test.status === 'running'"
              >
                <div class="test-progress-bar">
                  <div 
                    class="test-progress-fill"
                    :style="{ width: test.progress + '%' }"
                  ></div>
                </div>
              </div>
              <div 
                class="test-result"
                v-if="test.result"
                :class="test.status"
              >
                <span class="result-text cyber-mono">{{ test.result }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Результаты анализа -->
        <div class="analysis-results" v-if="analysisComplete">
          <div class="results-header">
            <h3 class="cyber-heading">
              <span class="text-indigo-theme">РЕЗУЛЬТАТЫ АНАЛИЗА</span>
            </h3>
            <div class="results-summary">
              <div class="summary-item success">
                <span class="summary-count cyber-mono">{{ passedTests }}</span>
                <span class="summary-label cyber-mono">ПРОЙДЕНО</span>
              </div>
              <div class="summary-item error">
                <span class="summary-count cyber-mono">{{ failedTests }}</span>
                <span class="summary-label cyber-mono">ОШИБОК</span>
              </div>
              <div class="summary-item">
                <span class="summary-count cyber-mono">{{ totalTime }}мс</span>
                <span class="summary-label cyber-mono">ВРЕМЯ</span>
              </div>
            </div>
          </div>

          <div class="results-actions">
            <button class="cyber-button primary">
              <span class="button-icon">📊</span>
              ДЕТАЛЬНЫЙ ОТЧЕТ
            </button>
            <button class="cyber-button secondary" @click="resetUpload">
              <span class="button-icon">🔄</span>
              НОВЫЙ АНАЛИЗ
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Статусная панель -->
    <div class="status-panel" v-if="currentStatus">
      <div class="status-indicator" :class="statusType">
        <span class="status-icon">{{ statusIcon }}</span>
        <span class="status-text cyber-mono">{{ currentStatus }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Refs
const fileInput = ref(null)
const dragOver = ref(false)
const uploadedFile = ref(null)
const isUploading = ref(false)
const uploadProgress = ref(0)
const isAnalyzing = ref(false)
const analysisComplete = ref(false)

// Данные тестов
const tests = ref([
  {
    id: 1,
    name: 'ПРОВЕРКА ЦЕЛОСТНОСТИ',
    description: 'Верификация структуры и целостности файла',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null
  },
  {
    id: 2,
    name: 'АНАЛИЗ БЕЗОПАСНОСТИ',
    description: 'Поиск потенциальных угроз и уязвимостей',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null
  },
  {
    id: 3,
    name: 'ПРОВЕРКА СОВМЕСТИМОСТИ',
    description: 'Анализ формата и совместимости с системой',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null
  },
  {
    id: 4,
    name: 'СТАТИСТИЧЕСКИЙ АНАЛИЗ',
    description: 'Сбор статистики и метаданных файла',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null
  },
  {
    id: 5,
    name: 'ФИНАЛЬНАЯ ВЕРИФИКАЦИЯ',
    description: 'Подготовка итогового отчета',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null
  }
])

// Вычисляемые свойства
const totalTests = computed(() => tests.value.length)
const completedTests = computed(() => 
  tests.value.filter(test => test.status === 'success' || test.status === 'error').length
)
const testsProgress = computed(() => (completedTests.value / totalTests.value) * 100)
const passedTests = computed(() => tests.value.filter(test => test.status === 'success').length)
const failedTests = computed(() => tests.value.filter(test => test.status === 'error').length)
const totalTime = computed(() => 
  tests.value.reduce((total, test) => total + (test.duration || 0), 0)
)

const circumference = computed(() => 2 * Math.PI * 27)

const currentStatus = computed(() => {
  if (isUploading.value) return 'Загрузка файла...'
  if (isAnalyzing.value) return 'Выполнение тестов...'
  if (analysisComplete.value) return 'Анализ завершен'
  return 'Ожидание загрузки файла'
})

const statusType = computed(() => {
  if (isUploading.value) return 'warning'
  if (isAnalyzing.value) return 'running'
  if (analysisComplete.value) return 'success'
  return 'idle'
})

const statusIcon = computed(() => {
  switch (statusType.value) {
    case 'warning': return '🔄'
    case 'running': return '⚡'
    case 'success': return '✅'
    default: return '⏸'
  }
})

// Методы
const triggerFileInput = () => {
  fileInput.value?.click()
}

const onFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    handleFile(file)
  }
}

const onDragOver = (event) => {
  event.preventDefault()
  dragOver.value = true
}

const onDragLeave = () => {
  dragOver.value = false
}

const onDrop = (event) => {
  event.preventDefault()
  dragOver.value = false
  
  const file = event.dataTransfer.files[0]
  if (file) {
    handleFile(file)
  }
}

const handleFile = (file) => {
  uploadedFile.value = file
  // Сброс прогресса анализа
  resetAnalysis()
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const startAnalysis = async () => {
  if (!uploadedFile.value) return
  
  isUploading.value = true
  uploadProgress.value = 0
  
  // Имитация загрузки файла
  for (let i = 0; i <= 100; i += 10) {
    await new Promise(resolve => setTimeout(resolve, 100))
    uploadProgress.value = i
  }
  
  isUploading.value = false
  isAnalyzing.value = true
  
  // Запуск тестов
  await runTests()
}

const runTests = async () => {
  for (const test of tests.value) {
    test.status = 'running'
    test.progress = 0
    
    // Имитация выполнения теста
    const startTime = Date.now()
    
    for (let i = 0; i <= 100; i += 20) {
      await new Promise(resolve => setTimeout(resolve, 100 + Math.random() * 200))
      test.progress = i
    }
    
    test.duration = Date.now() - startTime
    
    // Случайный результат для демонстрации
    const isSuccess = Math.random() > 0.2
    test.status = isSuccess ? 'success' : 'error'
    test.result = isSuccess ? 'Тест пройден успешно' : 'Обнаружены проблемы'
  }
  
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

const resetUpload = () => {
  uploadedFile.value = null
  resetAnalysis()
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

onMounted(() => {
  // Инициализация
})
</script>

<style scoped>
.file-upload-container {
  max-width: 800px;
  margin: 0 auto;
  padding: var(--spacing-xl);
}

.upload-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  border-bottom: 2px solid var(--color-border);
  padding-bottom: var(--spacing-lg);
}

.upload-subtitle {
  color: var(--color-text-muted);
  font-size: 1.1rem;
  margin-top: var(--spacing-sm);
}

.upload-main {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.upload-zone {
  border: 3px dashed var(--color-border);
  border-radius: var(--border-radius-xl);
  padding: var(--spacing-2xl);
  text-align: center;
  transition: all var(--transition-normal);
  background: var(--color-bg-elevated);
  position: relative;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-zone.drag-over {
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
  transform: scale(1.02);
}

.upload-zone.has-file {
  border-color: var(--color-success);
  background: var(--color-success-soft);
}

.upload-zone.uploading {
  border-color: var(--color-warning);
  background: var(--color-warning-soft);
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
}

.upload-icon {
  font-size: 3rem;
  opacity: 0.7;
}

.upload-title {
  color: var(--color-text);
  margin: 0;
}

.upload-description {
  color: var(--color-text-muted);
  margin: 0;
}

.file-input {
  display: none;
}

.file-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  width: 100%;
  justify-content: space-between;
}

.file-icon {
  font-size: 2.5rem;
}

.file-details {
  flex: 1;
  text-align: left;
}

.file-name {
  color: var(--color-text);
  margin: 0 0 var(--spacing-xs) 0;
  word-break: break-all;
}

.file-size {
  color: var(--color-text-muted);
  margin: 0;
}

.upload-progress {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
  width: 100%;
}

.progress-icon {
  font-size: 2.5rem;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.progress-title {
  color: var(--color-text);
  margin: 0;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: var(--border-radius-full);
  transition: width var(--transition-normal);
  background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
}

.progress-percent {
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
}

.tests-visualization {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-indigo);
}

.tests-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--spacing-md);
}

.tests-progress {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.progress-text {
  color: var(--color-text-muted);
}

.progress-circle {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.circle-percent {
  position: absolute;
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
  font-size: 0.8rem;
}

.tests-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.test-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
  background: var(--color-bg-subtle);
  transition: all var(--transition-normal);
}

.test-item.running {
  border-color: var(--color-warning);
  background: var(--color-warning-soft);
  box-shadow: 0 0 10px rgba(255, 143, 0, 0.1);
}

.test-item.success {
  border-color: var(--color-success);
  background: var(--color-success-soft);
}

.test-item.error {
  border-color: var(--color-error);
  background: var(--color-error-soft);
}

.test-icon {
  font-size: 1.5rem;
  display: flex;
  align-items: flex-start;
}

.test-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.test-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.test-name {
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
}

.test-duration {
  color: var(--color-text-muted);
  font-size: 0.8rem;
}

.test-description {
  color: var(--color-text-light);
  margin: 0;
  font-size: 0.9rem;
}

.test-progress-bar {
  width: 100%;
  height: 4px;
  background: var(--color-border);
  border-radius: var(--border-radius-full);
  overflow: hidden;
}

.test-progress-fill {
  height: 100%;
  background: var(--color-warning);
  border-radius: var(--border-radius-full);
  transition: width var(--transition-normal);
  background: linear-gradient(90deg, var(--color-warning), var(--color-accent));
}

.test-result {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  font-size: 0.8rem;
}

.test-result.success {
  background: var(--color-success);
  color: var(--color-text-inverted);
}

.test-result.error {
  background: var(--color-error);
  color: var(--color-text-inverted);
}

.analysis-results {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-lg);
  border-top: 2px solid var(--color-border);
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.results-summary {
  display: flex;
  gap: var(--spacing-lg);
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-md);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
}

.summary-item.success {
  border-color: var(--color-success);
  background: var(--color-success-soft);
}

.summary-item.error {
  border-color: var(--color-error);
  background: var(--color-error-soft);
}

.summary-count {
  font-size: 1.5rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
}

.summary-item.success .summary-count {
  color: var(--color-success);
}

.summary-item.error .summary-count {
  color: var(--color-error);
}

.summary-label {
  color: var(--color-text-muted);
  font-size: 0.8rem;
}

.results-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  margin-top: var(--spacing-lg);
}

.status-panel {
  margin-top: var(--spacing-xl);
  display: flex;
  justify-content: center;
}

.status-indicator {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius-full);
  background: var(--color-bg-subtle);
  border: 2px solid var(--color-border);
  transition: all var(--transition-normal);
}

.status-indicator.running {
  border-color: var(--color-warning);
  background: var(--color-warning-soft);
}

.status-indicator.success {
  border-color: var(--color-success);
  background: var(--color-success-soft);
}

.status-indicator.warning {
  border-color: var(--color-warning);
  background: var(--color-warning-soft);
}

.status-icon {
  font-size: 1.2rem;
}

.status-text {
  color: var(--color-text);
  font-weight: var(--font-weight-medium);
}

/* Адаптивность */
@media (max-width: 768px) {
  .file-upload-container {
    padding: var(--spacing-md);
  }
  
  .upload-zone {
    padding: var(--spacing-xl);
  }
  
  .file-info {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }
  
  .file-details {
    text-align: center;
  }
  
  .tests-header {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }
  
  .results-header {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }
  
  .results-summary {
    justify-content: center;
  }
  
  .results-actions {
    flex-direction: column;
  }
  
  .test-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }
}

@media (max-width: 480px) {
  .upload-zone {
    padding: var(--spacing-lg);
    min-height: 150px;
  }
  
  .upload-icon {
    font-size: 2rem;
  }
  
  .results-summary {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .summary-item {
    flex-direction: row;
    justify-content: space-between;
  }
}
</style>