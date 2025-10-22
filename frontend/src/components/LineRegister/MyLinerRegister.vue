<template>
  <div class="lfsr-container">
    <!-- Заголовок -->
    <div class="lfsr-header">
      <h2 class="cyber-heading">
        <span class="text-indigo-theme">16-БИТНЫЙ LFSR</span>
      </h2>
      <p class="lfsr-subtitle futurism-elegant">
        Линейный Регистр Сдвига с Обратной Связью
      </p>
    </div>

    <!-- Основной контейнер -->
    <div class="lfsr-main">
      <!-- Панель управления -->
      <div class="control-panel">
        <div class="control-group">
          <label class="control-label cyber-mono">КОНФИГУРАЦИЯ ОБРАТНЫХ СВЯЗЕЙ</label>
          <select 
            id="tapPreset" 
            v-model="selectedPreset" 
            :disabled="isRunning"
            class="cyber-select"
          >
            <option v-for="preset in tapPresets" :key="preset.id" :value="preset.id">
              {{ preset.label }} (тапы: {{ preset.taps.join(', ') }})
            </option>
          </select>
        </div>

        <div class="control-buttons">
          <button 
            class="cyber-button primary"
            @click="start" 
            :disabled="isRunning"
          >
            <span class="button-icon">▶</span>
            ЗАПУСТИТЬ
          </button>
          <button 
            class="cyber-button secondary"
            @click="step" 
            :disabled="isRunning"
          >
            <span class="button-icon">⏭</span>
            ШАГ
          </button>
          <button 
            class="cyber-button accent"
            @click="reset"
          >
            <span class="button-icon">↺</span>
            СБРОС
          </button>
          <button 
            class="cyber-button warning"
            @click="stop" 
            v-if="isRunning"
          >
            <span class="button-icon">⏹</span>
            СТОП
          </button>
        </div>
      </div>

      <!-- Визуализация регистра -->
      <div class="register-visualization">
        <div class="register-container">
          <div
            v-for="(bit, index) in bitsReversed"
            :key="index"
            class="register-bit"
            :class="{
              'bit-1': bit === 1,
              'bit-0': bit === 0,
              'active-tap': activeTaps.includes(15 - index),
              'new-bit': index === 0 && justUpdated
            }"
            :title="`Бит ${15 - index}${activeTaps.includes(15 - index) ? ' — тап' : ''}`"
          >
            <div class="bit-value cyber-mono">{{ bit }}</div>
            <div class="bit-index cyber-mono">{{ 15 - index }}</div>
            <div 
              v-if="activeTaps.includes(15 - index)"
              class="tap-connector"
            ></div>
          </div>
        </div>

        <!-- Информация о состоянии -->
        <div class="state-info">
          <div class="state-item">
            <span class="state-label cyber-mono">СОСТОЯНИЕ:</span>
            <span class="state-value cyber-mono">{{ stateToBinary }}</span>
          </div>
          <div class="state-item">
            <span class="state-label cyber-mono">HEX:</span>
            <span class="state-value cyber-mono">{{ stateToHex }}</span>
          </div>
        </div>
      </div>

      <!-- Статус -->
      <div class="status-section">
        <div class="status-indicator" :class="{ 'active': isRunning }">
          <span class="status-icon">{{ isRunning ? '⚡' : '⏸' }}</span>
          <span class="status-text cyber-mono">
            {{ isRunning ? 'АВТОМАТИЧЕСКИЙ РЕЖИМ' : 'РЕЖИМ ОЖИДАНИЯ' }}
          </span>
        </div>
        <p class="status-note futurism-elegant" v-if="isRunning">
          Обновление каждые 500 мс
        </p>
      </div>
    </div>

    <!-- Информационная панель -->
    <div class="info-panel">
      <div class="info-item">
        <h4 class="info-title cyber-heading">ПРИНЦИП РАБОТЫ LFSR</h4>
        <p class="info-text futurism-elegant">
          16-битный линейный регистр сдвига генерирует псевдослучайную последовательность 
          через XOR выбранных битов (тапов). Максимальный период: 65535 тактов.
        </p>
      </div>
      <div class="info-item">
        <h4 class="info-title cyber-heading">КОНФИГУРАЦИИ</h4>
        <div class="config-list">
          <div 
            v-for="preset in tapPresets" 
            :key="preset.id"
            class="config-item"
            :class="{ 'active': selectedPreset === preset.id }"
          >
            <span class="config-label cyber-mono">{{ preset.label }}</span>
            <span class="config-taps cyber-mono">Тапы: {{ preset.taps.join(', ') }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, defineProps } from 'vue'

const props = defineProps({
  chislo: Number,
  startSdvig: Boolean
})



// Предопределённые корректные тапы для 16-битного LFSR (максимальная длина = 65535)
const tapPresets = [
  { id: 'preset1', label: 'Минимум (2 тапа)', taps: [16, 14] },       // x^16 + x^14 + 1
  { id: 'preset2', label: 'Стандартный (3 тапа)', taps: [16, 15, 13, 4] }, // часто используемый
  { id: 'preset3', label: 'Максимальная длина (4 тапа)', taps: [16, 14, 13, 11] }, // primitive polynomial
]

const selectedPreset = ref('preset2')
const state = ref(props.chislo) // Ненулевое начальное состояние (часто используется)
const isRunning = ref(false)
const justUpdated = ref(false)

// Watch для отслеживания изменения startSdvig
watch(() => props.startSdvig, (newValue) => {
  if (newValue) {
    console.log('startSdvig стал true, запускаем LFSR')
    isRunning.value = true
    start()
  }
})

// Получаем активные тапы (в индексах битов от 0 до 15)
const activeTaps = computed(() => {
  const preset = tapPresets.find(p => p.id === selectedPreset.value)
  if (!preset) return []
  // Тапы заданы как номера битов от 1 до 16 → преобразуем в 0–15
  return preset.taps.map(t => t - 1).filter(bit => bit >= 0 && bit < 16)
})

// Биты регистра (младший бит — справа, но для визуализации будем показывать слева → старший)
const bits = computed(() => {
  return Array.from({ length: 16 }, (_, i) => (state.value >> (15 - i)) & 1)
})

// Для визуализации: показываем слева → старший бит (бит 15), справа — младший (бит 0)
// Но при сдвиге вправо: младший уходит, новый входит в старший
const bitsReversed = computed(() => {
  return bits.value
})

// Вспомогательные представления
const stateToBinary = computed(() =>
  state.value.toString(2).padStart(16, '0')
)
const stateToHex = computed(() =>
  '0x' + state.value.toString(16).toUpperCase().padStart(4, '0')
)

// Вычисление нового бита (XOR выбранных тапов)
function computeFeedback() {
  let feedback = 0
  for (const tap of activeTaps.value) {
    feedback ^= (state.value >> tap) & 1
  }
  return feedback
}

// Один шаг LFSR
function lfsrStep() {
  const newBit = computeFeedback()
  // Сдвиг вправо на 1, вставляем newBit в старший разряд (бит 15)
  state.value = ((state.value >> 1) | (newBit << 15)) & 0xFFFF
  justUpdated.value = true
  setTimeout(() => justUpdated.value = false, 300)
}

// Кнопки
function step() {
  lfsrStep()
}

function start() {
  isRunning.value = true
  const interval = setInterval(() => {
    if (!isRunning.value) {
      clearInterval(interval)
      return
    }
    lfsrStep()
  }, 500)
  window.lfsrInterval = interval
}

function stop() {
  isRunning.value = false
  if (window.lfsrInterval) {
    clearInterval(window.lfsrInterval)
    delete window.lfsrInterval
  }
}

function reset() {
  stop()
  state.value = 0xACE1 // или 1, но 0xACE1 — хороший ненулевой seed
}
</script>

<style scoped>
.lfsr-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-xl);
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-lg);
}

.lfsr-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  border-bottom: 2px solid var(--color-border);
  padding-bottom: var(--spacing-lg);
}

.lfsr-subtitle {
  color: var(--color-text-muted);
  font-size: 1.1rem;
  margin-top: var(--spacing-sm);
}

.lfsr-main {
  display: grid;
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-2xl);
}

.control-panel {
  background: var(--color-bg-elevated);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-indigo);
}

.control-group {
  margin-bottom: var(--spacing-lg);
}

.control-label {
  display: block;
  margin-bottom: var(--spacing-sm);
  color: var(--color-text-muted);
  font-size: 0.9rem;
  text-transform: uppercase;
}

.cyber-select {
  width: 100%;
  padding: var(--spacing-md);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-md);
  background: var(--color-bg-subtle);
  color: var(--color-text);
  font-family: 'Rajdhani', sans-serif;
  font-size: 1rem;
  transition: all var(--transition-normal);
}

.cyber-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.cyber-select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.control-buttons {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

.cyber-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border: 2px solid;
  border-radius: var(--border-radius-md);
  font-family: 'Rajdhani', sans-serif;
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  cursor: pointer;
  transition: all var(--transition-normal);
  background: transparent;
}

.cyber-button.primary {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.cyber-button.primary:hover:not(:disabled) {
  background: var(--color-primary);
  color: var(--color-text-inverted);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.cyber-button.secondary {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.cyber-button.secondary:hover:not(:disabled) {
  background: var(--color-accent);
  color: var(--color-text-inverted);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.cyber-button.accent {
  border-color: var(--color-warning);
  color: var(--color-warning);
}

.cyber-button.accent:hover {
  background: var(--color-warning);
  color: var(--color-text-inverted);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.cyber-button.warning {
  border-color: var(--color-error);
  color: var(--color-error);
}

.cyber-button.warning:hover {
  background: var(--color-error);
  color: var(--color-text-inverted);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.cyber-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.button-icon {
  font-size: 1.1rem;
}

.register-visualization {
  background: var(--color-bg-elevated);
  padding: var(--spacing-xl);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-indigo);
}

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-lg);
  flex-wrap: wrap;
}

.register-bit {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  position: relative;
}

.bit-value {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-md);
  font-size: 1rem;
  font-weight: var(--font-weight-bold);
  transition: all var(--transition-normal);
}

.bit-1 .bit-value {
  background: var(--color-primary);
  color: var(--color-text-inverted);
  border-color: var(--color-primary);
  box-shadow: 0 0 8px var(--color-primary);
}

.bit-0 .bit-value {
  background: var(--color-bg-subtle);
  color: var(--color-text);
}

.active-tap .bit-value {
  border-color: var(--color-accent);
  background: var(--color-accent-soft);
}

.new-bit .bit-value {
  animation: pulse 0.6s ease-in-out;
  background: var(--color-success);
  color: var(--color-text-inverted);
  border-color: var(--color-success);
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.bit-index {
  font-size: 0.7rem;
  color: var(--color-text-light);
}

.tap-connector {
  position: absolute;
  top: -15px;
  width: 2px;
  height: 15px;
  background: var(--color-accent);
}

.state-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

.state-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-border);
}

.state-label {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.state-value {
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
  font-size: 1rem;
}

.status-section {
  background: var(--color-bg-elevated);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-indigo);
  text-align: center;
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

.status-indicator.active {
  border-color: var(--color-success);
  background: var(--color-success-soft);
}

.status-icon {
  font-size: 1.2rem;
}

.status-text {
  color: var(--color-text);
  font-weight: var(--font-weight-medium);
}

.status-note {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  margin-top: var(--spacing-sm);
  margin-bottom: 0;
}

.info-panel {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.info-item {
  background: var(--color-bg-elevated);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
}

.info-title {
  color: var(--color-primary);
  font-size: 1rem;
  margin-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--spacing-xs);
}

.info-text {
  color: var(--color-text);
  line-height: 1.6;
  margin: 0;
}

.config-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.config-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
  transition: all var(--transition-normal);
}

.config-item.active {
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
}

.config-label {
  color: var(--color-text);
  font-weight: var(--font-weight-medium);
}

.config-taps {
  color: var(--color-text-muted);
  font-size: 0.8rem;
}

/* Адаптивность */
@media (max-width: 768px) {
  .lfsr-container {
    padding: var(--spacing-md);
  }
  
  .register-container {
    gap: var(--spacing-xs);
  }
  
  .bit-value {
    width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }
  
  .control-buttons {
    flex-direction: column;
  }
  
  .cyber-button {
    justify-content: center;
  }
  
  .state-info {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .bit-value {
    width: 30px;
    height: 30px;
    font-size: 0.8rem;
  }
  
  .config-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }
}
</style>