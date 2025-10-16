<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Заголовок -->
      <div class="login-header">
        <h1 class="login-title">Вход в систему</h1>
        <p class="login-subtitle">Войдите в свой аккаунт</p>
      </div>

      <!-- Форма входа -->
      <form @submit.prevent="handleSubmit" class="login-form">
        <!-- Поле для логина или email -->
        <div class="form-group">
          <label for="login" class="form-label">Логин или Email *</label>
          <input
            id="login"
            v-model="form.login"
            type="text"
            class="form-input"
            :class="{ 'form-input--error': errors.login }"
            placeholder="Введите логин или email"
            required
            autocomplete="username"
          />
          <span v-if="errors.login" class="form-error">{{ errors.login }}</span>
        </div>

        <!-- Поле пароля -->
        <div class="form-group">
          <div class="form-label-wrapper">
            <label for="password" class="form-label">Пароль *</label>
            <RouterLink :to="{ name:  'forgot' }" class="forgot-password">
              Забыли пароль?
            </RouterLink>
          </div>
          <div class="password-input-wrapper">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              class="form-input"
              :class="{ 'form-input--error': errors.password }"
              placeholder="Введите ваш пароль"
              required
              autocomplete="current-password"
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

        <!-- Запомнить меня -->
        <div class="form-options">
          <div class="form-checkbox">
            <input
              id="rememberMe"
              v-model="form.rememberMe"
              type="checkbox"
              class="checkbox-input"
            />
            <label for="rememberMe" class="checkbox-label">
              Запомнить меня
            </label>
          </div>
        </div>

        <!-- Кнопка входа -->
        <button
          type="submit"
          class="submit-button"
          :disabled="isSubmitting"
          :class="{ 'submit-button--loading': isSubmitting }"
        >
          <span v-if="!isSubmitting">Войти</span>
          <div v-else class="loading-spinner">
            <i class="pi pi-spinner pi-spin"></i>
            <span>Вход...</span>
          </div>
        </button>

        <!-- Разделитель -->
        <div class="divider">
          <span class="divider-text">или</span>
        </div>

        <!-- Быстрый вход (опционально) -->
        <div class="social-login">
          <button type="button" class="social-button social-button--google" @click="handleSocialLogin('google')">
            <i class="pi pi-google"></i>
            <span>Войти через Google</span>
          </button>
          
          <button type="button" class="social-button social-button--github" @click="handleSocialLogin('github')">
            <i class="pi pi-github"></i>
            <span>Войти через GitHub</span>
          </button>
        </div>

        <!-- Ссылка на регистрацию -->
        <div class="register-link">
          Еще нет аккаунта? 
          <RouterLink :to="{ name:  'auth' }" class="link link--primary">Зарегистрироваться</RouterLink>
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
  login: '',
  password: '',
  rememberMe: false
})

// Ошибки валидации
const errors = reactive({
  login: '',
  password: ''
})

// Состояние UI
const showPassword = ref(false)
const isSubmitting = ref(false)

// Валидация формы
const validateForm = () => {
  let isValid = true

  // Очистка предыдущих ошибок
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })

  // Валидация логина/email
  if (!form.login.trim()) {
    errors.login = 'Введите логин или email'
    isValid = false
  } else if (form.login.length < 3) {
    errors.login = 'Логин должен содержать минимум 3 символа'
    isValid = false
  }

  // Валидация пароля
  if (!form.password) {
    errors.password = 'Введите пароль'
    isValid = false
  } else if (form.password.length < 6) {
    errors.password = 'Пароль должен содержать минимум 6 символов'
    isValid = false
  }

  return isValid
}

// Обработчик входа
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true

  try {
    // Имитация API запроса
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Здесь будет реальный API вызов
    console.log('Вход выполнен:', {
      login: form.login,
      rememberMe: form.rememberMe
    })

    // Успешный вход
    // В реальном приложении здесь будет редирект или обновление состояния авторизации
    alert('Вход выполнен успешно!')
    
    // В реальном приложении:
    // - Сохранение токена
    // - Редирект на главную
    // - Обновление состояния пользователя

  } catch (error) {
    console.error('Ошибка входа:', error)
    
    // В реальном приложении здесь будут конкретные ошибки от API
    if (error.message?.includes('credentials')) {
      errors.login = 'Неверный логин или пароль'
      errors.password = 'Неверный логин или пароль'
    } else {
      alert('Произошла ошибка при входе. Попробуйте еще раз.')
    }
  } finally {
    isSubmitting.value = false
  }
}

// Обработчик социального входа
const handleSocialLogin = (provider) => {
  console.log(`Социальный вход через: ${provider}`)
  // В реальном приложении здесь будет OAuth redirect
  alert(`Вход через ${provider} (в разработке)`)
}

// Автозаполнение для демонстрации
const fillDemoCredentials = () => {
  form.login = 'demo@example.com'
  form.password = 'demopassword123'
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  background: var(--color-bg-muted);
}

.login-card {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-lg);
  padding: var(--spacing-2xl);
  width: 100%;
  max-width: 440px;
  border: 1px solid var(--color-border);
}

.login-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.login-title {
  font-size: 2rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin: 0 0 var(--spacing-sm);
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-subtitle {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 1.125rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.form-label-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-label {
  font-weight: var(--font-weight-medium);
  color: var(--color-text);
  font-size: 0.875rem;
}

.forgot-password {
  color: var(--color-primary);
  font-size: 0.875rem;
  text-decoration: none;
  transition: color var(--transition-fast);
}

.forgot-password:hover {
  color: var(--color-primary-hover);
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
  width: 90%;
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

/* Опции формы */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: var(--spacing-sm) 0;
}

.form-checkbox {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.checkbox-input {
  width: 1.125rem;
  height: 1.125rem;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-sm);
  background: var(--color-bg);
  cursor: pointer;
}

.checkbox-label {
  font-size: 0.875rem;
  color: var(--color-text);
  cursor: pointer;
}

/* Кнопка входа */
.submit-button {
  background: var(--gradient-primary);
  color: var(--color-text-inverted);
  border: none;
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-md);
  font-size: 1rem;
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-normal);
  height: 52px;
  margin-top: var(--spacing-sm);
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

/* Разделитель */
.divider {
  position: relative;
  text-align: center;
  margin: var(--spacing-lg) 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--color-border);
}

.divider-text {
  background: var(--color-bg-elevated);
  padding: 0 var(--spacing-md);
  color: var(--color-text-muted);
  font-size: 0.875rem;
  position: relative;
  z-index: 1;
}

/* Социальный вход */
.social-login {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.social-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  background: var(--color-bg);
  color: var(--color-text);
  font-size: 0.875rem;
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.social-button:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
  border-color: var(--color-border-hover);
}

.social-button--google:hover {
  border-color: #db4437;
  background: #f8f8f8;
}

.social-button--github:hover {
  border-color: #333;
  background: #f6f8fa;
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

.register-link {
  text-align: center;
  color: var(--color-text-muted);
  font-size: 0.875rem;
  margin-top: var(--spacing-lg);
}

/* Демо кнопка (можно убрать в продакшене) */
.demo-button {
  background: var(--color-secondary-soft);
  color: var(--color-secondary);
  border: 1px solid var(--color-secondary-muted);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: 0.75rem;
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-top: var(--spacing-md);
}

.demo-button:hover {
  background: var(--color-secondary-muted);
}

/* Адаптивность */
@media (max-width: 768px) {
  .login-container {
    padding: var(--spacing-md);
  }

  .login-card {
    padding: var(--spacing-xl);
  }

  .login-title {
    font-size: 1.75rem;
  }

  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: var(--spacing-lg);
    margin: var(--spacing-sm);
  }

  .login-title {
    font-size: 1.5rem;
  }

  .social-button {
    font-size: 0.8rem;
    padding: var(--spacing-sm);
  }
}
</style>