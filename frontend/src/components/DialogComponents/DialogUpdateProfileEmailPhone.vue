<template>
  <div class="data-add-container">
    <div class="data-add-card">
      <div class="card-header">
        <h1 class="cyber-heading">Добавление данных</h1>
        <p class="futurism-elegant">Выберите тип данных для добавления</p>
      </div>

      <div class="selection-section">
        <h3 class="section-title cyber-dynamic">Выберите тип данных:</h3>
        <div class="checkbox-group">
          <label class="checkbox-label" :class="{ active: selectedTypes.phone }">
            <input
              type="checkbox"
              v-model="selectedTypes.phone"
              @change="handleTypeChange"
              class="checkbox-input"
            />
            <span class="custom-checkbox"></span>
            <span class="checkbox-text">Телефон</span>
          </label>

          <label class="checkbox-label" :class="{ active: selectedTypes.email }">
            <input
              type="checkbox"
              v-model="selectedTypes.email"
              @change="handleTypeChange"
              class="checkbox-input"
            />
            <span class="custom-checkbox"></span>
            <span class="checkbox-text">Email</span>
          </label>
        </div>
      </div>

      <div class="inputs-section">
        <transition-group name="slide-fade">
          <div v-if="selectedTypes.phone" key="phone" class="input-group">
            <label for="phone" class="form-label cyber-dynamic"> Номер телефона </label>
            <div class="input-container">
              <input
                v-model="form.phone"
                type="tel"
                id="phone"
                class="data-input"
                placeholder="+7 (999) 999-99-99"
                :class="{ error: errors.phone }"
                @input="validatePhone"
              />
              <div class="input-icon">
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M22 16.92V19.92C22 20.52 21.53 20.99 20.96 21.02C20.41 21.05 19.42 21 18 21C9 21 3 15 3 6C3 4.59 2.95 3.59 2.98 3.04C3.01 2.47 3.48 2 4.08 2H7.08C7.58 2 8 2.45 8 2.95C8 3.46 8.05 4.41 8.14 4.86C8.24 5.31 8.71 5.64 9.18 5.54C10.14 5.34 11.32 5.2 12 5.2C12.68 5.2 13.86 5.34 14.82 5.54C15.29 5.64 15.76 5.31 15.86 4.86C15.95 4.41 16 3.46 16 2.95C16 2.45 16.42 2 16.92 2H19.92C20.52 2 21 2.48 21 3.08C21 5.7 21 14.3 22 16.92Z"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>
            </div>
            <div v-if="errors.phone" class="error-message">
              {{ errors.phone }}
            </div>
          </div>

          <div v-if="selectedTypes.email" key="email" class="input-group">
            <label for="email" class="form-label cyber-dynamic"> Email адрес </label>
            <div class="input-container">
              <input
                v-model="form.email"
                type="email"
                id="email"
                class="data-input"
                placeholder="example@domain.com"
                :class="{ error: errors.email }"
                @input="validateEmail"
              />
              <div class="input-icon">
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M4 4H20C21.1 4 22 4.9 22 6V18C22 19.1 21.1 20 20 20H4C2.9 20 2 19.1 2 18V6C2 4.9 2.9 4 4 4Z"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                  <path
                    d="M22 6L12 13L2 6"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>
            </div>
            <div v-if="errors.email" class="error-message">
              {{ errors.email }}
            </div>
          </div>
        </transition-group>
      </div>

      <button
        type="button"
        class="submit-button cyber-heading"
        :disabled="!isFormValid"
        :class="{ disabled: !isFormValid }"
        @click="handleSubmit"
      >
        <span v-if="loading" class="button-loading">
          <div class="spinner"></div>
          Добавление...
        </span>
        <span v-else>Добавить данные</span>
      </button>

      <div v-if="message" class="message" :class="messageType">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'

// Emits
const emit = defineEmits(['dataAdded'])

// Reactive state
const selectedTypes = reactive({
  phone: false,
  email: false,
})

const form = reactive({
  phone: '',
  email: '',
})

const errors = reactive({
  phone: '',
  email: '',
})

const loading = ref(false)
const message = ref('')
const messageType = ref('')

// Computed properties
const isFormValid = computed(() => {
  const hasSelectedType = selectedTypes.phone || selectedTypes.email
  const phoneValid = !selectedTypes.phone || (form.phone && !errors.phone)
  const emailValid = !selectedTypes.email || (form.email && !errors.email)

  return hasSelectedType && phoneValid && emailValid && !loading.value
})

const hasActiveInputs = computed(() => {
  return selectedTypes.phone || selectedTypes.email
})

// Methods
const handleTypeChange = () => {
  // Сбрасываем ошибки при изменении выбора
  if (!selectedTypes.phone) {
    form.phone = ''
    errors.phone = ''
  }
  if (!selectedTypes.email) {
    form.email = ''
    errors.email = ''
  }
}

const validatePhone = () => {
  const phone = form.phone.trim()

  if (!phone) {
    errors.phone = 'Введите номер телефона'
    return
  }

  // Простая валидация российского номера
  const phoneRegex =
    /^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$/

  if (!phoneRegex.test(phone.replace(/\s/g, ''))) {
    errors.phone = 'Введите корректный номер телефона'
  } else {
    errors.phone = ''
  }
}

const validateEmail = () => {
  const email = form.email.trim()

  if (!email) {
    errors.email = 'Введите email адрес'
    return
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!emailRegex.test(email)) {
    errors.email = 'Введите корректный email адрес'
  } else {
    errors.email = ''
  }
}

const formatFormData = () => {
  const data = {}

  if (selectedTypes.phone && form.phone) {
    data.phone = form.phone
  }

  if (selectedTypes.email && form.email) {
    data.email = form.email
  }

  return data
}

const handleSubmit = async () => {
  if (!isFormValid.value) return

  loading.value = true
  message.value = ''

  try {
    // Имитация API запроса
    await new Promise((resolve) => setTimeout(resolve, 1500))

    const formData = formatFormData()

    // Эмитим событие с данными
    emit('dataAdded', formData)

    // Сброс формы
    resetForm()

    showMessage('Данные успешно добавлены!', 'success')
  } catch (error) {
    console.error('Ошибка при добавлении данных:', error)
    showMessage('Произошла ошибка при добавлении данных', 'error')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  form.phone = ''
  form.email = ''
  errors.phone = ''
  errors.email = ''
  selectedTypes.phone = false
  selectedTypes.email = false
}


// Watchers
watch(
  () => form.phone,
  () => {
    if (selectedTypes.phone) {
      validatePhone()
    }
  },
)

watch(
  () => form.email,
  () => {
    if (selectedTypes.email) {
      validateEmail()
    }
  },
)
</script>

<style scoped>
.data-add-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  padding: var(--spacing-xl);
  background: var(--gradient-subtle);
}

.data-add-card {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-xl);
  padding: var(--spacing-2xl);
  width: 100%;
  max-width: 500px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--color-border);
  position: relative;
  overflow: hidden;
}

.data-add-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-primary);
}

.card-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.card-header h1 {
  font-size: clamp(1.75rem, 4vw, 2.25rem);
  margin-bottom: var(--spacing-sm);
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.card-header p {
  color: var(--color-text-muted);
  font-size: 1.1rem;
}

.selection-section {
  margin-bottom: var(--spacing-2xl);
}

.section-title {
  font-size: 1.1rem;
  margin-bottom: var(--spacing-lg);
  color: var(--color-text);
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--color-bg-subtle);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
  position: relative;
}

.checkbox-label:hover {
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
}

.checkbox-label.active {
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.checkbox-input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.custom-checkbox {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-sm);
  background: var(--color-bg-elevated);
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  justify-content: center;
}

.checkbox-label.active .custom-checkbox {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.custom-checkbox::after {
  content: '✓';
  color: var(--color-text-inverted);
  font-size: 12px;
  font-weight: bold;
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.checkbox-label.active .custom-checkbox::after {
  opacity: 1;
}

.checkbox-text {
  font-family: 'Rajdhani', sans-serif;
  font-weight: 500;
  color: var(--color-text);
  font-size: 1rem;
}

.inputs-section {
  margin-bottom: var(--spacing-2xl);
}

.input-group {
  margin-bottom: var(--spacing-xl);
}

.input-group:last-child {
  margin-bottom: 0;
}

.form-label {
  font-weight: 600;
  color: var(--color-text);
  font-size: 1rem;
  margin-bottom: var(--spacing-sm);
  display: block;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.data-input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  padding-left: 3rem;
  background: var(--color-bg-subtle);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  font-family: 'Exo 2', sans-serif;
  font-size: 1rem;
  color: var(--color-text);
  transition: all var(--transition-normal);
  outline: none;
}

.data-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
  background: var(--color-bg-elevated);
}

.data-input.error {
  border-color: var(--color-error);
  box-shadow: 0 0 0 3px var(--color-error-soft);
}

.data-input::placeholder {
  color: var(--color-text-light);
  opacity: 0.7;
}

.input-icon {
  position: absolute;
  left: var(--spacing-md);
  color: var(--color-text-light);
  display: flex;
  align-items: center;
  justify-content: center;
}

.data-input:focus + .input-icon {
  color: var(--color-primary);
}

.data-input.error + .input-icon {
  color: var(--color-error);
}

.error-message {
  color: var(--color-error);
  font-size: 0.85rem;
  margin-top: var(--spacing-xs);
  padding-left: var(--spacing-sm);
}

.submit-button {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-xl);
  background: var(--gradient-primary);
  color: var(--color-text-inverted);
  border: none;
  border-radius: var(--border-radius-lg);
  font-size: 1rem;
  cursor: pointer;
  transition: all var(--transition-normal);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  position: relative;
  overflow: hidden;
}

.submit-button:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.submit-button:active:not(.disabled) {
  transform: translateY(0);
}

.submit-button.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  background: var(--color-border);
}

.button-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.message {
  padding: var(--spacing-md);
  border-radius: var(--border-radius-lg);
  text-align: center;
  font-weight: 500;
  margin-top: var(--spacing-md);
}

.message.success {
  background: var(--color-success-soft);
  color: var(--color-success);
  border: 1px solid var(--color-success);
}

.message.error {
  background: var(--color-error-soft);
  color: var(--color-error);
  border: 1px solid var(--color-error);
}

/* Анимации */
.slide-fade-enter-active {
  transition: all var(--transition-slow) ease-out;
}

.slide-fade-leave-active {
  transition: all var(--transition-normal) ease-in;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Адаптивность */
@media (max-width: 480px) {
  .data-add-container {
    padding: var(--spacing-md);
  }

  .data-add-card {
    padding: var(--spacing-xl);
  }

  .checkbox-group {
    gap: var(--spacing-sm);
  }

  .checkbox-label {
    padding: var(--spacing-sm) var(--spacing-md);
  }
}
</style>
