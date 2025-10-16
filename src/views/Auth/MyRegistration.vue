<template>
  <div class="register-container">
    <div class="register-card">
      <!-- Заголовок -->
      <div class="register-header">
        <div class="logo-wrapper">
          <i class="pi pi-user-plus"></i>
        </div>
        <h1 class="register-title">Регистрация</h1>
        <p class="register-subtitle">Заполните форму для регистрации</p>
      </div>

      <!-- Форма регистрации -->
      <form @submit.prevent="handleSubmit" class="register-form">
        <!-- ФИО - в одной строке -->
        <div class="form-row form-row--three">
          <div class="form-group floating-group">
            <div class="input-container">
              <input
                id="last_name"
                v-model="form.last_name"
                type="text"
                class="form-input floating-input"
                :class="{
                  'form-input--error': errors.last_name,
                  'form-input--filled': form.last_name,
                }"
                placeholder=" "
                required
              />
              <label for="last_name" class="floating-label">
                <i class="pi pi-id-card"></i>
                Фамилия
              </label>
              <div class="input-decoration"></div>
            </div>
            <span v-if="errors.last_name" class="form-error">
              <i class="pi pi-exclamation-circle"></i>
              {{ errors.last_name }}
            </span>
          </div>

          <div class="form-group floating-group">
            <div class="input-container">
              <input
                id="first_name"
                v-model="form.first_name"
                type="text"
                class="form-input floating-input"
                :class="{
                  'form-input--error': errors.first_name,
                  'form-input--filled': form.first_name,
                }"
                placeholder=" "
                required
              />
              <label for="first_name" class="floating-label">
                <i class="pi pi-user"></i>
                Имя
              </label>
              <div class="input-decoration"></div>
            </div>
            <span v-if="errors.first_name" class="form-error">
              <i class="pi pi-exclamation-circle"></i>
              {{ errors.first_name }}
            </span>
          </div>

          <div class="form-group floating-group">
            <div class="input-container">
              <input
                id="middle_Name"
                v-model="form.middle_Name"
                type="text"
                class="form-input floating-input"
                :class="{
                  'form-input--error': errors.middle_Name,
                  'form-input--filled': form.middle_Name,
                }"
                placeholder=" "
              />
              <label for="middle_Name" class="floating-label">
                <i class="pi pi-users"></i>
                Отчество
              </label>
              <div class="input-decoration"></div>
            </div>
            <span v-if="errors.middle_Name" class="form-error">
              <i class="pi pi-exclamation-circle"></i>
              {{ errors.middle_Name }}
            </span>
          </div>
        </div>

        <!-- Основные поля -->
        <div class="form-group floating-group">
          <div class="input-container">
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-input floating-input"
              :class="{
                'form-input--error': errors.username,
                'form-input--filled': form.username,
              }"
              placeholder=" "
              required
            />
            <label for="username" class="floating-label">
              <i class="pi pi-at"></i>
              Логин
            </label>
            <div class="input-decoration"></div>
          </div>
          <span v-if="errors.username" class="form-error">
            <i class="pi pi-exclamation-circle"></i>
            {{ errors.username }}
          </span>
        </div>

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
            />
            <label for="email" class="floating-label">
              <i class="pi pi-envelope"></i>
              Email
            </label>
            <div class="input-decoration"></div>
          </div>
          <span v-if="errors.email" class="form-error">
            <i class="pi pi-exclamation-circle"></i>
            {{ errors.email }}
          </span>
        </div>

        <!-- Телефон и дата рождения в одной строке -->
        <div class="form-row form-row--two">
          <div class="form-group floating-group">
            <div class="input-container">
              <input
                id="phone"
                v-model="form.phone"
                type="tel"
                class="form-input floating-input"
                :class="{
                  'form-input--error': errors.phone,
                  'form-input--filled': form.phone,
                }"
                placeholder=" "
                required
              />
              <label for="phone" class="floating-label">
                <i class="pi pi-phone"></i>
                Телефон
              </label>
              <div class="input-decoration"></div>
            </div>
            <span v-if="errors.phone" class="form-error">
              <i class="pi pi-exclamation-circle"></i>
              {{ errors.phone }}
            </span>
          </div>

          <div class="form-group floating-group">
            <div class="input-container">
              <input
                id="birth_Date"
                v-model="form.birth_Date"
                type="date"
                class="form-input floating-input"
                :class="{
                  'form-input--error': errors.birth_Date,
                  'form-input--filled': form.birth_Date,
                }"
                placeholder=" "
                required
              />
              <label for="birth_Date" class="floating-label">
                <i class="pi pi-calendar"></i>
                Дата рождения
              </label>
              <div class="input-decoration"></div>
            </div>
            <span v-if="errors.birth_Date" class="form-error">
              <i class="pi pi-exclamation-circle"></i>
              {{ errors.birth_Date }}
            </span>
          </div>
        </div>

        <!-- Адрес -->
        <div class="form-group floating-group">
          <div class="input-container">
            <input
              id="address"
              v-model="form.address"
              type="text"
              class="form-input floating-input"
              :class="{
                'form-input--error': errors.address,
                'form-input--filled': form.address,
              }"
              placeholder=" "
              required
            />
            <label for="address" class="floating-label">
              <i class="pi pi-map-marker"></i>
              Адрес
            </label>
            <div class="input-decoration"></div>
          </div>
          <span v-if="errors.address" class="form-error">
            <i class="pi pi-exclamation-circle"></i>
            {{ errors.address }}
          </span>
        </div>

        <!-- Роль - чекбоксы -->
        <div class="form-group">
          <label class="roles-label">
            <i class="pi pi-briefcase"></i>
            Роль *
          </label>
          <div class="roles-container">
            <div 
              v-for="role in roles" 
              :key="role.value"
              class="role-checkbox-wrapper"
            >
              <input
                :id="`role-${role.value}`"
                v-model="form.role"
                type="radio"
                name="role"
                :value="role.value"
                class="role-checkbox-input"
                @change="onRoleChange"
              />
              <label 
                :for="`role-${role.value}`" 
                class="role-checkbox-label"
                :class="{ 'role-checkbox-label--selected': form.role === role.value }"
              >
                <div class="role-checkbox-decoration">
                  <i class="pi pi-check"></i>
                </div>
                <div class="role-content">
                  <div class="role-title">{{ role.title }}</div>
                </div>
              </label>
            </div>
          </div>
          <span v-if="errors.role" class="form-error">
            <i class="pi pi-exclamation-circle"></i>
            {{ errors.role }}
          </span>
        </div>

        <!-- Пароли -->
        <div class="form-row form-row--two">
          <div class="form-group floating-group">
            <div class="input-container">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input floating-input"
                :class="{
                  'form-input--error': errors.password,
                  'form-input--filled': form.password,
                }"
                placeholder=" "
                required
              />
              <label for="password" class="floating-label">
                <i class="pi pi-lock"></i>
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
            <span v-if="errors.password" class="form-error">
              <i class="pi pi-exclamation-circle"></i>
              {{ errors.password }}
            </span>
          </div>

          <div class="form-group floating-group">
            <div class="input-container">
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                class="form-input floating-input"
                :class="{
                  'form-input--error': errors.confirmPassword,
                  'form-input--filled': form.confirmPassword,
                }"
                placeholder=" "
                required
              />
              <label for="confirmPassword" class="floating-label">
                <i class="pi pi-shield"></i>
                Подтверждение
              </label>
              <div class="input-decoration"></div>

              <button
                type="button"
                class="password-toggle beauty-toggle"
                @click="showConfirmPassword = !showConfirmPassword"
                :aria-label="showConfirmPassword ? 'Скрыть пароль' : 'Показать пароль'"
              >
                <i :class="showConfirmPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
              </button>
            </div>
            <span v-if="errors.confirmPassword" class="form-error">
              <i class="pi pi-exclamation-circle"></i>
              {{ errors.confirmPassword }}
            </span>
          </div>
        </div>

        <!-- Соглашение -->
        <div class="form-options">
          <div class="beauty-checkbox">
            <input
              id="agreement"
              v-model="form.agreement"
              type="checkbox"
              class="checkbox-input"
              required
            />
            <label for="agreement" class="checkbox-label">
              <div class="checkbox-decoration">
                <i class="pi pi-check"></i>
              </div>
              <span class="checkbox-text">
                Я соглашаюсь с
                <a href="#" class="beauty-link">условиями использования</a>
                и
                <a href="#" class="beauty-link">политикой конфиденциальности</a>
              </span>
            </label>
          </div>
          <span v-if="!form.agreement && formSubmitted" class="form-error">
            <i class="pi pi-exclamation-circle"></i>
            Необходимо принять условия
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
            <i class="pi pi-user-plus"></i>
            Создать аккаунт
          </span>
          <div v-else class="loading-spinner">
            <div class="spinner-circle"></div>
            <span>Регистрируем...</span>
          </div>
        </button>

        <!-- Ссылка на вход -->
        <div class="login-link beauty-login">
          <span class="login-text">Уже есть аккаунт?</span>
          <RouterLink :to="{ name: 'login' }" class="login-action beauty-link">
            <i class="pi pi-sign-in"></i>
            Войти в систему
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { RouterLink } from 'vue-router'

// Список ролей
const roles = [
  {
    value: 'role1',
    title: 'Роль 1',
    description: 'Базовый доступ'
  },
  {
    value: 'role2', 
    title: 'Роль 2',
    description: 'Расширенный доступ'
  },
  {
    value: 'role3',
    title: 'Роль 3', 
    description: 'Полный доступ'
  }
]

// Состояние формы
const form = reactive({
  last_name: '',
  first_name: '',
  middle_Name: '',
  username: '',
  email: '',
  birth_Date: '',
  phone: '',
  address: '',
  role: '',
  password: '',
  confirmPassword: '',
  agreement: false,
})

// Ошибки валидации
const errors = reactive({
  last_name: '',
  first_name: '',
  middle_Name: '',
  username: '',
  email: '',
  birth_Date: '',
  phone: '',
  address: '',
  role: '',
  password: '',
  confirmPassword: '',
})

// Состояние UI
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isSubmitting = ref(false)
const formSubmitted = ref(false)

// Обработчик изменения роли
const onRoleChange = () => {
  console.log('Выбрана роль:', form.role)
}

// Валидация формы
const validateForm = () => {
  formSubmitted.value = true
  let isValid = true

  // Очистка предыдущих ошибок
  Object.keys(errors).forEach((key) => {
    errors[key] = ''
  })

  // Валидация ФИО
  if (!form.last_name.trim()) {
    errors.last_name = 'Фамилия обязательна'
    isValid = false
  }

  if (!form.first_name.trim()) {
    errors.first_name = 'Имя обязательно'
    isValid = false
  }

  // Валидация логина
  if (!form.username.trim()) {
    errors.username = 'Логин обязателен'
    isValid = false
  } else if (form.username.length < 3) {
    errors.username = 'Логин должен содержать минимум 3 символа'
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

  // Валидация телефона
  const phoneRegex = /^(\+7|8)?[\s\-]?\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$/
  if (!form.phone.trim()) {
    errors.phone = 'Номер телефона обязателен'
    isValid = false
  } else if (!phoneRegex.test(form.phone.replace(/\s/g, ''))) {
    errors.phone = 'Введите корректный номер телефона'
    isValid = false
  }

  // Валидация даты рождения
  if (!form.birth_Date) {
    errors.birth_Date = 'Дата рождения обязательна'
    isValid = false
  } else {
    const birth_Date = new Date(form.birth_Date)
    const today = new Date()
    const minDate = new Date()
    minDate.setFullYear(today.getFullYear() - 100)

    if (birth_Date > today) {
      errors.birth_Date = 'Дата рождения не может быть в будущем'
      isValid = false
    } else if (birth_Date < minDate) {
      errors.birth_Date = 'Проверьте корректность даты рождения'
      isValid = false
    }
  }

  // Валидация адреса
  if (!form.address.trim()) {
    errors.address = 'Адрес обязателен'
    isValid = false
  } else if (form.address.length < 5) {
    errors.address = 'Адрес должен содержать минимум 5 символов'
    isValid = false
  }

  // Валидация роли
  if (!form.role) {
    errors.role = 'Выберите роль'
    isValid = false
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

  // Соглашение
  if (!form.agreement) {
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
    await new Promise((resolve) => setTimeout(resolve, 2000))

    // Здесь будет реальный API вызов
    console.log('Форма отправлена:', {
      ...form,
      // Не логируем реальный пароль
    })

    // Успешная регистрация
    alert('Регистрация успешно завершена!')

    // Сброс формы
    Object.keys(form).forEach((key) => {
      if (key !== 'agreement') {
        form[key] = ''
      }
    })
    form.agreement = false
    formSubmitted.value = false
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
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: linear-gradient(135deg, var(--color-bg-muted) 0%, var(--color-primary-soft) 100%);
}

.register-card {
  background: var(--color-bg-elevated);
  border-radius: 16px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 800px;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.register-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradient-primary);
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-wrapper {
  margin-bottom: 0.75rem;
}

.logo-wrapper i {
  font-size: 2rem;
  color: var(--color-primary);
}

.register-title {
  font-size: 2.5rem;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 0.5rem;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.register-subtitle {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 1.1rem;
  font-weight: 400;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

/* Form Layout */
.form-row--three {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0.5rem;
}

.form-row--two {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.form-group {
  position: relative;
}

/* Floating Label Styles */
.floating-group {
  position: relative;
}

.input-container {
  position: relative;
}

.form-input {
  padding: 1.5rem 0.75rem 0.5rem 0.75rem;
  border: 1.5px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-bg);
  color: var(--color-text);
  font-size: 1rem;
  transition: all 0.2s ease;
  outline: none;
  width: 100%;
  height: 40px;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: var(--color-primary);
  background: var(--color-bg-elevated);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.form-input--filled {
  border-color: var(--color-primary-muted);
}

.form-input--error {
  border-color: var(--color-error);
  background: var(--color-error-soft);
}

/* Плавающая метка */
.floating-label {
  position: absolute;
  top: 50%;
  left: 0.75rem;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  font-size: 0.8rem;
  font-weight: 400;
  pointer-events: none;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.floating-label i {
  font-size: 0.8rem;
  opacity: 0.7;
}

.form-input:focus + .floating-label,
.form-input--filled + .floating-label {
  top: 0.5rem;
  transform: none;
  font-size: 0.75rem;
  color: var(--color-primary);
  font-weight: 500;
}

.input-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--gradient-primary);
  transform: scaleX(0);
  transition: transform 0.2s ease;
}

.form-input:focus ~ .input-decoration {
  transform: scaleX(1);
}

/* Стили для выбора роли */
.roles-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text);
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.75rem;
}

.roles-label i {
  font-size: 0.8rem;
  opacity: 0.7;
}

.roles-container {
  display: flex;
  flex-direction: row;
  width:100%;
  justify-content:space-between;
  gap: 0.5rem;
}

.role-checkbox-wrapper {
  position: relative;
  width:100%;
}

.role-checkbox-input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.role-checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  border: 1.5px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-bg);
  color: var(--color-text);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.role-checkbox-label:hover {
  border-color: var(--color-primary-muted);
  background: var(--color-bg-elevated);
  transform: translateY(-1px);
}

.role-checkbox-label--selected {
  border-color: var(--color-primary);
  background: linear-gradient(135deg, var(--color-bg-elevated) 0%, var(--color-primary-soft) 100%);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.role-checkbox-label--selected::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-primary);
}

.role-checkbox-decoration {
  width: 20px;
  height: 20px;
  border: 1.5px solid var(--color-border);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  background: var(--color-bg);
  flex-shrink: 0;
  margin-top: 0.1rem;
}

.role-checkbox-label--selected .role-checkbox-decoration {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.role-checkbox-label--selected .role-checkbox-decoration i {
  transform: scale(1);
}

.role-checkbox-decoration i {
  font-size: 0.7rem;
  transform: scale(0);
  transition: transform 0.3s ease;
}

.role-content {
  flex: 1;
}

.role-title {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--color-text);
  margin-bottom: 0.25rem;
}

.role-checkbox-label--selected .role-title {
  color: var(--color-primary);
}

.role-description {
  font-size: 0.8rem;
  color: var(--color-text-muted);
  line-height: 1.3;
}

/* Анимация при выборе */
.role-checkbox-label {
  animation: fadeInUp 0.3s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Password Toggle */
.beauty-toggle {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.beauty-toggle:hover {
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

/* Checkbox Styles */
.form-options {
  margin: 1rem 0;
}

.beauty-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.checkbox-input {
  display: none;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.checkbox-decoration {
  width: 16px;
  height: 16px;
  border: 1.5px solid var(--color-border);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  background: var(--color-bg);
  flex-shrink: 0;
  margin-top: 0.1rem;
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
  font-size: 0.7rem;
  transform: scale(0);
  transition: transform 0.2s ease;
}

.checkbox-text {
  color: var(--color-text);
  font-size: 0.8rem;
  font-weight: 400;
  line-height: 1.3;
}

/* Button Styles */
.beauty-button {
  background: var(--gradient-primary);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 44px;
  margin-top: 0.5rem;
  position: relative;
  overflow: hidden;
}

.beauty-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid white;
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

/* Links */
.beauty-link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
}

.beauty-link:hover {
  color: var(--color-primary-hover);
}

.beauty-link i {
  font-size: 0.7rem;
}

/* Login Link */
.beauty-login {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 0 0;
  border-top: 1px solid var(--color-border);
  margin-top: 1rem;
}

.login-text {
  color: var(--color-text-muted);
  font-size: 0.8rem;
}

.login-action {
  font-weight: 500;
}

/* Error Styles */
.form-error {
  display: flex;
  align-items: center;
  color: var(--color-error);
  font-size: 0.7rem;
  font-weight: 400;
  margin-top: 0.25rem;
  padding: 0.25rem 0.5rem;
  background: var(--color-error-soft);
  border-radius: 4px;
  border-left: 2px solid var(--color-error);
  gap: 0.25rem;
}

.form-error i {
  font-size: 0.65rem;
}

/* Адаптивность */
@media (max-width: 768px) {
  .register-container {
    padding: 0.5rem;
  }

  .register-card {
    padding: 1.5rem;
    margin: 0.5rem;
  }

  .register-title {
    font-size: 1.25rem;
  }

  .form-row--three,
  .form-row--two {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .beauty-login {
    flex-direction: column;
    gap: 0.25rem;
    text-align: center;
  }

  .floating-input {
    height: 42px;
    font-size: 0.85rem;
  }

  .beauty-button {
    height: 42px;
    font-size: 0.85rem;
  }

  .roles-container {
    gap: 0.375rem;
  }
  
  .role-checkbox-label {
    padding: 0.75rem;
  }
  
  .role-title {
    font-size: 0.85rem;
  }
  
  .role-description {
    font-size: 0.75rem;
  }
}

@media (max-width: 480px) {
  .register-card {
    padding: 1rem;
    border-radius: 12px;
  }

  .register-title {
    font-size: 1.1rem;
  }

  .register-subtitle {
    font-size: 0.8rem;
  }

  .register-form {
    gap: 1rem;
  }

  .role-checkbox-label {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .role-checkbox-decoration {
    align-self: flex-start;
  }
}

input[type='date']:invalid::-webkit-datetime-edit {
  color: transparent;
}

input[type='date']:focus::-webkit-datetime-edit,
input[type='date']:valid::-webkit-datetime-edit {
  color: var(--color-text);
}

/* Для Firefox */
input[type='date']:invalid {
  color: transparent;
}

input[type='date']:focus,
input[type='date']:valid {
  color: var(--color-text);
}
</style>