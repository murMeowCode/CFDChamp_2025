import { reactive } from 'vue'
export function useValidation() {
  const errors = reactive({
    last_name: '',
    first_name: '',
    username: '',
    email: '',
    phone: '',
    birth_Date: '',
    address: '',
    role: '',
    password: '',
    confirmPassword: ''
  })
  const formSubmitted = reactive({ value: false })

  const validateForm = (form) => {
    formSubmitted.value = true
    let isValid = true

    // Очистка предыдущих ошибок
    Object.keys(errors).forEach((key) => {
      errors[key] = ''
    })

    // Валидация ФИО
    if (!form.last_name?.trim()) {
      errors.last_name = 'Фамилия обязательна'
      isValid = false
    }

    if (!form.first_name?.trim()) {
      errors.first_name = 'Имя обязательно'
      isValid = false
    }

    // Валидация логина
    if (!form.username?.trim()) {
      errors.username = 'Логин обязателен'
      isValid = false
    } else if (form.username.length < 3) {
      errors.username = 'Логин должен содержать минимум 3 символа'
      isValid = false
    }

    // Валидация email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!form.email?.trim()) {
      errors.email = 'Email обязателен'
      isValid = false
    } else if (!emailRegex.test(form.email)) {
      errors.email = 'Введите корректный email'
      isValid = false
    }

    // Валидация телефона
    const phoneRegex = /^(\+7|8)?[\s\-]?\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$/
    if (!form.phone?.trim()) {
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
    if (!form.address?.trim()) {
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

  return {
    errors,
    formSubmitted,
    validateForm
  }
}