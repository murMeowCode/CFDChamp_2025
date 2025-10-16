<template>
  <div class="register-container">
    <div class="register-card">
      <!-- Заголовок -->
      <div class="register-header">
        <h1 class="register-title">Регистрация</h1>
        <p class="register-subtitle">Создайте новый аккаунт</p>
      </div>

      <!-- Форма регистрации -->
      <form @submit.prevent="handleSubmit" class="register-form">
        <!-- ФИО - в одной строке -->
        <div class="form-row">
          <div class="form-group">
            <label for="lastName" class="form-label">Фамилия *</label>
            <input
              id="lastName"
              v-model="form.lastName"
              type="text"
              class="form-input"
              :class="{ 'form-input--error': errors.lastName }"
              placeholder="Иванов"
              required
            />
            <span v-if="errors.lastName" class="form-error">{{ errors.lastName }}</span>
          </div>

          <div class="form-group">
            <label for="firstName" class="form-label">Имя *</label>
            <input
              id="firstName"
              v-model="form.firstName"
              type="text"
              class="form-input"
              :class="{ 'form-input--error': errors.firstName }"
              placeholder="Иван"
              required
            />
            <span v-if="errors.firstName" class="form-error">{{ errors.firstName }}</span>
          </div>

          <div class="form-group">
            <label for="middleName" class="form-label">Отчество</label>
            <input
              id="middleName"
              v-model="form.middleName"
              type="text"
              class="form-input"
              :class="{ 'form-input--error': errors.middleName }"
              placeholder="Иванович"
            />
            <span v-if="errors.middleName" class="form-error">{{ errors.middleName }}</span>
          </div>
        </div>

        <!-- Основные поля -->
        <div class="form-group">
          <label for="login" class="form-label">Логин *</label>
          <input
            id="login"
            v-model="form.login"
            type="text"
            class="form-input"
            :class="{ 'form-input--error': errors.login }"
            placeholder="Придумайте логин"
            required
          />
          <span v-if="errors.login" class="form-error">{{ errors.login }}</span>
        </div>

        <div class="form-group">
          <label for="email" class="form-label">Email *</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="form-input"
            :class="{ 'form-input--error': errors.email }"
            placeholder="your@email.com"
            required
          />
          <span v-if="errors.email" class="form-error">{{ errors.email }}</span>
        </div>

        <div class="form-group">
          <label for="birthDate" class="form-label">Дата рождения *</label>
          <input
            id="birthDate"
            v-model="form.birthDate"
            type="date"
            class="form-input"
            :class="{ 'form-input--error': errors.birthDate }"
            required
          />
          <span v-if="errors.birthDate" class="form-error">{{ errors.birthDate }}</span>
        </div>

        <!-- Пароли -->
        <div class="form-row">
          <div class="form-group">
            <label for="password" class="form-label">Пароль *</label>
            <div class="password-input-wrapper">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                :class="{ 'form-input--error': errors.password }"
                placeholder="Не менее 8 символов"
                required
              />
              <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
                :aria-label="showPassword ? 'Скрыть пароль' : 'Показать пароль'"
              >
                <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
              </button>
            </div>
            <span v-if="errors.password" class="form-error">{{ errors.password }}</span>
          </div>

          <div class="form-group">
            <label for="confirmPassword" class="form-label">Подтверждение пароля *</label>
            <div class="password-input-wrapper">
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                class="form-input"
                :class="{ 'form-input--error': errors.confirmPassword }"
                placeholder="Повторите пароль"
                required
              />
              <button
                type="button"
                class="password-toggle"
                @click="showConfirmPassword = !showConfirmPassword"
                :aria-label="showConfirmPassword ? 'Скрыть пароль' : 'Показать пароль'"
              >
                <i :class="showConfirmPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
              </button>
            </div>
            <span v-if="errors.confirmPassword" class="form-error">{{ errors.confirmPassword }}</span>
          </div>
        </div>

        <!-- Соглашение -->
        <div class="form-checkbox">
          <input
            id="agreement"
            v-model="form.agreement"
            type="checkbox"
            class="checkbox-input"
            required
          />
          <label for="agreement" class="checkbox-label">
            Я соглашаюсь с 
            <a href="#" class="link">условиями использования</a>
            и 
            <a href="#" class="link">политикой конфиденциальности</a>
          </label>
        </div>

        <!-- Кнопка отправки -->
        <button
          type="submit"
          class="submit-button"
          :disabled="isSubmitting"
          :class="{ 'submit-button--loading': isSubmitting }"
        >
          <span v-if="!isSubmitting">Зарегистрироваться</span>
          <div v-else class="loading-spinner">
            <i class="pi pi-spinner pi-spin"></i>
            <span>Регистрация...</span>
          </div>
        </button>

        <!-- Ссылка на вход -->
        <div class="login-link">
          Уже есть аккаунт? 
          <RouterLink :to="{ name:  'login' }" class="link link--primary">Войти</RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { RouterLink } from 'vue-router'

// Состояние формы
const form = reactive({
  lastName: '',
  firstName: '',
  middleName: '',
  login: '',
  email: '',
  birthDate: '',
  password: '',
  confirmPassword: '',
  agreement: false
})

// Ошибки валидации
const errors = reactive({
  lastName: '',
  firstName: '',
  middleName: '',
  login: '',
  email: '',
  birthDate: '',
  password: '',
  confirmPassword: ''
})

// Состояние UI
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isSubmitting = ref(false)

// Валидация формы
const validateForm = () => {
  let isValid = true

  // Очистка предыдущих ошибок
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })

  // Валидация ФИО
  if (!form.lastName.trim()) {
    errors.lastName = 'Фамилия обязательна'
    isValid = false
  }

  if (!form.firstName.trim()) {
    errors.firstName = 'Имя обязательно'
    isValid = false
  }

  // Валидация логина
  if (!form.login.trim()) {
    errors.login = 'Логин обязателен'
    isValid = false
  } else if (form.login.length < 3) {
    errors.login = 'Логин должен содержать минимум 3 символа'
    isValid = false
  }

  // Валидация email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.email.trim()) {
    errors.email = 'Email обязателен'
    isValid = false
  } else if (!emailRegex.test(form.email)) {
    errors.email = 'Введите корректный email'
    isValid = false
  }

  // Валидация даты рождения
  if (!form.birthDate) {
    errors.birthDate = 'Дата рождения обязательна'
    isValid = false
  } else {
    const birthDate = new Date(form.birthDate)
    const today = new Date()
    const minDate = new Date()
    minDate.setFullYear(today.getFullYear() - 100)
    
    if (birthDate > today) {
      errors.birthDate = 'Дата рождения не может быть в будущем'
      isValid = false
    } else if (birthDate < minDate) {
      errors.birthDate = 'Проверьте корректность даты рождения'
      isValid = false
    }
  }

  // Валидация пароля
  if (!form.password) {
    errors.password = 'Пароль обязателен'
    isValid = false
  } else if (form.password.length < 8) {
    errors.password = 'Пароль должен содержать минимум 8 символов'
    isValid = false
  }

  // Подтверждение пароля
  if (!form.confirmPassword) {
    errors.confirmPassword = 'Подтвердите пароль'
    isValid = false
  } else if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Пароли не совпадают'
    isValid = false
  }

  return isValid
}

// Обработчик отправки формы
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true

  try {
    // Имитация API запроса
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Здесь будет реальный API вызов
    console.log('Форма отправлена:', {
      ...form,
      password: '***' // Не логируем реальный пароль
    })

    // Успешная регистрация
    alert('Регистрация успешно завершена!')
    
    // Сброс формы
    Object.keys(form).forEach(key => {
      if (key !== 'agreement') {
        form[key] = ''
      }
    })
    form.agreement = false

  } catch (error) {
    console.error('Ошибка регистрации:', error)
    alert('Произошла ошибка при регистрации. Попробуйте еще раз.')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  background: var(--color-bg-muted);
}

.register-card {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-lg);
  padding: var(--spacing-2xl);
  width: 100%;
  max-width: 1200px;
  border: 1px solid var(--color-border);
}

.register-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.register-title {
  font-size: 2rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin: 0 0 var(--spacing-sm);
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.register-subtitle {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 1.125rem;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: var(--spacing-md);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.form-label {
  font-weight: var(--font-weight-medium);
  color: var(--color-text);
  font-size: 0.875rem;
}

.form-input {
  padding: var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
  background: var(--color-bg);
  color: var(--color-text);
  font-size: 1rem;
  transition: all var(--transition-normal);
  outline: none;
}

.form-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.form-input--error {
  border-color: var(--color-error);
}

.form-input--error:focus {
  border-color: var(--color-error);
  box-shadow: 0 0 0 3px var(--color-error-soft);
}

.form-error {
  color: var(--color-error);
  font-size: 0.75rem;
  font-weight: var(--font-weight-medium);
}

/* Стили для поля пароля */
.password-input-wrapper {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: var(--spacing-md);
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: var(--spacing-xs);
  border-radius: var(--border-radius-sm);
  transition: all var(--transition-fast);
}

.password-toggle:hover {
  color: var(--color-primary);
  background: var(--color-primary-soft);
}

/* Чекбокс */
.form-checkbox {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-sm);
  margin: var(--spacing-md) 0;
}

.checkbox-input {
  margin-top: 0.25rem;
  width: 1.125rem;
  height: 1.125rem;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-sm);
  background: var(--color-bg);
  cursor: pointer;
}

.checkbox-label {
  font-size: 0.875rem;
  color: var(--color-text-muted);
  line-height: 1.4;
}

/* Кнопка отправки */
.submit-button {
  background: var(--gradient-primary);
  color: var(--color-text-inverted);
  border: none;
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: 1rem;
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-normal);
  height: 52px;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.submit-button--loading {
  cursor: wait;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
}

/* Ссылки */
.link {
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.link:hover {
  color: var(--color-primary-hover);
}

.link--primary {
  font-weight: var(--font-weight-medium);
}

.login-link {
  text-align: center;
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

/* Адаптивность */
@media (max-width: 768px) {
  .register-container {
    padding: var(--spacing-md);
  }

  .register-card {
    padding: var(--spacing-xl);
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }

  .register-title {
    font-size: 1.75rem;
  }
}

@media (max-width: 480px) {
  .register-card {
    padding: var(--spacing-lg);
  }

  .register-title {
    font-size: 1.5rem;
  }
}
</style>