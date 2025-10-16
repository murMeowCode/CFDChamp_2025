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
            <label for="last_name" class="form-label">Фамилия *</label>
            <input
              id="last_name"
              v-model="form.last_name"
              type="text"
              class="form-input"
              :class="{ 'form-input--error': errors.last_name }"
              placeholder="Иванов"
              required
            />
            <span v-if="errors.last_name" class="form-error">{{ errors.last_name }}</span>
          </div>

          <div class="form-group">
            <label for="first_name" class="form-label">Имя *</label>
            <input
              id="first_name"
              v-model="form.first_name"
              type="text"
              class="form-input"
              :class="{ 'form-input--error': errors.first_name }"
              placeholder="Иван"
              required
            />
            <span v-if="errors.first_name" class="form-error">{{ errors.first_name }}</span>
          </div>

          <div class="form-group">
            <label for="middle_Name" class="form-label">Отчество</label>
            <input
              id="middle_Name"
              v-model="form.middle_Name"
              type="text"
              class="form-input"
              :class="{ 'form-input--error': errors.middle_Name }"
              placeholder="Иванович"
            />
            <span v-if="errors.middle_Name" class="form-error">{{ errors.middle_Name }}</span>
          </div>
        </div>

        <!-- Основные поля -->
        <div class="form-group">
          <label for="username" class="form-label">Логин *</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="form-input"
            :class="{ 'form-input--error': errors.username }"
            placeholder="Придумайте логин"
            required
          />
          <span v-if="errors.username" class="form-error">{{ errors.username }}</span>
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

        <!-- Телефон и дата рождения в одной строке -->
        <div class="form-row">
          <div class="form-group">
            <label for="phone" class="form-label">Номер телефона *</label>
            <input
              id="phone"
              v-model="form.phone"
              type="tel"
              class="form-input"
              :class="{ 'form-input--error': errors.phone }"
              placeholder="+7 (999) 999-99-99"
              required
            />
            <span v-if="errors.phone" class="form-error">{{ errors.phone }}</span>
          </div>

          <div class="form-group">
            <label for="birth_Date" class="form-label">Дата рождения *</label>
            <input
              id="birth_Date"
              v-model="form.birth_Date"
              type="date"
              class="form-input"
              :class="{ 'form-input--error': errors.birth_Date }"
              required
            />
            <span v-if="errors.birth_Date" class="form-error">{{ errors.birth_Date }}</span>
          </div>
        </div>

        <!-- Адрес -->
        <div class="form-group">
          <label for="address" class="form-label">Адрес *</label>
          <input
            id="address"
            v-model="form.address"
            type="text"
            class="form-input"
            :class="{ 'form-input--error': errors.address }"
            placeholder="Город, улица, дом, квартира"
            required
          />
          <span v-if="errors.address" class="form-error">{{ errors.address }}</span>
        </div>

        <!-- Роль -->
        <div class="form-group">
          <label for="role" class="form-label">Роль *</label>
          <select
            id="role"
            v-model="form.role"
            class="form-input"
            :class="{ 'form-input--error': errors.role }"
            required
          >
            <option value="" disabled selected>Выберите роль</option>
            <option value="role1">Роль 1</option>
            <option value="role2">Роль 2</option>
            <option value="role3">Роль 3</option>
          </select>
          <span v-if="errors.role" class="form-error">{{ errors.role }}</span>
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
          <RouterLink :to="{ name: 'login' }" class="link link--primary">Войти</RouterLink>
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
  agreement: false
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

/* Стили для select */
select.form-input {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=US-ASCII,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 4 5'><path fill='%23666' d='M2 0L0 2h4zm0 5L0 3h4z'/></svg>");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 12px;
  padding-right: 40px;
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