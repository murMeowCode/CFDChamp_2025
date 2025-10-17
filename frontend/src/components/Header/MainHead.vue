<template>
  <header class="header">
    <div class="container">
      <!-- Логотип -->
      <div class="logo">
        <h1 class="logo-text">ЦФО</h1>
      </div>

      <!-- Правая часть: навигация + переключатель темы -->
      <div class="header-right">
        <nav class="nav">
          <RouterLink
            v-for="item in navItems"
            :key="item.route"
            :to="{ name: item.route }"
            class="nav-link"
            active-class="nav-link--active"
          >
            <i :class="item.icon" class="nav-icon"></i>
            <span class="nav-label">{{ item.label }}</span>
          </RouterLink>

          <!-- Динамическая иконка входа/профиля -->
          <RouterLink
            :to="{ name: isAuthenticated ? 'profile' : 'login' }"
            class="nav-link profile-link"
            active-class="nav-link--active"
          >
            <i :class="isAuthenticated ? 'pi pi-user' : 'pi pi-sign-in'" class="nav-icon"></i>
            <span class="nav-label">{{ isAuthenticated ? 'Профиль' : 'Войти' }}</span>
          </RouterLink>
        </nav>
        <ThemeToggle class="theme-toggle theme-toggle--desktop" />

        <!-- Кнопка для тестирования переключения (можно убрать в продакшене)
        <button 
          v-if="showDebugButton"
          @click="toggleAuth" 
          class="debug-button"
          title="Тест переключения авторизации"
        >
          <i class="pi pi-refresh"></i>
        </button> -->
      </div>

      <!-- Переключатель темы для мобильных -->
      <ThemeToggle class="theme-toggle--mobile" />

      <!-- Бургер-меню (только на мобильных) -->
      <button
        class="burger"
        @click="toggleMobileMenu"
        aria-label="Меню"
        :aria-expanded="isMobileMenuOpen"
      >
        <span class="burger-line"></span>
        <span class="burger-line"></span>
        <span class="burger-line"></span>
      </button>

      <!-- Мобильное меню -->
      <nav v-if="isMobileMenuOpen" class="nav-mobile" data-aos="flip-right">
        <RouterLink
          v-for="item in navItems"
          :key="item.route"
          :to="{ name: item.route }"
          class="nav-link"
          active-class="nav-link--active"
          @click="closeMobileMenu"
        >
          <i :class="item.icon" class="nav-icon"></i>
          <span class="nav-label">{{ item.label }}</span>
        </RouterLink>

        <!-- Динамическая иконка для мобильного меню -->
        <RouterLink
          :to="{ name: isAuthenticated ? 'profile' : 'login' }"
          class="nav-link profile-link"
          active-class="nav-link--active"
          @click="closeMobileMenu"
        >
          <i :class="isAuthenticated ? 'pi pi-user' : 'pi pi-sign-in'" class="nav-icon"></i>
          <span class="nav-label">{{
            isAuthenticated ? 'Личный кабинет' : 'Войти / Регистрация'
          }}</span>
        </RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import ThemeToggle from '../Theme/ThemeToggle.vue'
import { useUserStore } from '@/stores/useUserStore'
import { storeToRefs } from 'pinia'
// Состояние авторизации (в реальном приложении будет из store/auth)
const { getAuth: isAuthenticated } = storeToRefs(useUserStore())
// const isAuthenticated = ref(false)

// Навигационные пункты
const navItems = [
  {
    label: 'Главная',
    icon: 'pi pi-home',
    route: 'home',
  },
  {
    label: 'Первый',
    icon: 'pi pi-calendar',
    route: 'one',
  },
  {
    label: 'Второй',
    icon: 'pi pi-map',
    route: 'two',
  },
  {
    label: 'Третий',
    icon: 'pi pi-chart-bar',
    route: 'three',
  },
]

const isMobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

// Функция переключения авторизации для тестирования
const toggleAuth = () => {
  isAuthenticated.value = !isAuthenticated.value
  console.log(
    'Статус авторизации изменен:',
    isAuthenticated.value ? 'Авторизован' : 'Не авторизован',
  )
}

// Закрывать меню при изменении размера окна (если стало > 768px)
const handleResize = () => {
  if (window.innerWidth >= 768) {
    isMobileMenuOpen.value = false
  }
}

// Инициализация при загрузке
onMounted(() => {
  window.addEventListener('resize', handleResize)

  // Проверяем есть ли токен в localStorage (реальная логика)
  const token = localStorage.getItem('auth-token')
  if (token) {
    isAuthenticated.value = true
  }

  // Для демонстрации - автоматическое переключение каждые 5 секунд
  // setInterval(toggleAuth, 5000)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* === Контейнер шапки === */
.header {
  background: var(--color-bg-elevated);
  border-bottom: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 1000;
  backdrop-filter: var(--backdrop-blur);
  backdrop-saturate: var(--backdrop-saturate);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
  display: flex;
  align-items: center;
  justify-content: space-between;

  position: relative;
}

/* === Логотип === */
.logo {
  display: flex;
  align-items: center;
}

.logo-text {
  font-size: 1.875rem;
  font-weight: var(--font-weight-bold);
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.025em;
  line-height: 1;
  margin: 0;
}

/* === Правая часть: навигация + переключатель темы === */
.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

/* === Навигация === */
.nav {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.nav-link {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 64px;
  color: var(--color-text-muted);
  text-decoration: none;
  font-size: 0.75rem;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-normal);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-sm);
  border: 1px solid transparent;
}

.nav-icon {
  font-size: 1.25rem;
  margin-bottom: var(--spacing-xs);
  transition: all var(--transition-normal);
}

.nav-link:hover {
  color: var(--color-primary);
  background: var(--color-primary-soft);
  border-color: var(--color-primary-muted);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.nav-link:hover .nav-icon {
  transform: translateY(-2px) scale(1.1);
}

.nav-link--active {
  color: var(--color-primary);
  background: var(--color-primary-soft);
  border: 1px solid var(--color-primary-muted);
  box-shadow: var(--shadow-sm);
}

.nav-link--active .nav-icon {
  transform: translateY(-2px);
  filter: drop-shadow(0 2px 4px rgba(59, 130, 246, 0.2));
}

/* Специальные стили для иконки профиля/входа */
.profile-link {
  margin-left: var(--spacing-xs);
}

.profile-link .nav-icon {
  font-size: 1.3rem;
}

/* Кнопка отладки (только для разработки) */
.debug-button {
  background: var(--color-warning-soft);
  color: var(--color-warning);
  border: 1px solid var(--color-warning);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
}

.debug-button:hover {
  background: var(--color-warning);
  color: white;
  transform: scale(1.05);
}

.debug-button--mobile {
  width: 100%;
  height: 52px;
  margin-top: var(--spacing-md);
  gap: var(--spacing-sm);
}

/* === Мобильное меню === */
.nav-mobile {
  display: none;
}

/* === Переключатель темы для мобильных === */
.theme-toggle--mobile {
  display: none;
}

/* === Бургер-меню === */
.burger {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 32px;
  height: 24px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1001;
  transition: transform var(--transition-normal);
}

.burger:hover {
  transform: scale(1.05);
}

.burger-line {
  width: 100%;
  height: 2px;
  background: var(--color-text);
  border-radius: var(--border-radius-full);
  transition: all var(--transition-normal);
  transform-origin: center;
}

.burger[aria-expanded='true'] .burger-line:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
  background: var(--color-primary);
}

.burger[aria-expanded='true'] .burger-line:nth-child(2) {
  opacity: 0;
  transform: scale(0);
}

.burger[aria-expanded='true'] .burger-line:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
  background: var(--color-primary);
}

/* === Адаптивность === */
@media (max-width: 768px) {
  .container {
    height: 64px;
    padding: 0 var(--spacing-md);
  }

  .logo-text {
    font-size: 1.5rem;
  }

  /* Скрыть правую часть на мобильных */
  .header-right {
    display: none;
  }

  /* Показать переключатель темы для мобильных */
  .theme-toggle--mobile {
    display: block;
    margin-right: var(--spacing-md);
  }

  /* Скрыть переключатель темы в десктопной версии */
  .theme-toggle--desktop {
    display: none;
  }

  /* Показать бургер */
  .burger {
    display: flex;
  }

  /* Мобильное меню */
  .nav-mobile {
    display: flex;
    position: fixed;
    top: 0;
    right: 0;
    height: 100vh;
    width: 320px;
    max-width: 85vw;
    background: var(--color-bg-elevated);
    flex-direction: column;
    padding: 80px var(--spacing-md) var(--spacing-lg);
    gap: var(--spacing-xs);
    box-shadow: var(--shadow-xl);
    border-left: 1px solid var(--color-border);
    z-index: 999;
    overflow-y: auto;
    animation: slideInRight var(--transition-normal) ease-out;
  }

  .nav-link {
    width: 80%;
    height: 56px;
    flex-direction: row;
    justify-content: flex-start;
    padding: 0 var(--spacing-lg);
    gap: var(--spacing-md);
    font-size: 1rem;
    font-weight: var(--font-weight-medium);
    border-radius: var(--border-radius-md);
    border: 1px solid var(--color-border);
    margin-bottom: var(--spacing-xs);
  }

  .nav-link:hover {
    transform: translateX(4px);
  }

  .nav-icon {
    font-size: 1.125rem;
    margin-bottom: 0;
    width: 20px;
    text-align: center;
  }

  .nav-link--active {
    background: var(--color-primary-soft);
    border-color: var(--color-primary-muted);
    color: var(--color-primary);
  }

  /* Для мобильной версии иконка профиля */
  .profile-link {
    margin-left: 0;
    margin-top: var(--spacing-sm);
    background: var(--color-secondary-soft);
    border-color: var(--color-secondary-muted);
  }

  .profile-link.nav-link--active {
    background: var(--color-secondary-muted);
    border-color: var(--color-secondary);
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 var(--spacing-sm);
  }

  .logo-text {
    font-size: 1.375rem;
  }

  .nav-mobile {
    width: 280px;
  }

  .nav-link {
    padding: 0 var(--spacing-md);
    height: 52px;
  }
}

/* Анимация для мобильного меню */
@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Затемнение фона при открытом мобильном меню */
.nav-mobile::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: -1;
  opacity: 0;
  animation: fadeIn var(--transition-normal) ease-out forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}
</style>
