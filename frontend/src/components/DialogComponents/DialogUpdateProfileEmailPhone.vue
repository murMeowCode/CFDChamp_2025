<template>
  <div class="data-edit-container">
    <div class="data-edit-card">
      <div class="card-header">
        <h1 class="cyber-heading">Редактирование данных</h1>
        <p class="futurism-elegant">Измените ваши персональные данные</p>
      </div>

      <form @submit.prevent="handleSubmit" class="edit-form">
        <div class="form-grid">
          <div class="input-group">
            <label for="first_name" class="form-label cyber-dynamic"> Имя </label>
            <div class="input-container">
              <input
                v-model="form.first_name"
                type="text"
                id="first_name"
                class="data-input"
                placeholder="Введите имя"
                :class="{ error: errors.first_name }"
                @input="validateField('first_name')"
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
                    d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                  <path
                    d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>
            </div>
            <div v-if="errors.first_name" class="error-message">
              {{ errors.first_name }}
            </div>
          </div>

          <div class="input-group">
            <label for="last_name" class="form-label cyber-dynamic"> Фамилия </label>
            <div class="input-container">
              <input
                v-model="form.last_name"
                type="text"
                id="last_name"
                class="data-input"
                placeholder="Введите фамилию"
                :class="{ error: errors.last_name }"
                @input="validateField('last_name')"
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
                    d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                  <path
                    d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>
            </div>
            <div v-if="errors.last_name" class="error-message">
              {{ errors.last_name }}
            </div>
          </div>

          <div class="input-group">
            <label for="middle_name" class="form-label cyber-dynamic"> Отчество </label>
            <div class="input-container">
              <input
                v-model="form.middle_name"
                type="text"
                id="middle_name"
                class="data-input"
                placeholder="Введите отчество"
                :class="{ error: errors.middle_name }"
                @input="validateField('middle_name')"
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
                    d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                  <path
                    d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>
            </div>
            <div v-if="errors.middle_name" class="error-message">
              {{ errors.middle_name }}
            </div>
          </div>

          <div class="input-group">
            <label for="birth_date" class="form-label cyber-dynamic"> Дата рождения </label>
            <div class="input-container">
              <input
                v-model="form.birth_date"
                type="date"
                id="birth_date"
                class="data-input"
                :class="{ error: errors.birth_date }"
                @change="validateField('birth_date')"
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
                    d="M8 7V3M16 7V3M7 11H17M5 21H19C20.1046 21 21 20.1046 21 19V7C21 5.89543 20.1046 5 19 5H5C3.89543 5 3 5.89543 3 7V19C3 20.1046 3.89543 21 5 21Z"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>
            </div>
            <div v-if="errors.birth_date" class="error-message">
              {{ errors.birth_date }}
            </div>
          </div>

          <div class="input-group full-width">
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

          <div class="input-group full-width">
            <label for="address" class="form-label cyber-dynamic"> Адрес </label>
            <div class="input-container">
              <input
                v-model="form.address"
                type="text"
                id="address"
                class="data-input"
                placeholder="Введите ваш адрес"
                :class="{ error: errors.address }"
                @input="validateField('address')"
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
                    d="M21 10C21 17 12 23 12 23C12 23 3 17 3 10C3 7.61305 3.94821 5.32387 5.63604 3.63604C7.32387 1.94821 9.61305 1 12 1C14.3869 1 16.6761 1.94821 18.364 3.63604C20.0518 5.32387 21 7.61305 21 10Z"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                  <path
                    d="M12 13C13.6569 13 15 11.6569 15 10C15 8.34315 13.6569 7 12 7C10.3431 7 9 8.34315 9 10C9 11.6569 10.3431 13 12 13Z"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>
            </div>
            <div v-if="errors.address" class="error-message">
              {{ errors.address }}
            </div>
          </div>
        </div>

        <button
          type="submit"
          class="submit-button cyber-heading"
          :disabled="!isFormValid || !hasChanges"
          :class="{ disabled: !isFormValid || !hasChanges }"
        >
          <span v-if="loading" class="button-loading">
            <div class="spinner"></div>
            Сохранение...
          </span>
          <span v-else>Изменить данные</span>
        </button>

        <div v-if="message" class="message" :class="messageType">
          {{ message }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useUserStore } from '@/stores/useUserStore'
import { storeToRefs } from 'pinia'
import { useNotificationsStore } from '@/stores/useToastStore'
const useUser = useUserStore()
const { getUser } = storeToRefs(useUserStore())
const notific = useNotificationsStore()
// Reactive state
const form = reactive({
  first_name: '',
  last_name: '',
  middle_name: '',
  birth_date: '',
  phone: '',
  address: '',
})

const initialForm = reactive({ ...form })
const emits = defineEmits(['onClose'])
const errors = reactive({
  first_name: '',
  last_name: '',
  middle_name: '',
  birth_date: '',
  phone: '',
  address: '',
})

const loading = ref(false)
const message = ref('')
const messageType = ref('')

// Computed properties
const isFormValid = computed(() => {
  return (
    Object.values(errors).every((error) => !error) &&
    form.first_name?.trim() &&
    form.last_name?.trim() &&
    form.phone?.trim()
  )
})

const hasChanges = computed(() => {
  return Object.keys(form).some((key) => form[key] !== initialForm[key])
})

// Methods
const validateField = (fieldName) => {
  // Безопасное получение значения с проверкой на undefined
  const value = form[fieldName]?.trim() || ''

  if (!value && fieldName !== 'middle_name' && fieldName !== 'address') {
    errors[fieldName] = 'Это поле обязательно для заполнения'
    return
  }

  // Дополнительные проверки для конкретных полей
  switch (fieldName) {
    case 'first_name':
    case 'last_name':
    case 'middle_name':
      if (value && value.length < 2) {
        errors[fieldName] = 'Минимальная длина - 2 символа'
      } else if (value && !/^[а-яА-ЯёЁa-zA-Z\- ]+$/.test(value)) {
        errors[fieldName] = 'Допустимы только буквы, дефисы и пробелы'
      } else {
        errors[fieldName] = ''
      }
      break
    case 'address':
      if (value && value.length < 5) {
        errors.address = 'Адрес должен содержать не менее 5 символов'
      } else if (value && !/^[а-яА-ЯёЁa-zA-Z0-9\-\s.,/]+$/.test(value)) {
        errors.address = 'Недопустимые символы в адресе'
      } else {
        errors.address = ''
      }
      break
    case 'birth_date':
      if (!value) {
        errors.birth_date = 'Выберите дату рождения'
      } else {
        validateBirthDate()
      }
      break
    default:
      errors[fieldName] = ''
  }
}

const validatePhone = () => {
  const phone = form.phone?.trim() || ''

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

const validateBirthDate = () => {
  const birthDate = form.birth_date

  if (!birthDate) {
    errors.birth_date = 'Выберите дату рождения'
    return
  }

  const selectedDate = new Date(birthDate)
  const today = new Date()
  const minDate = new Date()
  minDate.setFullYear(today.getFullYear() - 120) // Максимальный возраст 120 лет
  const maxDate = new Date()
  maxDate.setFullYear(today.getFullYear() - 14) // Минимальный возраст 14 лет

  if (selectedDate < minDate || selectedDate > maxDate) {
    errors.birth_date = 'Дата рождения должна быть в разумных пределах'
  } else {
    errors.birth_date = ''
  }
}

const loadUserData = () => {
  // Загружаем данные из store
  if (getUser.value) {
    const userData = getUser.value
    Object.keys(form).forEach((key) => {
      if (userData[key] !== undefined) {
        form[key] = userData[key] || ''
        initialForm[key] = userData[key] || ''
      }
    })
  }
}

const handleSubmit = async () => {
  if (!isFormValid || !hasChanges.value) return

  loading.value = true
  message.value = ''

  try {
    // Валидация всех полей перед отправкой
    validateField('first_name')
    validateField('last_name')
    validateField('middle_name')
    validateField('address')
    validateField('birth_date')
    validatePhone()

    if (!isFormValid) {
      throw new Error('Пожалуйста, исправьте ошибки в форме')
    }

    // Обновляем данные пользователя
    useUser.updateUser({
      first_name: form.first_name.trim(),
      last_name: form.last_name.trim(),
      middle_name: form.middle_name.trim(),
      birth_date: form.birth_date,
      phone: form.phone.trim(),
      address: form.address.trim(),
    })
    emits('onClose')
    notific.success('Вы успешно изменили данные')
    // Обновляем initialForm для отслеживания следующих изменений
    Object.keys(form).forEach((key) => {
      initialForm[key] = form[key]
    })
  } catch (error) {
    console.error('Ошибка при обновлении данных:', error)
    notific.error('Произошла ошибка при обновлении данных, попробуйте позже')
  } finally {
    loading.value = false
  }
}

// Watchers
watch(
  () => getUser.value,
  (newData) => {
    if (newData) {
      loadUserData()
    }
  },
  { deep: true, immediate: true },
)

watch(
  () => form.birth_date,
  () => {
    if (form.birth_date) {
      validateBirthDate()
    }
  },
)

// Lifecycle
onMounted(() => {
  loadUserData()
})
</script>

<style scoped>
.data-edit-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  padding: var(--spacing-xl);
  background: var(--gradient-subtle);
}

.data-edit-card {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-xl);
  padding: var(--spacing-2xl);
  width: 100%;
  max-width: 600px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--color-border);
  position: relative;
  overflow: hidden;
}

.data-edit-card::before {
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

.edit-form {
  width: 100%;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-2xl);
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group.full-width {
  grid-column: 1 / -1;
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

/* Адаптивность */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }

  .input-group.full-width {
    grid-column: 1;
  }
}

@media (max-width: 480px) {
  .data-edit-container {
    padding: var(--spacing-md);
  }

  .data-edit-card {
    padding: var(--spacing-xl);
  }
}
</style>
