<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Заголовок -->
      <div class="login-header">
        <div class="logo-wrapper">
          <i class="pi pi-shield" style="font-size: 2.5rem; color: var(--color-primary);"></i>
        </div>
        <h1 class="login-title">Добро пожаловать</h1>
        <p class="login-subtitle">Войдите в свой аккаунт</p>
      </div>

      <!-- Форма входа -->
      <form @submit.prevent="handleSubmit" class="login-form">
        <!-- Поле для логина или email -->
        <div class="form-group floating-group">
          <div class="input-container">
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-input floating-input"
              :class="{ 
                'form-input--error': errors.username,
                'form-input--filled': form.username 
              }"
              placeholder=" "
              required
              autocomplete="username"
            />
            <label for="username" class="floating-label">
              <i class="pi pi-user" style="margin-right: 8px;"></i>
              Логин или Email
            </label>
            <div class="input-decoration"></div>
          </div>
          <span v-if="errors.username" class="form-error">
            <i class="pi pi-exclamation-circle" style="margin-right: 4px;"></i>
            {{ errors.username }}
          </span>
        </div>

        <!-- Поле пароля -->
        <div class="form-group floating-group">
          <div class="input-container">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              class="form-input floating-input"
              :class="{ 
                'form-input--error': errors.password,
                'form-input--filled': form.password 
              }"
              placeholder=" "
              required
              autocomplete="current-password"
            />
            <label for="password" class="floating-label">
              <i class="pi pi-lock" style="margin-right: 8px;"></i>
              Пароль
            </label>
            <div class="input-decoration"></div>
            
            <button
              type="button"
              class="password-toggle beauty-toggle"
              @click="showPassword = !showPassword"
              :aria-label="showPassword ? 'Скрыть пароль' : 'Показать пароль'"
            >
              <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
            </button>
          </div>
          <div class="password-actions">
            <RouterLink :to="{ name: 'forgot' }" class="forgot-password beauty-link">
              <i class="pi pi-key" style="margin-right: 6px;"></i>
              Забыли пароль?
            </RouterLink>
          </div>
          <span v-if="errors.password" class="form-error">
            <i class="pi pi-exclamation-circle" style="margin-right: 4px;"></i>
            {{ errors.password }}
          </span>
        </div>

        <!-- Запомнить меня -->
        <div class="form-options">
          <div class="beauty-checkbox">
            <input
              id="rememberMe"
              v-model="form.rememberMe"
              type="checkbox"
              class="checkbox-input"
            />
            <label for="rememberMe" class="checkbox-label">
              <div class="checkbox-decoration">
                <i class="pi pi-check"></i>
              </div>
              <span class="checkbox-text">Запомнить меня</span>
            </label>
          </div>
        </div>

        <!-- Кнопка входа -->
        <button
          type="submit"
          class="submit-button beauty-button"
          :disabled="isSubmitting"
          :class="{ 
            'submit-button--loading': isSubmitting,
            'beauty-button--loading': isSubmitting
          }"
        >
          <span v-if="!isSubmitting" class="button-content">
            <i class="pi pi-sign-in" style="margin-right: 8px;"></i>
            Войти в систему
          </span>
          <div v-else class="loading-spinner">
            <div class="spinner-circle"></div>
            <span>Выполняется вход...</span>
          </div>
        </button>

        <!-- Разделитель -->
        <div class="divider beauty-divider">
          <div class="divider-line"></div>
          <span class="divider-text">или продолжите через</span>
          <div class="divider-line"></div>
        </div>

        <!-- Быстрый вход -->
        <div class="social-login">
          <button type="button" class="social-button social-button--google beauty-social" @click="handleSocialLogin('google')">
            <div class="social-icon">
              <i class="pi pi-google"></i>
            </div>
            <span class="social-text">Google</span>
          </button>
          
          <button type="button" class="social-button social-button--github beauty-social" @click="handleSocialLogin('github')">
            <div class="social-icon">
              <i class="pi pi-github"></i>
            </div>
            <span class="social-text">GitHub</span>
          </button>

          <button type="button" class="social-button social-button--twitter beauty-social" @click="handleSocialLogin('twitter')">
            <div class="social-icon">
              <i class="pi pi-twitter"></i>
            </div>
            <span class="social-text">Twitter</span>
          </button>
        </div>

        <!-- Ссылка на регистрацию -->
        <div class="register-link beauty-register">
          <span class="register-text">Впервые у нас?</span>
          <RouterLink :to="{ name: 'auth' }" class="register-action beauty-link">
            <i class="pi pi-user-plus" style="margin-right: 6px;"></i>
            Создать аккаунт
          </RouterLink>
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
  username: '',
  password: '',
  rememberMe: false
})

// Ошибки валидации
const errors = reactive({
  username: '',
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
  if (!form.username.trim()) {
    errors.username = 'Введите логин или email'
    isValid = false
  } else if (form.username.length < 3) {
    errors.username = 'Логин должен содержать минимум 3 символа'
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
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Здесь будет реальный API вызов
    console.log('Вход выполнен:', {
      username: form.username,
      rememberMe: form.rememberMe
    })

    // Успешный вход
    alert('Вход выполнен успешно!')
    
  } catch (error) {
    console.error('Ошибка входа:', error)
    
    if (error.message?.includes('credentials')) {
      errors.username = 'Неверный логин или пароль'
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
  alert(`Вход через ${provider} (в разработке)`)
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  background: linear-gradient(135deg, var(--color-bg-muted) 0%, var(--color-primary-soft) 100%);
  position: relative;
}

.login-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
}

.login-card {
  background: var(--color-bg-elevated);
  border-radius: 24px;
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  padding: 3rem;
  width: 100%;
  max-width: 440px;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-primary);
}

.login-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.logo-wrapper {
  margin-bottom: 1rem;
}

.login-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 0.5rem;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-subtitle {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 1rem;
  font-weight: 400;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Floating Label Styles */
.floating-group {
  position: relative;
}

.input-container {
  position: relative;
}

.floating-input {
  padding: 1.5rem 1rem 0.5rem 1rem;
  border: 2px solid var(--color-border);
  border-radius: 12px;
  background: var(--color-bg);
  color: var(--color-text);
  font-size: 1rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  outline: none;
  width: 100%;
  height: 56px;
}

.floating-input:focus {
  border-color: var(--color-primary);
  background: var(--color-bg-elevated);
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.floating-input--filled {
  border-color: var(--color-primary-muted);
  background: var(--color-bg-elevated);
}

.floating-input--error {
  border-color: var(--color-error);
  background: var(--color-error-soft);
}

.floating-label {
  position: absolute;
  top: 50%;
  left: 1rem;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  font-size: 1rem;
  font-weight: 500;
  pointer-events: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
}

.floating-input:focus + .floating-label,
.floating-input--filled + .floating-label {
  top: 0.75rem;
  transform: none;
  font-size: 0.75rem;
  color: var(--color-primary);
  font-weight: 600;
}

.input-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-primary);
  transform: scaleX(0);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.floating-input:focus ~ .input-decoration {
  transform: scaleX(1);
}

/* Password Toggle */
.beauty-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: var(--color-primary-soft);
  border: none;
  color: var(--color-primary);
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.beauty-toggle:hover {
  background: var(--color-primary);
  color: white;
  transform: translateY(-50%) scale(1.1);
}

/* Password Actions */
.password-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.beauty-link {
  color: var(--color-primary);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.beauty-link:hover {
  color: var(--color-primary-hover);
  transform: translateX(2px);
}

/* Checkbox Styles */
.beauty-checkbox {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.checkbox-input {
  display: none;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.checkbox-label:hover {
  transform: translateY(-1px);
}

.checkbox-decoration {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-border);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  background: var(--color-bg);
}

.checkbox-input:checked + .checkbox-label .checkbox-decoration {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.checkbox-input:checked + .checkbox-label .checkbox-decoration i {
  transform: scale(1);
}

.checkbox-decoration i {
  font-size: 0.75rem;
  transform: scale(0);
  transition: transform 0.3s ease;
}

.checkbox-text {
  color: var(--color-text);
  font-size: 0.875rem;
  font-weight: 500;
}

/* Button Styles */
.beauty-button {
  background: var(--gradient-primary);
  color: white;
  border: none;
  border-radius: 16px;
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  height: 56px;
  margin-top: 0.5rem;
  position: relative;
  overflow: hidden;
}

.beauty-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s ease;
}

.beauty-button:hover::before {
  left: 100%;
}

.beauty-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 32px rgba(0, 0, 0, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.1);
}

.beauty-button:active:not(:disabled) {
  transform: translateY(0);
}

.beauty-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.button-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Loading Spinner */
.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.spinner-circle {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Divider Styles */
.beauty-divider {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 1.5rem 0;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-border), transparent);
}

.divider-text {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
}

/* Social Login Styles */
.social-login {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

.beauty-social {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border: 2px solid var(--color-border);
  border-radius: 12px;
  background: var(--color-bg);
  color: var(--color-text);
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 80px;
}

.beauty-social:hover {
  transform: translateY(-2px);
  border-color: var(--color-primary);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.social-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: var(--color-bg-elevated);
  transition: all 0.3s ease;
}

.social-button--google:hover .social-icon {
  background: #db4437;
  color: white;
}

.social-button--github:hover .social-icon {
  background: #333;
  color: white;
}

.social-button--twitter:hover .social-icon {
  background: #1da1f2;
  color: white;
}

.social-text {
  font-weight: 600;
}

/* Register Link Styles */
.beauty-register {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1.5rem 0 0.5rem;
  border-top: 1px solid var(--color-border);
}

.register-text {
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

.register-action {
  font-weight: 600;
}

/* Error Styles */
.form-error {
  display: flex;
  align-items: center;
  color: var(--color-error);
  font-size: 0.75rem;
  font-weight: 500;
  margin-top: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: var(--color-error-soft);
  border-radius: 8px;
  border-left: 3px solid var(--color-error);
}

/* Адаптивность */
@media (max-width: 768px) {
  .login-container {
    padding: 1rem;
  }

  .login-card {
    padding: 2rem;
    margin: 1rem;
  }

  .login-title {
    font-size: 1.75rem;
  }

  .social-login {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .beauty-social {
    flex-direction: row;
    justify-content: flex-start;
    height: auto;
    padding: 0.75rem 1rem;
  }

  .beauty-register {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 1.5rem;
  }

  .login-title {
    font-size: 1.5rem;
  }

  .floating-input {
    height: 52px;
  }

  .beauty-button {
    height: 52px;
  }
}
</style>