<template>
  <div class="password-reset-container">
    <div class="password-reset-card">
      <div class="card-header">
        <h1 class="cyber-heading">Обновление пароля</h1>
        <p class="futurism-elegant">Создайте новый надежный пароль</p>
      </div>

      <form @submit.prevent="handleSubmit" class="password-form">
        <div class="form-group">
          <label for="newPassword" class="form-label cyber-dynamic"> Новый пароль </label>
          <div class="input-container">
            <input
              v-model="form.newPassword"
              :type="showNewPassword ? 'text' : 'password'"
              id="newPassword"
              class="password-input"
              placeholder="Введите новый пароль"
              required
              :disabled="!token || loading"
              @input="validatePassword"
            />
            <button
              type="button"
              class="password-toggle"
              :disabled="!token || loading"
              @click="togglePasswordVisibility('new')"
            >
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  v-if="!showNewPassword"
                  d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  v-if="!showNewPassword"
                  d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  v-if="showNewPassword"
                  d="M17.94 17.94C16.76 19.12 14.48 20 12 20C5 20 1 12 1 12C1 12 3 8 6.06 6.06"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  v-if="showNewPassword"
                  d="M9.9 4.24C10.59 4.08 11.3 4 12 4C19 4 23 12 23 12C23 12 22.1 13.76 20.94 15.06"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  v-if="showNewPassword"
                  d="M1 1L23 23"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </button>
          </div>

          <div class="password-strength">
            <div class="strength-bar" :style="strengthBarStyle"></div>
          </div>

          <div class="password-requirements">
            <div
              v-for="requirement in passwordRequirements"
              :key="requirement.id"
              class="requirement"
              :class="{ valid: requirement.valid }"
            >
              <span class="requirement-icon">
                {{ requirement.valid ? '✓' : '●' }}
              </span>
              {{ requirement.text }}
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="confirmPassword" class="form-label cyber-dynamic">
            Подтверждение пароля
          </label>
          <div class="input-container">
            <input
              v-model="form.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              id="confirmPassword"
              class="password-input"
              placeholder="Повторите новый пароль"
              required
              :disabled="!token || loading"
              @input="validatePasswordMatch"
            />
            <button
              type="button"
              class="password-toggle"
              :disabled="!token || loading"
              @click="togglePasswordVisibility('confirm')"
            >
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  v-if="!showConfirmPassword"
                  d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  v-if="!showConfirmPassword"
                  d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  v-if="showConfirmPassword"
                  d="M17.94 17.94C16.76 19.12 14.48 20 12 20C5 20 1 12 1 12C1 12 3 8 6.06 6.06"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  v-if="showConfirmPassword"
                  d="M9.9 4.24C10.59 4.08 11.3 4 12 4C19 4 23 12 23 12C23 12 22.1 13.76 20.94 15.06"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  v-if="showConfirmPassword"
                  d="M1 1L23 23"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </button>
          </div>
          <div
            v-if="form.confirmPassword"
            class="match-message"
            :class="passwordsMatch ? 'valid' : 'error'"
          >
            {{ passwordsMatch ? '✓ Пароли совпадают' : '✗ Пароли не совпадают' }}
          </div>
        </div>

        <button
          type="submit"
          class="submit-button cyber-heading"
          :disabled="!isFormValid"
          :class="{ disabled: !isFormValid }"
        >
          <span v-if="loading" class="button-loading">
            <div class="spinner"></div>
            Обновление...
          </span>
          <span v-else>Поменять пароль</span>
        </button>

        <div v-if="message" class="message" :class="messageType">
          {{ message }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useApiMutations } from '@/utils/api/useApiMutation'
import { useNotificationsStore } from '@/stores/useToastStore'
import { api8000 } from '@/utils/apiUrl/urlApi'
// Emits
const emit = defineEmits(['passwordUpdated'])
const { usePost } = useApiMutations()
const notifications = useNotificationsStore()
// Reactive state
const token = ref(null)
const form = reactive({
  newPassword: '',
  confirmPassword: '',
})
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)
const loading = ref(false)
const passwordStrength = ref(0)
const message = ref('')
const messageType = ref('')

const passwordRequirements = ref([
  { id: 'length', text: 'Минимум 8 символов', valid: false },
  { id: 'uppercase', text: 'Заглавная буква', valid: false },
  { id: 'lowercase', text: 'Строчная буква', valid: false },
  { id: 'number', text: 'Цифра', valid: false },
  { id: 'special', text: 'Специальный символ', valid: false },
])

// Computed properties
const passwordsMatch = computed(() => {
  return form.newPassword && form.confirmPassword && form.newPassword === form.confirmPassword
})

const isFormValid = computed(() => {
  return token.value && passwordsMatch.value && passwordStrength.value >= 4 && !loading.value
})

const strengthBarStyle = computed(() => {
  const width = (passwordStrength.value / 5) * 100
  let background

  if (passwordStrength.value <= 2) {
    background = 'var(--color-error)'
  } else if (passwordStrength.value <= 3) {
    background = 'var(--color-warning)'
  } else {
    background = 'var(--color-success)'
  }

  return {
    width: `${width}%`,
    background: background,
  }
})
const resetMutation = usePost(`${api8000}/auth/reset-password`, {
  onSuccess: (data) => {
    console.log('✅ Восстановление:', data)
    // Успешная отправка
    isSuccess.value = true
    startCooldown()
    notifications.success('Вы успешно обновили пароль')
  },
  onError: (error) => {
    console.error('❌ Ошибка обновления пароля:', error)
    notifications.error('Произошла ошибка при обновлении пароля', 'Попробуйте еще раз')
  },
})
const maskedToken = computed(() => {
  if (!token.value) return ''
  // Показываем только первые и последние 4 символа токена для безопасности
  return `${token.value.substring(0, 8)}...${token.value.substring(token.value.length - 4)}`
})

// Methods
const extractTokenFromQuery = () => {
  const urlParams = new URLSearchParams(window.location.search)
  token.value = urlParams.get('token')

  if (!token.value) {
    showMessage('Токен не найден в URL', 'error')
  }
}

const validateToken = async () => {
  if (!token.value) return

  loading.value = true
  try {
    // Здесь должна быть проверка валидности токена на сервере
    await new Promise((resolve) => setTimeout(resolve, 1000))

    console.log('Токен валиден:', token.value)
  } catch (error) {
    console.error('Ошибка проверки токена:', error)
    showMessage('Токен недействителен или устарел', 'error')
    token.value = null
  } finally {
    loading.value = false
  }
}

const validatePassword = () => {
  const password = form.newPassword

  // Проверка требований к паролю
  passwordRequirements.value[0].valid = password.length >= 8
  passwordRequirements.value[1].valid = /[A-Z]/.test(password)
  passwordRequirements.value[2].valid = /[a-z]/.test(password)
  passwordRequirements.value[3].valid = /\d/.test(password)
  passwordRequirements.value[4].valid = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)

  // Расчет силы пароля
  passwordStrength.value = passwordRequirements.value.filter((req) => req.valid).length
}

const validatePasswordMatch = () => {
  // Реактивная валидация уже обрабатывается в computed свойствах
}

const togglePasswordVisibility = (type) => {
  if (type === 'new') {
    showNewPassword.value = !showNewPassword.value
  } else {
    showConfirmPassword.value = !showConfirmPassword.value
  }
}

const handleSubmit = async () => {
  if (!isFormValid.value) return

  loading.value = true
  message.value = ''

  try {
    await resetMutation.mutateAsync({ token: token.value, new_password: form.newPassword })

    // Сброс формы
    form.newPassword = ''
    form.confirmPassword = ''
    passwordStrength.value = 0
    passwordRequirements.value.forEach((req) => (req.valid = false))
  } catch (error) {
    console.error('Ошибка при обновлении пароля:', error)
  } finally {
    loading.value = false
  }
}

const showMessage = (text, type) => {
  message.value = text
  messageType.value = type

  setTimeout(() => {
    message.value = ''
    messageType.value = ''
  }, 5000)
}

// Lifecycle
onMounted(() => {
  extractTokenFromQuery()
  validateToken()
})
</script>

<style scoped>
.password-reset-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  padding: var(--spacing-xl);
  background: var(--gradient-subtle);
}

.password-reset-card {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-xl);
  padding: var(--spacing-2xl);
  width: 100%;
  max-width: 480px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--color-border);
  position: relative;
  overflow: hidden;
}

.password-reset-card::before {
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
  margin-bottom: var(--spacing-md);
}

.token-info {
  background: var(--color-primary-soft);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-primary-muted);
  margin-top: var(--spacing-md);
}

.token-error {
  background: var(--color-error-soft);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-error);
  margin-top: var(--spacing-md);
}

.error-message {
  color: var(--color-error);
  font-weight: 500;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.form-label {
  font-weight: 600;
  color: var(--color-text);
  font-size: 1rem;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  padding-right: 3rem;
  background: var(--color-bg-subtle);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  font-family: 'Exo 2', sans-serif;
  font-size: 1rem;
  color: var(--color-text);
  transition: all var(--transition-normal);
  outline: none;
}

.password-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
  background: var(--color-bg-elevated);
}

.password-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.password-input::placeholder {
  color: var(--color-text-light);
  opacity: 0.7;
}

.password-toggle {
  position: absolute;
  right: var(--spacing-md);
  background: none;
  border: none;
  color: var(--color-text-light);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
  padding: 4px;
  border-radius: var(--border-radius-sm);
}

.password-toggle:hover:not(:disabled) {
  color: var(--color-primary);
  background: var(--color-primary-soft);
}

.password-toggle:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.password-strength {
  height: 6px;
  background: var(--color-border);
  border-radius: var(--border-radius-full);
  overflow: hidden;
  margin-top: var(--spacing-xs);
}

.strength-bar {
  height: 100%;
  border-radius: var(--border-radius-full);
  transition: all var(--transition-normal);
}

.password-requirements {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  margin-top: var(--spacing-sm);
}

.requirement {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 0.85rem;
  color: var(--color-text-light);
  transition: color var(--transition-normal);
}

.requirement.valid {
  color: var(--color-success);
}

.requirement-icon {
  font-size: 0.7rem;
  width: 16px;
  text-align: center;
}

.match-message {
  font-size: 0.85rem;
  margin-top: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  transition: all var(--transition-normal);
}

.match-message.valid {
  color: var(--color-success);
  background: var(--color-success-soft);
}

.match-message.error {
  color: var(--color-error);
  background: var(--color-error-soft);
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
@media (max-width: 480px) {
  .password-reset-container {
    padding: var(--spacing-md);
  }

  .password-reset-card {
    padding: var(--spacing-xl);
  }

  .password-requirements {
    font-size: 0.8rem;
  }
}
</style>
