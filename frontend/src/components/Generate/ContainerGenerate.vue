<template>
  <div class="generator-container">
    <!-- Заголовок -->
    <div class="generator-header">
      
        <span class="text-primary">ГЕНЕРАТОР ПОСЛЕДОВАТЕЛЬНОСТЕЙ</span>
     
    </div>

    <!-- Основной контейнер -->
    <div class="generator-main">
      <!-- Панель управления -->
      <div class="control-panel">
        <!-- Переключатель режима -->
        <div class="mode-switcher">
          <div class="mode-buttons">
            <button
              class="mode-button"
              :class="{ 'active': generationMode === 'web' }"
              @click="generationMode = 'web'"
            >
              <span class="mode-icon">🎯</span>
              <span class="mode-text">Выигрышные числа</span>
            </button>
            <button
              class="mode-button"
              :class="{ 'active': generationMode === 'txt' }"
              @click="generationMode = 'txt'"
            >
              <span class="mode-icon">📄</span>
              <span class="mode-text">Случайная последовательность</span>
            </button>
          </div>
        </div>

        <!-- Параметры для WEB режима -->
        <div class="web-params" v-if="generationMode === 'web'">
          <div class="params-grid">
            <div class="param-group">
              <label class="param-label cyber-mono">
                КОЛИЧЕСТВО ЧИСЕЛ
              </label>
              <input
                v-model="winNumbersCount"
                type="number"
                min="1"
                max="100"
                class="param-input cyber-mono"
              />
            </div>
            <div class="param-group">
              <label class="param-label cyber-mono">
                ДИАПАЗОН ОТ
              </label>
              <input
                v-model="rangeFrom"
                type="number"
                min="1"
                max="1000"
                class="param-input cyber-mono"
                @input="validateRange"
              />
            </div>
            <div class="param-group">
              <label class="param-label cyber-mono">
                ДИАПАЗОН ДО
              </label>
              <input
                v-model="rangeTo"
                type="number"
                min="1"
                max="1000"
                class="param-input cyber-mono"
                @input="validateRange"
              />
            </div>
          </div>
        </div>

        <!-- Параметры для TXT режима -->
        <div class="txt-params" v-if="generationMode === 'txt'">
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
                placeholder="Введите длину"
                class="length-input cyber-mono"
                @input="validateLength"
              />
              <span class="input-suffix">символов</span>
            </div>
            <div class="input-hint futurism-elegant">
              Введите число от 1 до 10 000
            </div>
          </div>
        </div>

        <!-- Кнопки генерации -->
        <div class="generation-buttons">
          <button
            class="cyber-button generate-button"
            @click="generateSequence"
            :disabled="!isValidParams || isGenerating"
            :class="{ 'disabled': !isValidParams || isGenerating }"
          >
            <span class="button-icon">{{ generationMode === 'web' ? '🎯' : '📄' }}</span>
            <span class="button-text">
              {{ generationMode === 'web' ? 'СГЕНЕРИРОВАТЬ ЧИСЛА' : 'СГЕНЕРИРОВАТЬ ФАЙЛ' }}
            </span>
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
              <span class="text-primary">ВЫИГРЫШНЫЕ ЧИСЛА</span>
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
            <button class="cyber-button primary" @click="generateSequence">
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
import { ref, computed, inject, provide } from 'vue'
import { useApiMutations } from '@/utils/api/useApiMutation'
import { api8000, api8001 } from '@/utils/apiUrl/urlApi'
import axios from 'axios'
const {usePost} = useApiMutations()
// Refs
const generationMode = ref('web') // 'web' или 'txt'
const sequenceLength = ref('')
const isGenerating = ref(false)
const generatedSequence = ref('')
const downloadedFile = ref(null)
const copySuccess = ref(false)
const generationStatus = ref('')

// Настройки для выигрышных чисел (WEB)
const winNumbersCount = ref(6) // Количество выигрышных чисел
const rangeFrom = ref(1) // Диапазон от
const rangeTo = ref(49) // Диапазон до

// Инъекция функций управления тестами из главного компонента
const { 
  startTests, 
  updateTestProgress, 
  completeTest, 
  completeAllTests,
  setTestResults // ДОБАВЛЯЕМ ЭТУ ФУНКЦИЮ
} = inject('testControls')

// Вычисляемые свойства
const isValidParams = computed(() => {
  if (generationMode.value === 'web') {
    return winNumbersCount.value > 0 && 
           rangeFrom.value > 0 && 
           rangeTo.value > 0 &&
           rangeFrom.value <= rangeTo.value &&
           winNumbersCount.value <= (rangeTo.value - rangeFrom.value + 1)
  } else {
    const length = parseInt(sequenceLength.value)
    return length > 0 && length <= 10000
  }
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

const validateRange = () => {
  // Гарантируем, что "от" не больше "до"
  if (parseInt(rangeFrom.value) > parseInt(rangeTo.value)) {
    rangeTo.value = rangeFrom.value
  }
  
  // Ограничиваем максимальные значения
  if (rangeFrom.value > 1000) rangeFrom.value = 1000
  if (rangeTo.value > 1000) rangeTo.value = 1000
  if (rangeFrom.value < 1) rangeFrom.value = 1
  if (rangeTo.value < 1) rangeTo.value = 1
}

// Генерация выигрышных чисел (для WEB)
const generateWinNumbers = (count, from, to) => {
  const numbers = []
  const rangeSize = to - from + 1
  const availableNumbers = Array.from({ length: rangeSize }, (_, i) => i + from)
  
  for (let i = 0; i < count; i++) {
    if (availableNumbers.length === 0) break
    
    const randomIndex = Math.floor(Math.random() * availableNumbers.length)
    const selectedNumber = availableNumbers.splice(randomIndex, 1)[0]
    numbers.push(selectedNumber)
  }
  
  // Сортируем числа по возрастанию
  numbers.sort((a, b) => a - b)
  
  return numbers.join(' | ')
}

// Генерация случайной последовательности (для TXT)
const generateRandomSequence = (length) => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

const generateSequence = async () => {
  if (!isValidParams.value) return
  
  isGenerating.value = true
  
  if (generationMode.value === 'web') {
    await generateWeb()
  } else {
    await generateTxt()
  }
}
const forgotMutation = usePost(`${api8000}/auth/forgot-password`, {
  onSuccess: (data) => {
    console.log('✅ Восстановление:', data)
    // Успешная отправка
    isSuccess.value = true
    startCooldown()
    notifications.success('Ссылка для восстановления отправлена на вашу почту', 'Проверьте email')
  },
  onError: (error) => {
    console.error('❌ Ошибка восстановления пароля:', error)
    notifications.error('Произошла ошибка при отправке ссылки', 'Попробуйте еще раз')
  },
})
const generateWeb = async () => {
  generationStatus.value = 'Генерация выигрышных чисел...'
  
  try {
    // Отправляем запрос на сервер с параметрами
    const response = await axios.post(`${api8001}/generate/generate-winners`, {
      count_of_winning_numbers: winNumbersCount.value,
      max_number: rangeTo.value
    })
    
    console.log('🎯 Ответ сервера для выигрышных чисел:', response.data)
    
    // Получаем данные из ответа сервера
    const responseData = response.data
    
    // Извлекаем сгенерированные числа из ответа
    let winNumbers = ''
    
    if (typeof responseData === 'object' && responseData !== null) {
      // Если сервер возвращает объект с winning_tickets
      if (responseData.winning_tickets) {
        // Преобразуем строку "3,11,38" в форматированную строку "3 | 11 | 38"
        winNumbers = responseData.winning_tickets
          .split(',')
          .map(num => num.trim())
          .join(' | ')
      } 
      // Если сервер возвращает массив numbers
      else if (responseData.numbers && Array.isArray(responseData.numbers)) {
        winNumbers = responseData.numbers.join(' | ')
      } 
      // Если сервер возвращает последовательность
      else if (responseData.sequence) {
        winNumbers = responseData.sequence
      } else {
        // Если структура ответа неизвестна, генерируем локально
        console.warn('⚠️ Неизвестная структура ответа сервера, генерируем локально')
        winNumbers = generateWinNumbers(winNumbersCount.value, rangeFrom.value, rangeTo.value)
      }
    } else if (typeof responseData === 'string') {
      // Если сервер возвращает строку
      winNumbers = responseData
    } else {
      // Fallback на локальную генерацию
      console.warn('⚠️ Неподдерживаемый формат ответа, генерируем локально')
      winNumbers = generateWinNumbers(winNumbersCount.value, rangeFrom.value, rangeTo.value)
    }
    
    generatedSequence.value = winNumbers
    downloadedFile.value = null
    generationStatus.value = 'Выигрышные числа сгенерированы'
    
    // Если сервер возвращает ID последовательности, можно отправить на тестирование
    if (responseData.id || responseData.sequence_id) {
      const sequenceId = responseData.id || responseData.sequence_id
      console.log('🆔 ID последовательности для тестов:', sequenceId)
      
      // Создаем бинарную последовательность для тестов из выигрышных чисел
      let binarySequence = ''
      if (responseData.winning_tickets) {
        // Преобразуем выигрышные числа в бинарную последовательность
        const numbers = responseData.winning_tickets.split(',').map(num => parseInt(num.trim()))
        binarySequence = numbers.map(num => num.toString(2)).join('')
      } else {
        // Fallback - используем числа как есть
        binarySequence = winNumbers.replace(/\s*\|\s*/g, '')
      }
      
      // Отправляем на тестирование, если нужно
      try {
        const testResponse = await axios.post(`${api8000}/statistics/sequence`, {
          sequence_id: responseData.id || responseData.sequence_id,
          sequence: binarySequence
        })
        
        console.log('📊 Результаты тестов для выигрышных чисел:', testResponse.data.tests_results)
        
        // Передаем результаты тестов в родительский компонент
        if (setTestResults && testResponse.data.tests_results) {
          setTestResults(testResponse.data.tests_results)
        }
        
        // Запускаем тесты с полученными результатами
        await runTests(testResponse.data.tests_results)
        
      } catch (testError) {
        console.warn('⚠️ Не удалось получить результаты тестов:', testError)
        // Продолжаем без тестов
        generationStatus.value = 'Числа сгенерированы (тесты недоступны)'
      }
    } else {
      // Если нет ID, просто показываем числа без тестов
      console.log('ℹ️ ID последовательности не получен, тесты не запускаются')
      generationStatus.value = 'Выигрышные числа сгенерированы'
    }
    
  } catch (error) {
    console.error('❌ Ошибка генерации выигрышных чисел:', error)
    
    // Fallback на локальную генерацию при ошибке
    try {
      console.log('🔄 Используем локальную генерацию...')
      const winNumbers = generateWinNumbers(winNumbersCount.value, rangeFrom.value, rangeTo.value)
      generatedSequence.value = winNumbers
      downloadedFile.value = null
      generationStatus.value = 'Числа сгенерированы локально (сервер недоступен)'
    } catch (fallbackError) {
      console.error('❌ Ошибка локальной генерации:', fallbackError)
      generationStatus.value = 'Ошибка генерации'
    }
  } finally {
    isGenerating.value = false
  }
}

const generateTxt = async () => {
  generationStatus.value = 'Генерация и скачивание файла...'
  
  try {
    // Имитация запроса к бэкенду для TXT генерации
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Генерация случайной последовательности
    const length = parseInt(sequenceLength.value)
    console.log(sequenceLength.value,'ДЛИНА')
    const response = await axios.post(`${api8001}/generate/generate-file`, {length:sequenceLength.value})
    console.log(response.data,'RESPONSE')
    
    // Получаем данные из ответа сервера
    const responseData = response.data
    
    // Ищем поля Sequence и ID в ответе
    let sequence = ''
    let sequenceId = ''
    
    // Если responseData - это объект, ищем поля Sequence и ID
    if (typeof responseData === 'object' && responseData !== null) {
      sequence = responseData.Sequence || ''
      sequenceId = responseData.ID || responseData.id || responseData.uuid || ''
      console.log('📊 ID из объекта:', sequenceId)
      console.log('📊 Sequence из объекта:', sequence)
    } 
    // Если responseData - это строка (текст файла), ищем в тексте
    else if (typeof responseData === 'string') {
      console.log('📄 Ответ в виде текста, ищем Sequence и ID...')
      
      // Пытаемся найти строку с ID в тексте
      const idMatch = responseData.match(/ID:\s*([a-fA-F0-9-]+)/)
      if (idMatch) {
        sequenceId = idMatch[1]
        console.log('✅ ID найден в тексте:', sequenceId)
      }
      
      // Пытаемся найти строку с Sequence в тексте
      const sequenceMatch = responseData.match(/Sequence:\s*([01]+)/)
      if (sequenceMatch) {
        sequence = sequenceMatch[1]
        console.log('✅ Sequence найден в тексте:', sequence)
      } else {
        // Если не нашли по шаблону, возможно весь текст и есть последовательность
        sequence = responseData.trim()
        console.log('ℹ️ Sequence не найден, используем весь текст:', sequence)
      }
    }
    
    // Если sequence пустой, используем fallback
    if (!sequence) {
      console.warn('⚠️ Sequence не найден, генерируем локально')
      sequence = generateRandomSequence(length)
    }
    
    console.log('🎯 Финальная последовательность для тестов:', sequence)
    console.log('🆔 ID последовательности:', sequenceId)
    
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
    
    // Отправляем ID и sequence на сервер для получения результатов тестов
    const responseID = await axios.post(`${api8000}/statistics/sequence`, {
      sequence_id: sequenceId,
      sequence: sequence
    })
    
    console.log('📊 Результаты тестов с сервера:', responseID.data.tests_results)
    
    // ПЕРЕДАЕМ РЕЗУЛЬТАТЫ ТЕСТОВ В РОДИТЕЛЬСКИЙ КОМПОНЕНТ ЧЕРЕЗ INJECT
    if (setTestResults && responseID.data.tests_results) {
      setTestResults(responseID.data.tests_results)
    }
    
    // Запускаем тесты с полученными результатами
    await runTests(responseID.data.tests_results)
    
  } catch (error) {
    console.error('Ошибка генерации:', error)
    generationStatus.value = 'Ошибка генерации файла'
  } finally {
    isGenerating.value = false
  }
}

// ПЕРЕДЕЛАННАЯ ФУНКЦИЯ runTests по аналогии с runFileTests
const runTests = async (testsResults) => {
  // Запускаем тесты через инъекцию из главного компонента
  startTests()
  
  console.log('📊 Получены данные тестов с сервера:', testsResults)
  
  // Список тестов с русскими названиями и задержками
  const tests = [
    { key: 'frequency', name: 'Частотный тест', delay: 80 },
    { key: 'runs', name: 'Тест серий', delay: 90 },
    { key: 'poker', name: 'Покер-тест', delay: 70 },
    { key: 'serial', name: 'Последовательный тест', delay: 85 },
    { key: 'longest_runs', name: 'Тест самых длинных серий', delay: 75 },
    { key: 'cumulative_sums', name: 'Тест кумулятивных сумм', delay: 80 },
    { key: 'autocorrelation', name: 'Тест автокорреляции', delay: 90 },
    { key: 'matrix_rank', name: 'Тест ранга матрицы', delay: 70 }
  ]
  
  // Запускаем каждый тест
  for (let i = 0; i < tests.length; i++) {
    const { key, name, delay } = tests[i]
    const testData = testsResults?.[key]
    
    // Прогресс для текущего теста
    for (let j = 0; j <= 100; j += 10) {
      await new Promise(resolve => setTimeout(resolve, delay / 10))
      updateTestProgress(i + 1, j)
    }
    
    // Формируем сообщение на основе данных теста
    let message = name
    let success = false
    
    if (testData) {
      message += `: ${testData.result}`
      if (testData.p_value !== null && testData.p_value !== undefined) {
        message += ` (p-value: ${testData.p_value})`
      }
      
      // Определяем успешность теста
      success = testData.result === 'PASS' || testData.result === 'SKIP'
    } else {
      message += ': Данные недоступны'
    }
    
    completeTest(i + 1, message, success)
  }
  
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
  max-width: 100%;
  overflow: hidden;
}

.generator-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  border-bottom: 2px solid var(--color-border);
  padding-bottom: var(--spacing-lg);
}

.main-title {
  font-size: clamp(1.4rem, 4vw, 1.8rem);
  margin-bottom: var(--spacing-sm);
  word-break: break-word;
}

.generator-main {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
  width: 100%;
}

.control-panel {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  width: 100%;
  box-sizing: border-box;
}

/* Переключатель режимов */
.mode-switcher {
  margin-bottom: var(--spacing-lg);
}

.mode-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-sm);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-sm);
  background: var(--color-bg-subtle);
  width: 100%;
}

.mode-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm);
  border: none;
  border-radius: var(--border-radius-sm);
  background: transparent;
  color: var(--color-text);
  transition: all var(--transition-normal);
  cursor: pointer;
  box-sizing: border-box;
  min-height: 60px;
  width: 100%;
}

.mode-button.active {
  background: var(--color-primary);
  color: var(--color-text-inverted);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.mode-button:hover:not(.active) {
  background: var(--color-bg-elevated);
}

.mode-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.mode-text {
  font-size: clamp(0.7rem, 2vw, 0.8rem);
  font-weight: var(--font-weight-medium);
  text-align: center;
  line-height: 1.2;
  word-break: break-word;
  overflow-wrap: break-word;
}

/* Параметры для WEB режима */
.web-params {
  margin-bottom: var(--spacing-lg);
}

.params-grid {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  width: 100%;
}

.param-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  width: 100%;
}

.param-label {
  font-size: clamp(0.7rem, 2vw, 0.8rem);
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  word-break: break-word;
}

.param-input {
  padding: var(--spacing-sm);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-md);
  background: var(--color-bg-subtle);
  color: var(--color-text);
  font-family: var(--font-mono);
  transition: all var(--transition-normal);
  box-sizing: border-box;
  width: 100%;
  font-size: clamp(0.8rem, 2vw, 0.9rem);
}

.param-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

/* Параметры для TXT режима */
.txt-params {
  margin-bottom: var(--spacing-lg);
}

.input-section {
  margin-bottom: 0;
  width: 100%;
}

.input-label {
  display: block;
  margin-bottom: var(--spacing-sm);
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  text-transform: uppercase;
  word-break: break-word;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.length-input {
  flex: 1;
  padding: var(--spacing-md);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-md);
  background: var(--color-bg-subtle);
  color: var(--color-text);
  font-size: clamp(0.9rem, 2vw, 1rem);
  font-family: var(--font-mono);
  transition: all var(--transition-normal);
  box-sizing: border-box;
  width: 100%;
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
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  pointer-events: none;
  white-space: nowrap;
}

.input-hint {
  margin-top: var(--spacing-xs);
  color: var(--color-text-light);
  font-size: clamp(0.7rem, 2vw, 0.8rem);
  word-break: break-word;
}

/* Кнопка генерации */
.generation-buttons {
  margin-bottom: var(--spacing-lg);
  display: flex;
  justify-content: center;
  width: 100%;
}

.generate-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  border: 2px solid var(--color-primary);
  border-radius: var(--border-radius-lg);
  background: var(--color-primary);
  color: var(--color-text-inverted);
  font-weight: var(--font-weight-bold);
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  transition: all var(--transition-normal);
  width: 100%;
  max-width: 300px;
  box-sizing: border-box;
  flex-wrap: wrap;
}

.generate-button:hover:not(.disabled) {
  background: var(--color-primary-dark);
  border-color: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(var(--color-primary-rgb), 0.3);
}

.generate-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.button-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.button-text {
  text-align: center;
  line-height: 1.2;
  word-break: break-word;
  overflow-wrap: break-word;
}

/* Статус генерации */
.generation-status {
  display: flex;
  justify-content: center;
  width: 100%;
}

.status-indicator {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius-full);
  background: var(--color-bg-subtle);
  border: 2px solid var(--color-border);
  transition: all var(--transition-normal);
  box-sizing: border-box;
  max-width: 100%;
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
  flex-shrink: 0;
}

.status-text {
  color: var(--color-text);
  font-weight: var(--font-weight-medium);
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  word-break: break-word;
}

/* Результаты генерации */
.generation-results {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  box-sizing: border-box;
  width: 100%;
}

.result-header {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--spacing-md);
  width: 100%;
}

.copy-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  font-size: clamp(0.7rem, 2vw, 0.8rem);
  border-radius: var(--border-radius-md);
  min-width: auto;
  width: 100%;
  max-width: 140px;
  box-sizing: border-box;
  white-space: nowrap;
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
  box-sizing: border-box;
  width: 100%;
}

.sequence-text {
  margin: 0;
  color: var(--color-text);
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  line-height: 1.4;
  word-break: break-all;
  white-space: pre-wrap;
  text-align: center;
  font-weight: var(--font-weight-bold);
  overflow-wrap: break-word;
}

.sequence-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-md);
  padding: var(--spacing-sm);
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-border);
  box-sizing: border-box;
  width: 100%;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  width: 100%;
}

.info-label {
  font-size: clamp(0.65rem, 2vw, 0.7rem);
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  text-transform: uppercase;
  word-break: break-word;
}

.info-value {
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
  font-family: var(--font-mono);
  word-break: break-word;
}

.file-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  text-align: center;
  width: 100%;
}

.file-icon {
  font-size: 2rem;
}

.file-details {
  text-align: center;
  width: 100%;
}

.file-name {
  color: var(--color-text);
  margin: 0 0 var(--spacing-xs) 0;
  font-size: clamp(0.9rem, 2vw, 1rem);
  word-break: break-word;
}

.file-size {
  color: var(--color-text-muted);
  margin: 0;
  font-size: clamp(0.7rem, 2vw, 0.8rem);
}

.download-actions {
  display: flex;
  justify-content: center;
  margin-top: var(--spacing-md);
  width: 100%;
}

/* Основные кнопки в результатах */
.primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  background: var(--color-primary);
  border: 2px solid var(--color-primary);
  color: var(--color-text-inverted);
  font-size: clamp(0.7rem, 2vw, 0.8rem);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius-md);
  width: 100%;
  max-width: 200px;
  box-sizing: border-box;
}

.primary:hover {
  background: var(--color-primary-dark);
  border-color: var(--color-primary-dark);
}

/* Адаптивность */
@media (max-width: 768px) {
  .mode-buttons {
    grid-template-columns: 1fr;
    gap: var(--spacing-xs);
  }
  
  .params-grid {
    gap: var(--spacing-sm);
  }
  
  .result-header {
    flex-direction: column;
    gap: var(--spacing-sm);
    align-items: center;
    text-align: center;
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
  
  .generate-button {
    max-width: 100%;
    padding: var(--spacing-sm);
    font-size: 0.8rem;
  }
  
  .mode-button {
    padding: var(--spacing-xs);
    min-height: 50px;
  }
  
  .control-panel {
    padding: var(--spacing-md);
  }
}

@media (max-width: 480px) {
  .control-panel {
    padding: var(--spacing-sm);
  }
  
  .generate-button {
    padding: var(--spacing-sm);
    font-size: 0.75rem;
    gap: var(--spacing-xs);
  }
  
  .button-icon {
    font-size: 1rem;
  }
  
  .mode-button {
    padding: var(--spacing-xs);
    min-height: 45px;
  }
  
  .mode-icon {
    font-size: 1rem;
  }
  
  .mode-text {
    font-size: 0.7rem;
  }
  
  .params-grid {
    gap: var(--spacing-sm);
  }
  
  .param-input,
  .length-input {
    padding: var(--spacing-sm);
    font-size: 0.8rem;
  }
  
  .generation-results {
    padding: var(--spacing-md);
  }
}

/* Дополнительные исправления для очень маленьких экранов */
@media (max-width: 360px) {
  .mode-text {
    font-size: 0.65rem;
  }
  
  .generate-button .button-text {
    font-size: 0.7rem;
  }
  
  .param-label,
  .input-label {
    font-size: 0.7rem;
  }
}
</style>