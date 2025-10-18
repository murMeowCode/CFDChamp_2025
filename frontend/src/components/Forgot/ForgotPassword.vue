<template>
  <div class="forgot-password-container" data-aos="zoom-in">
    <div class="forgot-password-card">
      <!-- Заголовок -->
      <div class="forgot-password-header">
        <div class="logo-wrapper">
          <i class="pi pi-key"></i>
        </div>
        <p class="forgot-password-subtitle">
          Введите email, и мы отправим вам ссылку для сброса пароля
        </p>
      </div>

      <!-- Форма восстановления -->
      <form @submit.prevent="handleSubmit" class="forgot-password-form">
        <!-- Поле email -->
        <div class="form-group floating-group">
          <div class="input-container">
            <input
              id="email"
              v-model="form.email"
              type="email"
              class="form-input floating-input"
              :class="{
                'form-input--error': errors.email,
                'form-input--filled': form.email,
              }"
              placeholder=" "
              required
              autocomplete="email"
              @focus="handleInputFocus('email')"
              @blur="handleInputBlur('email')"
            />
            <label
              for="email"
              class="floating-label"
              :class="{
                'floating-label--active': form.email || isFocused.email,
              }"
            >
              <i class="pi pi-envelope"></i>
              Email адрес
            </label>
            <div class="input-decoration"></div>
          </div>
          <span v-if="errors.email" class="form-error">
            <i class="pi pi-exclamation-circle"></i>
            {{ errors.email }}
          </span>
        </div>

        <!-- Кнопка отправки -->
        <button
          type="submit"
          class="submit-button beauty-button"
          :disabled="isSubmitting"
          :class="{
            'submit-button--loading': isSubmitting,
            'beauty-button--loading': isSubmitting,
          }"
        >
          <span v-if="!isSubmitting" class="button-content">
            <i class="pi pi-send"></i>
            Отправить ссылку
          </span>
          <div v-else class="loading-spinner">
            <div class="spinner-circle"></div>
            <span>Отправка...</span>
          </div>
        </button>

        <!-- Дополнительные действия -->
        <div class="form-actions">
          <RouterLink :to="{ name: 'login' }" class="back-link beauty-link">
            <i class="pi pi-arrow-left"></i>
            Вернуться к входу
          </RouterLink>
        </div>
      </form>

      <!-- Успешное сообщение -->
      <div v-if="isSuccess" class="success-message">
        <div class="success-icon">
          <i class="pi pi-check-circle"></i>
        </div>
        <div class="success-content">
          <h3 class="success-title">Письмо отправлено!</h3>
          <p class="success-description">
            Мы отправили ссылку для сброса пароля на адрес
            <strong>{{ form.email }}</strong
            >. Проверьте вашу почту.
          </p>
          <div class="success-actions">
            <button
              @click="handleResend"
              class="resend-button beauty-button beauty-button--outline"
              :disabled="isResending"
            >
              <i class="pi pi-refresh" :class="{ 'pi-spin': isResending }"></i>
              Отправить повторно
            </button>
            <div class="timer" v-if="cooldown > 0">
              Можно отправить снова через: {{ cooldown }}с
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useNotificationsStore } from '@/stores/useToastStore'

const notifications = useNotificationsStore()

// Состояние формы
const form = reactive({
  email: '',
})

// Ошибки валидации
const errors = reactive({
  email: '',
})

// Состояние UI
const isSubmitting = ref(false)
const isSuccess = ref(false)
const isResending = ref(false)
const cooldown = ref(0)
let cooldownTimer = null

// Отслеживание фокуса
const isFocused = reactive({
  email: false,
})

// Обработчики фокуса
const handleInputFocus = (field) => {
  isFocused[field] = true
}

const handleInputBlur = (field) => {
  isFocused[field] = false
}

// Валидация формы
const validateForm = () => {
  let isValid = true

  // Очистка предыдущих ошибок
  Object.keys(errors).forEach((key) => {
    errors[key] = ''
  })

  // Валидация email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.email.trim()) {
    errors.email = 'Email обязателен'
    isValid = false
  } else if (!emailRegex.test(form.email)) {
    errors.email = 'Введите корректный email адрес'
    isValid = false
  }

  return isValid
}

// Запуск таймера обратного отсчета
const startCooldown = () => {
  cooldown.value = 60
  cooldownTimer = setInterval(() => {
    cooldown.value--
    if (cooldown.value <= 0) {
      clearInterval(cooldownTimer)
    }
  }, 1000)
}

// Обработчик отправки формы
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true

  try {
    // Имитация API запроса
    await new Promise((resolve) => setTimeout(resolve, 1500))

    // Успешная отправка
    isSuccess.value = true
    startCooldown()

    notifications.success('Ссылка для восстановления отправлена на вашу почту', 'Проверьте email')
  } catch (error) {
    console.error('Ошибка восстановления:', error)
    notifications.error('Произошла ошибка при отправке ссылки', 'Попробуйте еще раз')
  } finally {
    isSubmitting.value = false
  }
}

// Повторная отправка
const handleResend = async () => {
  if (cooldown.value > 0) return

  isResending.value = true

  try {
    await new Promise((resolve) => setTimeout(resolve, 1000))

    startCooldown()
    notifications.info('Ссылка отправлена повторно', 'Проверьте почту')
  } catch (error) {
    notifications.error('Ошибка при повторной отправке')
  } finally {
    isResending.value = false
  }
}

// Очистка таймера при размонтировании
onUnmounted(() => {
  if (cooldownTimer) {
    clearInterval(cooldownTimer)
  }
})
</script>

<style scoped>
.forgot-password-container {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  background: var(--color-bg-muted);
}

.forgot-password-card {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-lg);
  padding: var(--spacing-2xl);
  width: 100%;
  max-width: 440px;
  backdrop-filter: var(--backdrop-blur);
  position: relative;
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.forgot-password-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--color-primary);
}

.forgot-password-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.logo-wrapper {
  margin-bottom: var(--spacing-lg);
}

.logo-wrapper i {
  font-size: 2.5rem;
  color: var(--color-primary);
  background: var(--color-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.forgot-password-title {
  font-size: 1.75rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin: 0 0 var(--spacing-sm);
  background: var(--color-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.forgot-password-subtitle {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 0.95rem;
  font-weight: var(--font-weight-normal);
  line-height: 1.5;
}

.forgot-password-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* Floating Label Styles */
.floating-group {
  position: relative;
}

.input-container {
  position: relative;
}

.floating-input {
  padding: 1.125rem 0.875rem 0.625rem 0.875rem;
  border: 1.5px solid var(--color-border);
  border-radius: var(--border-radius-md);
  background: var(--color-bg);
  color: var(--color-text);
  font-size: 0.9rem;
  transition: all var(--transition-normal);
  outline: none;
  width: 100%;
  height: 52px;
}

.floating-input:focus {
  border-color: var(--color-primary);
  background: var(--color-bg-elevated);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.floating-input--error {
  border-color: var(--color-error);
  background: var(--color-error-soft);
}

.floating-label {
  position: absolute;
  top: 50%;
  left: 0.875rem;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  font-size: 0.9rem;
  font-weight: var(--font-weight-normal);
  pointer-events: none;
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.floating-label i {
  font-size: 0.85rem;
  opacity: 0.7;
}

.floating-input:focus + .floating-label,
.floating-label--active {
  top: 0.625rem;
  transform: none;
  font-size: 0.75rem;
  color: var(--color-primary);
  font-weight: var(--font-weight-medium);
}

.input-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--color-primary);
  transform: scaleX(0);
  transition: transform var(--transition-normal);
}

.floating-input:focus ~ .input-decoration {
  transform: scaleX(1);
}

/* Button Styles */
.beauty-button {
  background: var(--color-primary);
  color: var(--color-text-inverted);
  border: none;
  border-radius: var(--border-radius-md);
  padding: 0.875rem 1.75rem;
  font-size: 0.95rem;
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-normal);
  height: 48px;
  margin-top: var(--spacing-sm);
}

.beauty-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.beauty-button:active:not(:disabled) {
  transform: translateY(0);
}

.beauty-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.beauty-button--outline {
  background: transparent;
  border: 1.5px solid var(--color-primary);
  color: var(--color-primary);
}

.beauty-button--outline:hover:not(:disabled) {
  background: var(--color-primary);
  color: var(--color-text-inverted);
}

.button-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.button-content i {
  font-size: 0.9rem;
}

/* Loading Spinner */
.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spinner-circle {
  width: 18px;
  height: 18px;
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

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: center;
  margin-top: var(--spacing-lg);
}

.beauty-link {
  color: var(--color-primary);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.beauty-link:hover {
  color: var(--color-primary-hover);
}

.beauty-link i {
  font-size: 0.8rem;
}

/* Success Message */
.success-message {
  background: var(--color-success-soft);
  border: 1px solid var(--color-success);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  margin-top: var(--spacing-xl);
  text-align: center;
}

.success-icon {
  font-size: 3rem;
  color: var(--color-success);
  margin-bottom: var(--spacing-lg);
}

.success-content {
  color: var(--color-text);
}

.success-title {
  font-size: 1.25rem;
  font-weight: var(--font-weight-semibold);
  margin: 0 0 var(--spacing-sm);
  color: var(--color-success);
}

.success-description {
  color: var(--color-text-muted);
  margin: 0 0 var(--spacing-lg);
  line-height: 1.5;
  font-size: 0.9rem;
}

.success-actions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  align-items: center;
}

.resend-button {
  min-width: 180px;
}

.timer {
  font-size: 0.8rem;
  color: var(--color-text-light);
  font-weight: var(--font-weight-medium);
}

/* Error Styles */
.form-error {
  display: flex;
  align-items: center;
  color: var(--color-error);
  font-size: 0.75rem;
  font-weight: var(--font-weight-medium);
  margin-top: 0.375rem;
  padding: 0.5rem 0.75rem;
  background: var(--color-error-soft);
  border-radius: var(--border-radius-sm);
  border-left: 3px solid var(--color-error);
  gap: 0.375rem;
}

.form-error i {
  font-size: 0.7rem;
}

/* Адаптивность */
@media (max-width: 768px) {
  .forgot-password-container {
    padding: var(--spacing-lg);
  }

  .forgot-password-card {
    padding: var(--spacing-xl);
    margin: var(--spacing-sm);
  }

  .forgot-password-title {
    font-size: 1.5rem;
  }

  .success-message {
    padding: var(--spacing-lg);
  }

  .success-icon {
    font-size: 2.5rem;
  }
}

@media (max-width: 480px) {
  .forgot-password-container {
    padding: var(--spacing-md);
  }

  .forgot-password-card {
    padding: var(--spacing-lg);
    border-radius: var(--border-radius-lg);
  }

  .forgot-password-title {
    font-size: 1.25rem;
  }

  .forgot-password-subtitle {
    font-size: 0.875rem;
  }

  .floating-input {
    height: 48px;
    font-size: 0.875rem;
  }

  .beauty-button {
    height: 44px;
    font-size: 0.9rem;
  }

  .success-actions {
    flex-direction: column;
  }
}
</style>
