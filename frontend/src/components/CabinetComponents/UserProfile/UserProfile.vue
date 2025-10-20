<template>
  <div class="main-panel">
    <!-- Заголовок профиля -->
    <header class="profile-header">
      <div class="bg-photo">
        <img :src="ph1" alt="Background Photo" />
        <div class="bg-overlay"></div>
      </div>
      <div class="avatar-photo">
        <img :src="ph2" alt="User Avatar" />
        <div class="avatar-status"></div>
      </div>
      <h1 class="user-name cyber-heading">{{ FIO }}</h1>
      <p class="user-profession futurism-elegant">{{ Profession }}</p>
      <blockquote class="user-quote futurism-elegant" v-if="Quote">"{{ Quote }}"</blockquote>
      <div class="level-badge">
        <span class="level-text cyber-mono">Уровень {{ Level }}</span>
        <div class="level-progress">
          <div class="progress-fill" :style="{ width: '65%' }"></div>
        </div>
      </div>

      <!-- Кнопка выхода -->
      <button class="logout-btn cyber-dynamic" @click="handleLogout">
        <span class="btn-icon">🚪</span>
        <span class="btn-text">Выйти</span>
      </button>
    </header>

    <!-- Персональная информация -->
    <section class="personal-info">
      <div class="section-header">
        <h2 class="cyber-heading">Персональная информация</h2>
        <div class="edit-toggle cyber-dynamic" @click="showModal">
          <span class="edit-icon">{{ isEditing ? '💾' : '✏️' }}</span>
          <span>{{ isEditing ? 'Сохранить' : 'Изменить' }}</span>
        </div>
      </div>

      <form @submit.prevent="toggleEdit" class="info-form">
        <!-- Имя -->
        <div class="form-group floating-label">
          <input
            :disabled="!isEditing"
            type="text"
            v-model="Name"
            placeholder=" "
            class="floating-input futurism-elegant"
          />
          <label class="cyber-dynamic">Имя</label>
          <div class="input-decoration"></div>
        </div>

        <!-- Профессия -->
        <div class="form-group floating-label">
          <input
            :disabled="!isEditing"
            type="text"
            v-model="Profession"
            placeholder=" "
            class="floating-input futurism-elegant"
          />
          <label class="cyber-dynamic">Профессия</label>
          <div class="input-decoration"></div>
        </div>

        <!-- Цитата -->
        <div class="form-group floating-label">
          <input
            :disabled="!isEditing"
            type="text"
            v-model="Quote"
            placeholder=" "
            class="floating-input futurism-elegant"
          />
          <label class="cyber-dynamic">Цитата</label>
          <div class="input-decoration"></div>
        </div>

        <!-- Контакты -->
        <div class="form-group communication">
          <label class="section-label cyber-dynamic">Контакты</label>
          <div class="contacts-grid">
            <div v-for="(contact, index) in contacts" :key="index" class="contact-item">
              <div class="contact-item-content" v-if="isEditing">
                <div class="contact-type-badge cyber-mono">{{ contact.type }}</div>
                <input
                  v-model="contact.value"
                  :type="contact.type === 'email' ? 'email' : 'text'"
                  :placeholder="`Введите ${contact.type}`"
                  class="contact-input futurism-elegant"
                />
                <button
                  type="button"
                  class="remove-contact-btn cyber-dynamic"
                  @click="removeContact(index)"
                >
                  🗑️
                </button>
              </div>
              <div v-else class="contact-display">
                <span class="contact-type cyber-dynamic">{{ contact.type }}:</span>
                <span class="contact-value futurism-elegant">{{ contact.value }}</span>
              </div>
            </div>
          </div>

          <button
            v-if="isEditing"
            type="button"
            class="add-contact-btn cyber-dynamic"
            @click="showContactModal = true"
          >
            <span class="btn-icon">+</span>
            Добавить контакт
          </button>
        </div>

        <!-- Дата и пол -->
        <div class="form-row">
          <div class="form-group floating-label half-width">
            <input
              :disabled="!isEditing"
              type="date"
              v-model="BurthDay"
              class="floating-input futurism-elegant"
            />
            <label class="cyber-dynamic">Дата рождения</label>
            <div class="input-decoration"></div>
          </div>
        </div>

        <!-- Адрес -->
        <div class="form-group floating-label">
          <input
            :disabled="!isEditing"
            type="text"
            v-model="Address"
            placeholder=" "
            class="floating-input futurism-elegant"
          />
          <label class="cyber-dynamic">Адрес</label>
          <div class="input-decoration"></div>
        </div>

        <!-- О себе -->
        <div class="form-group floating-label">
          <textarea
            :disabled="!isEditing"
            v-model="AboutMe"
            placeholder=" "
            class="floating-input textarea futurism-elegant"
          ></textarea>
          <label class="cyber-dynamic">О себе</label>
          <div class="input-decoration"></div>
        </div>
      </form>
    </section>

    <!-- Краткие данные -->
    <section class="summary-info">
      <div class="summary-header">
        <h2 class="cyber-heading">Профиль</h2>
        <div class="online-status cyber-dynamic">
          <div class="status-dot"></div>
          <span>Online</span>
        </div>
      </div>

      <div class="profile-stats">
        <div class="stat-item">
          <div class="stat-value cyber-mono">{{ FIO.split(' ')[0] }}</div>
          <div class="stat-label cyber-dynamic">Имя</div>
        </div>
        <div class="stat-item">
          <div class="stat-value cyber-mono">{{ DateBirthday }}</div>
          <div class="stat-label cyber-dynamic">Дата рождения</div>
        </div>
        <div class="stat-item">
          <div class="stat-value cyber-mono">@{{ NickName }}</div>
          <div class="stat-label cyber-dynamic">Логин</div>
        </div>
        <div class="stat-item">
          <div class="stat-value level-stat cyber-mono">{{ Level }}</div>
          <div class="stat-label cyber-dynamic">Уровень</div>
        </div>
      </div>

      <div class="achievements-section">
        <h3 class="cyber-heading">Достижения</h3>
        <div class="achievements-grid">
          <UserAchive
            v-for="(achive, index) in Achives.ACHIVES"
            :key="index"
            :Achive="achive"
            class="achievement-item"
          />
        </div>
      </div>
    </section>
    
    <DynamicDialog />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import UserAchive from '../Achive/UserAchive.vue'
import { useUserStore } from '@/stores/useUserStore'
import ph1 from '@/components/CabinetComponents/img/Gori.jpg'
import ph2 from '@/components/CabinetComponents/img/TunTunTun.jpg'
import { useAchivesStore } from '@/stores/useAchivesStore'
import { useDialogServices } from '@/utils/Dialog/useDialogServices'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import DynamicDialog from 'primevue/dynamicdialog'
import { useAuthStore } from '@/stores/useAuthStore'

const useAuStore = useAuthStore()
const useUsStore = useUserStore()
const router = useRouter()
const { getUser } = storeToRefs(useUserStore())
const { showUpdateEmailPhone } = useDialogServices()

const FIO = `${getUser.value.first_name} ${getUser.value.last_name} ${getUser.value.middle_name}`
const DateBirthday = getUser.value.birth_date
const NickName = getUser.value.username
const Level = ref(1)
const Name = getUser.value.last_name
const Profession = getUser.value.role
const Quote = ref('Мужчина')
const Email = getUser.value.email
const Phone = getUser.value.phone
const BurthDay = getUser.value.birth_date
const selectedOption = ref('Мужчина')
const Address = getUser.value.address
const AboutMe = ref('user.AboutMe')

const Achives = useAchivesStore()
const isEditing = ref(false)

// Массив контактов для динамического управления
const contacts = ref([
  { type: 'Почта', value: Email },
  { type: 'Телефон', value: Phone },
])

const showContactModal = ref(false)
const newContactType = ref('email')
const newContactValue = ref('')

async function showModal() {
  const result = showUpdateEmailPhone()

  if (result) {
    // Обрабатываем данные из диалога
    console.log('Полученные данные:', result)
    // { phone: '+79999999999', email: 'example@mail.com' }

    // Здесь можно отправить данные на сервер
    await submitContacts(result)
  }
}

const submitContacts = async (data) => {
  // Ваша логика отправки данных
  console.log('Отправка данных на сервер:', data)
}

function toggleEdit() {
  if (isEditing.value) {
    // Обновляем email и телефон из массива контактов при сохранении
    const emailContact = contacts.value.find((c) => c.type === 'email')
    const telContact = contacts.value.find((c) => c.type === 'tel')
    Email.value = emailContact ? emailContact.value : ''
    Phone.value = telContact ? telContact.value : ''
    alert('Данные сохранены!')
  }
  isEditing.value = !isEditing.value
}




function handleLogout() {
  // Здесь можно добавить логику выхода (очистка стора, токенов и т.д.)
  console.log('Выход из системы')
  useAuStore.removeToken()
  useUsStore.removeUser()
  router.push('/login') // Перенаправление на страницу входа
}
</script>

<style scoped>
.main-panel {
  height: 80vh;
  display: flex;
  margin: var(--spacing-xl) var(--spacing-2xl);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  box-shadow:
    0 10px 40px rgba(0, 0, 0, 0.1),
    0 2px 15px rgba(0, 0, 0, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius-2xl);
  overflow: hidden;
  font-family: var(--font-family-sans);
  color: var(--color-text);
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--color-border) transparent;
}

.main-panel::-webkit-scrollbar {
  width: 8px;
}

.main-panel::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 4px;
}

.main-panel::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 4px;
}

.main-panel::-webkit-scrollbar-thumb:hover {
  background: var(--color-border-hover);
}

/* Profile Header */
.profile-header {
  width: 25%;
  position: relative;
  text-align: center;
  padding-bottom: var(--spacing-xl);
  background: var(--color-bg-subtle);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bg-photo {
  position: relative;
  overflow: hidden;
  width: 100%;
}

.bg-photo img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  filter: brightness(0.8);
}

.bg-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--gradient-midnight);
  opacity: 0.3;
}

.avatar-photo {
  width: 140px;
  height: 140px;
  border-radius: var(--border-radius-full);
  overflow: hidden;
  border: 4px solid var(--color-bg);
  position: absolute;
  top: 120px;
  left: 50%;
  transform: translateX(-50%);
  box-shadow:
    var(--shadow-lg),
    0 0 0 4px var(--color-primary);
  z-index: 10;
}

.avatar-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-status {
  position: absolute;
  bottom: 12px;
  right: 12px;
  width: 24px;
  height: 24px;
  border-radius: var(--border-radius-full);
  background: var(--color-success);
  border: 3px solid var(--color-bg);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  z-index: 20;
  animation: status-pulse 2s infinite;
}

@keyframes status-pulse {
  0%,
  100% {
    transform: scale(1);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }
  50% {
    transform: scale(1.1);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.4);
  }
}

.user-name {
  margin-top: 100px;
  font-size: 1.8rem;
  font-weight: var(--font-weight-bold);
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.user-profession {
  color: var(--color-text-muted);
  font-style: italic;
  margin: var(--spacing-xs) 0 var(--spacing-sm);
  font-size: 1.1rem;
}

.user-quote {
  font-style: italic;
  color: var(--color-text-muted);
  margin: 0 var(--spacing-xl) var(--spacing-lg);
  padding: var(--spacing-md);
  background: var(--color-bg-muted);
  border-radius: var(--border-radius-lg);
  border-left: 4px solid var(--color-primary);
}

.level-badge {
  background: var(--gradient-primary);
  color: var(--color-text-inverted);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-full);
  margin: 0 var(--spacing-lg) var(--spacing-lg);
  box-shadow: var(--shadow-md);
}

.level-text {
  font-weight: var(--font-weight-semibold);
  font-size: 0.9rem;
}

.level-progress {
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  margin-top: var(--spacing-xs);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--color-text-inverted);
  border-radius: 2px;
  transition: width 0.3s ease;
}

/* Кнопка выхода */
.logout-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--color-error-soft);
  color: var(--color-error);
  border: 1px solid var(--color-error);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
  font-weight: var(--font-weight-medium);
  margin-top: auto;
  margin-bottom: var(--spacing-lg);
  width: calc(100% - var(--spacing-xl));
  justify-content: center;
}

.logout-btn:hover {
  background: var(--color-error);
  color: var(--color-text-inverted);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-icon {
  font-size: 1.2rem;
}

.btn-text {
  font-weight: var(--font-weight-semibold);
}

/* Personal Info */
.personal-info {
  padding: var(--spacing-2xl);
  width: 50%;
  background: var(--color-bg);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--color-primary);
}

.section-header h2 {
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  font-size: 1.5rem;
}

.edit-toggle {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  border: 1px solid var(--color-primary-muted);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
  font-weight: var(--font-weight-medium);
}

.edit-toggle:hover {
  background: var(--color-primary-muted);
  transform: translateY(-1px);
}

.edit-icon {
  font-size: 1.2rem;
}

/* Form Styles */
.info-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.form-row {
  display: flex;
  gap: var(--spacing-md);
}

.half-width {
  flex: 1;
}

.floating-label {
  position: relative;
  margin-bottom: 0;
}

.floating-input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-sm) var(--spacing-sm);
  border: none;
  border-bottom: 2px solid var(--color-border);
  background: transparent;
  font-size: 1rem;
  transition: all var(--transition-normal);
  color: var(--color-text);
}

.floating-input:focus {
  outline: none;
  border-bottom-color: var(--color-primary);
}

.floating-input:disabled {
  color: var(--color-text-muted);
  border-bottom-color: var(--color-border);
}

.floating-label label {
  position: absolute;
  top: var(--spacing-md);
  left: var(--spacing-sm);
  color: var(--color-text-muted);
  transition: all var(--transition-normal);
  pointer-events: none;
  font-weight: var(--font-weight-medium);
}

.floating-input:focus + label,
.floating-input:not(:placeholder-shown) + label {
  top: 0;
  font-size: 0.8rem;
  color: var(--color-primary);
}

.input-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--color-primary);
  transition: width var(--transition-normal);
}

.floating-input:focus ~ .input-decoration {
  width: 100%;
}

/* Стили для textarea */
.textarea {
  min-height: 40px;
  max-height: 200px;
  resize: none; /* Запрещаем изменение размера */
  overflow-y: auto; /* Добавляем скролл при необходимости */
  line-height: 1.4;
  padding-right: var(--spacing-md);
  transition: all var(--transition-normal);
}

/* Автоматическое увеличение высоты */
.textarea:focus {
  max-height: 150px; /* Увеличиваем максимальную высоту при фокусе */
}

/* Скрываем скроллбар для красоты */
.textarea::-webkit-scrollbar {
  width: 4px;
}

.textarea::-webkit-scrollbar-track {
  background: transparent;
}

.textarea::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 2px;
}

.textarea::-webkit-scrollbar-thumb:hover {
  background: var(--color-border-hover);
}

/* Для Firefox */
.textarea {
  scrollbar-width: thin;
  scrollbar-color: var(--color-border) transparent;
}

/* Делаем textarea визуально неотличимой от input */
.textarea.floating-input {
  padding-top: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border: none;
  border-bottom: 2px solid var(--color-border);
  background: transparent;
  font-family: inherit;
  font-size: 1rem;
}

.textarea.floating-input:focus {
  outline: none;
  border-bottom-color: var(--color-primary);
}

.textarea.floating-input:disabled {
  color: var(--color-text-muted);
  border-bottom-color: var(--color-border);
  background: transparent;
}
/* Contacts */
.section-label {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin-bottom: var(--spacing-md);
}

.contacts-grid {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.contact-item-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  background: var(--color-bg-muted);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border);
}

.contact-type-badge {
  padding: var(--spacing-xs) var(--spacing-sm);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  border-radius: var(--border-radius-full);
  font-size: 0.8rem;
  font-weight: var(--font-weight-semibold);
  min-width: 60px;
  text-align: center;
}

.contact-input {
  flex: 1;
  border: none;
  background: transparent;
  color: var(--color-text);
  font-size: 0.9rem;
}

.contact-input:focus {
  outline: none;
}

.remove-contact-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--spacing-xs);
  border-radius: var(--border-radius-full);
  transition: background var(--transition-fast);
  width: auto;
  margin: 0;
}

.remove-contact-btn:hover {
  background: var(--color-bg-muted);
}

.contact-display {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
}

.contact-type {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.contact-value {
  color: var(--color-text);
}

.add-contact-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  width: fit-content;
  background: var(--color-primary-soft);
  color: var(--color-primary);
  border: 1px dashed var(--color-primary-muted);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
  font-weight: var(--font-weight-medium);
  margin-top: var(--spacing-sm);
}

.add-contact-btn:hover {
  background: var(--color-primary-muted);
  border-style: solid;
}

/* Summary Info */
.summary-info {
  width: 25%;
  padding: var(--spacing-2xl);
  background: var(--color-bg-subtle);
  border-left: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  min-height: 0; /* Важно для корректной работы flex */
}

.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  flex-shrink: 0; /* Запрещаем сжатие */
}

.summary-header h2 {
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  font-size: 1.5rem;
}

.online-status {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 0.9rem;
  color: var(--color-text-muted);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: var(--border-radius-full);
  background: var(--color-success);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.profile-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-2xl);
  flex-shrink: 0; /* Запрещаем сжатие */
}

.stat-item {
  background: var(--color-bg);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-lg);
  text-align: center;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  transition: transform var(--transition-normal);
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-value {
  font-size: 1.2rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin-bottom: var(--spacing-xs);
}

.stat-value.level-stat {
  color: var(--color-primary);
}

.stat-label {
  font-size: 0.8rem;
  color: var(--color-text-muted);
  font-weight: var(--font-weight-medium);
}

.achievements-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0; /* Ключевое исправление - позволяет секции сжиматься */
  overflow: hidden; /* Скрываем переполнение */
}

.achievements-section h3 {
  color: var(--color-text);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--spacing-md);
  font-size: 1.1rem;
  flex-shrink: 0; /* Запрещаем сжатие заголовка */
}

.achievements-grid {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding-right: var(--spacing-xs);
}

.achievements-grid::-webkit-scrollbar {
  width: 4px;
}

.achievements-grid::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 2px;
}

.achievement-item {
  background: var(--color-bg);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border);
  transition: all var(--transition-normal);
  flex-shrink: 0; /* Запрещаем сжатие элементов */
}

.achievement-item:hover {
  transform: translateX(4px);
  border-color: var(--color-primary-muted);
}

/* Responsive */

@media (max-width: 1080px) {
  .main-panel {
    flex-direction: column;
    margin: var(--spacing-lg) var(--spacing-md);
    height: auto;
    min-height: 90vh;
  }

  .profile-header,
  .personal-info,
  .summary-info {
    width: 100% !important;
  }

  .profile-header {
    padding-bottom: var(--spacing-lg);
  }

  /* ФИКС ДЛЯ SUMMARY-INFO */
  .summary-info {
    padding: var(--spacing-lg);
    box-sizing: border-box;
    border-left: none;
    border-top: 1px solid var(--color-border);
    min-height: auto;
  }

  .profile-stats {
    grid-template-columns: repeat(4, 1fr);
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-lg);
  }

  .stat-item {
    padding: var(--spacing-sm);
    min-width: 0; /* Важно для ограничения ширины */
  }

  .stat-value {
    font-size: 1rem;
    word-break: break-word;
  }

  .stat-label {
    font-size: 0.75rem;
  }

  .achievements-section {
    min-width: 0; /* Предотвращает выход за границы */
    min-height: 200px; /* Фиксированная высота на мобильных */
  }

  .achievements-grid {
    max-height: 200px;
    min-width: 0;
  }

  /* ФИКС ДЛЯ ИНПУТОВ */
  .personal-info {
    padding: var(--spacing-lg);
    box-sizing: border-box;
  }

  .info-form {
    max-width: 100%;
    overflow: hidden;
  }

  .form-row {
    flex-direction: column;
    gap: var(--spacing-lg);
  }

  .half-width {
    width: 100%;
  }

  .floating-input {
    max-width: 100%;
    box-sizing: border-box;
  }

  input[type='date'].floating-input {
    min-width: auto;
    width: 100%;
  }

  select.floating-input {
    width: 100%;
  }

  .textarea {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
  }

  .section-header {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: flex-start;
  }

  .logout-btn {
    width: calc(100% - var(--spacing-lg));
    margin: var(--spacing-lg) auto;
  }
}

@media (max-width: 768px) {
  .summary-info {
    padding: var(--spacing-md);
  }

  .profile-stats {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-sm);
  }

  .stat-item {
    padding: var(--spacing-sm) var(--spacing-xs);
  }

  .stat-value {
    font-size: 0.9rem;
  }

  .stat-label {
    font-size: 0.7rem;
  }

  .achievements-grid {
    max-height: 150px;
  }

  .achievements-section h3 {
    font-size: 1rem;
    margin-bottom: var(--spacing-sm);
  }
}

@media (max-width: 480px) {
  .summary-info {
    padding: var(--spacing-sm);
  }

  .profile-stats {
    grid-template-columns: 1fr;
    gap: var(--spacing-xs);
  }

  .stat-item {
    padding: var(--spacing-xs);
  }

  .online-status {
    font-size: 0.8rem;
  }

  .summary-header h2 {
    font-size: 1.3rem;
  }

  .logout-btn {
    padding: var(--spacing-xs) var(--spacing-md);
    font-size: 0.9rem;
  }
}

/* КАСТОМНЫЕ СТИЛИ ДЛЯ DYNAMIC DIALOG ЗАТЕМНЕНИЯ */
:global(.p-dialog-mask) {
  background-color: rgba(0, 0, 0, 0.6) !important;
  backdrop-filter: blur(8px) !important;
}

:global(.p-dialog) {
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(255, 255, 255, 0.1) !important;
  border-radius: var(--border-radius-2xl) !important;
  border: 1px solid var(--color-border) !important;
}

:global(.p-dialog .p-dialog-header) {
  background: var(--color-bg-elevated) !important;
  border-top-left-radius: var(--border-radius-2xl) !important;
  border-top-right-radius: var(--border-radius-2xl) !important;
  border-bottom: 1px solid var(--color-border) !important;
  padding: var(--spacing-xl) !important;
}

:global(.p-dialog .p-dialog-content) {
  background: var(--color-bg) !important;
  border-bottom-left-radius: var(--border-radius-2xl) !important;
  border-bottom-right-radius: var(--border-radius-2xl) !important;
  padding: var(--spacing-xl) !important;
}

:global(.p-dialog .p-dialog-footer) {
  background: var(--color-bg-elevated) !important;
  border-bottom-left-radius: var(--border-radius-2xl) !important;
  border-bottom-right-radius: var(--border-radius-2xl) !important;
  border-top: 1px solid var(--color-border) !important;
  padding: var(--spacing-xl) !important;
}

:global(.p-dialog .p-dialog-header-icons) {
  display: flex !important;
  gap: var(--spacing-xs) !important;
}

:global(.p-dialog .p-dialog-header-icon) {
  width: 2rem !important;
  height: 2rem !important;
  border-radius: var(--border-radius-full) !important;
  border: none !important;
  background: var(--color-bg-muted) !important;
  color: var(--color-text) !important;
  transition: all var(--transition-normal) !important;
}

:global(.p-dialog .p-dialog-header-icon:hover) {
  background: var(--color-primary) !important;
  color: var(--color-text-inverted) !important;
  transform: scale(1.05) !important;
}

/* Анимация появления */
:global(.p-dialog-enter-active) {
  transition: all 0.3s ease-out !important;
}

:global(.p-dialog-enter-from) {
  opacity: 0 !important;
  transform: scale(0.9) translateY(-20px) !important;
}

:global(.p-dialog-enter-to) {
  opacity: 1 !important;
  transform: scale(1) translateY(0) !important;
}

:global(.p-dialog-leave-active) {
  transition: all 0.2s ease-in !important;
}

:global(.p-dialog-leave-from) {
  opacity: 1 !important;
  transform: scale(1) translateY(0) !important;
}

:global(.p-dialog-leave-to) {
  opacity: 0 !important;
  transform: scale(0.9) translateY(-20px) !important;
}
</style>