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
      <h1 class="user-name">{{ FIO }}</h1>
      <p class="user-profession">{{ Profession }}</p>
      <blockquote class="user-quote" v-if="Quote">"{{ Quote }}"</blockquote>
      <div class="level-badge">
        <span class="level-text">Уровень {{ Level }}</span>
        <div class="level-progress">
          <div class="progress-fill" :style="{ width: '65%' }"></div>
        </div>
      </div>
    </header>

    <!-- Персональная информация -->
    <section class="personal-info">
      <div class="section-header">
        <h2>Персональная информация</h2>
        <div class="edit-toggle" @click="toggleEdit">
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
            class="floating-input"
          />
          <label>Имя</label>
          <div class="input-decoration"></div>
        </div>

        <!-- Профессия -->
        <div class="form-group floating-label">
          <input
            :disabled="!isEditing"
            type="text"
            v-model="Profession"
            placeholder=" "
            class="floating-input"
          />
          <label>Профессия</label>
          <div class="input-decoration"></div>
        </div>

        <!-- Цитата -->
        <div class="form-group floating-label">
          <input
            :disabled="!isEditing"
            type="text"
            v-model="Quote"
            placeholder=" "
            class="floating-input"
          />
          <label>Цитата</label>
          <div class="input-decoration"></div>
        </div>

        <!-- Контакты -->
        <div class="form-group communication">
          <label class="section-label">Контакты</label>
          <div class="contacts-grid">
            <div v-for="(contact, index) in contacts" :key="index" class="contact-item">
              <div class="contact-item-content" v-if="isEditing">
                <div class="contact-type-badge">{{ contact.type }}</div>
                <input
                  v-model="contact.value"
                  :type="contact.type === 'email' ? 'email' : 'text'"
                  :placeholder="`Введите ${contact.type}`"
                  class="contact-input"
                />
                <button type="button" class="remove-contact-btn" @click="removeContact(index)">
                  🗑️
                </button>
              </div>
              <div v-else class="contact-display">
                <span class="contact-type">{{ contact.type }}:</span>
                <span class="contact-value">{{ contact.value }}</span>
              </div>
            </div>
          </div>

          <button
            v-if="isEditing"
            type="button"
            class="add-contact-btn"
            @click="showContactModal = true"
          >
            <span class="btn-icon">+</span>
            Добавить контакт
          </button>
        </div>

        <!-- Дата и пол -->
        <div class="form-row">
          <div class="form-group floating-label half-width">
            <input :disabled="!isEditing" type="date" v-model="BurthDay" class="floating-input" />
            <label>Дата рождения</label>
            <div class="input-decoration"></div>
          </div>

          <div class="form-group floating-label half-width">
            <select :disabled="!isEditing" v-model="selectedOption" class="floating-input">
              <option value="option1">Мужской</option>
              <option value="option2">Женский</option>
            </select>
            <label>Пол</label>
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
            class="floating-input"
          />
          <label>Адрес</label>
          <div class="input-decoration"></div>
        </div>

        <!-- О себе -->
        <div class="form-group floating-label">
          <textarea
            :disabled="!isEditing"
            v-model="AboutMe"
            placeholder=" "
            class="floating-input textarea"
          ></textarea>
          <label>О себе</label>
          <div class="input-decoration"></div>
        </div>
      </form>
    </section>

    <!-- Краткие данные -->
    <section class="summary-info">
      <div class="summary-header">
        <h2>Профиль</h2>
        <div class="online-status">
          <div class="status-dot"></div>
          <span>Online</span>
        </div>
      </div>

      <div class="profile-stats">
        <div class="stat-item">
          <div class="stat-value">{{ FIO.split(' ')[0] }}</div>
          <div class="stat-label">Имя</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ DateBirthday }}</div>
          <div class="stat-label">Дата рождения</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">@{{ NickName }}</div>
          <div class="stat-label">Никнейм</div>
        </div>
        <div class="stat-item">
          <div class="stat-value level-stat">{{ Level }}</div>
          <div class="stat-label">Уровень</div>
        </div>
      </div>

      <div class="achievements-section">
        <h3>Достижения</h3>
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

    <!-- Модальное окно для добавления контакта -->
    <div v-if="showContactModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3>Добавить контакт</h3>
        <div class="modal-form">
          <div class="form-group floating-label">
            <select v-model="newContactType" class="floating-input">
              <option value="email">Email</option>
              <option value="tel">Телефон</option>
              <option value="website">Сайт</option>
            </select>
            <label>Тип контакта</label>
            <div class="input-decoration"></div>
          </div>

          <div class="form-group floating-label">
            <input
              v-if="newContactType === 'email'"
              type="email"
              v-model="newContactValue"
              placeholder=" "
              class="floating-input"
            />
            <input
              v-else-if="newContactType === 'tel'"
              type="tel"
              v-model="newContactValue"
              placeholder=" "
              class="floating-input"
            />
            <input
              v-else-if="newContactType === 'website'"
              type="url"
              v-model="newContactValue"
              placeholder=" "
              class="floating-input"
            />
            <label>Значение</label>
            <div class="input-decoration"></div>
          </div>
        </div>

        <div class="modal-buttons">
          <button @click="addContact" :disabled="!newContactValue.trim()" class="btn-primary">
            Добавить
          </button>
          <button @click="closeModal" class="btn-secondary">Отмена</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import UserAchive from '../Achive/UserAchive.vue'

import { useUserStore } from '@/stores/useUserStore'
import ph1 from '@/components/CabinetComponents/img/Gori.jpg'
import ph2 from '@/components/CabinetComponents/img/TunTunTun.jpg'

const { getUser } = storeToRefs(useUserStore())

const FIO = `${getUser.value.last_name} ${getUser.value.first_name} ${getUser.value.middle_Name}`
const DateBirthday = getUser.value.birth_Date
const NickName = getUser.value.username
const Level = ref(1)

const Profession = getUser.value.role
const Quote = ref('user.Quote')
const Email = getUser.value.email
const Phone = getUser.value.phone
const BurthDay = getUser.value.birth_Date
const selectedOption = ref('Мужик')
const Address = getUser.value.address
const AboutMe = ref('zzzzzz')

import { useAchivesStore } from '@/stores/useAchivesStore'
import { storeToRefs } from 'pinia'

const Achives = useAchivesStore()

const isEditing = ref(false)

// Массив контактов для динамического управления
const contacts = ref([
  { type: 'email', value: Email.value },
  { type: 'tel', value: Phone.value },
])

const showContactModal = ref(false)
const newContactType = ref('email')
const newContactValue = ref('')

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

function addContact() {
  if (newContactValue.value.trim()) {
    contacts.value.push({
      type: newContactType.value,
      value: newContactValue.value.trim(),
    })
    closeModal()
  }
}

function closeModal() {
  showContactModal.value = false
  newContactType.value = 'email'
  newContactValue.value = ''
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
  background: linear-gradient(135deg, var(--color-bg-subtle) 0%, var(--color-bg-muted) 100%);
  border-right: 1px solid var(--color-border);
}

.bg-photo {
  position: relative;
  overflow: hidden;
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
  background: linear-gradient(to bottom, transparent 0%, var(--color-bg-subtle) 90%);
}

.avatar-container {
  position: relative;
  display: inline-block;
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
    0 0 0 4px var(--color-primary-soft);
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
  color: var(--color-text);
  background: linear-gradient(135deg, var(--color-text) 0%, var(--color-text-muted) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-family: var(--font-family-sans);
}

.user-profession {
  color: var(--color-text-muted);
  font-style: italic;
  margin: var(--spacing-xs) 0 var(--spacing-sm);
  font-size: 1.1rem;
  font-family: var(--font-family-sans);
}

.user-quote {
  font-style: italic;
  color: var(--color-text-muted);
  margin: 0 var(--spacing-xl) var(--spacing-lg);
  padding: var(--spacing-md);
  background: var(--color-bg-muted);
  border-radius: var(--border-radius-lg);
  border-left: 4px solid var(--color-primary);
  font-family: var(--font-family-sans);
}

.level-badge {
  background: var(--gradient-primary);
  color: var(--color-text-inverted);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-full);
  margin: 0 var(--spacing-lg);
  box-shadow: var(--shadow-md);
  font-family: var(--font-family-sans);
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
  font-family: var(--font-family-sans);
}

.edit-toggle {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-primary-soft);
  border: 1px solid var(--color-primary-muted);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
  font-weight: var(--font-weight-medium);
  font-family: var(--font-family-sans);
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
  font-family: var(--font-family-sans);
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
  font-family: var(--font-family-sans);
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
  background: var(--gradient-primary);
  transition: width var(--transition-normal);
}

.floating-input:focus ~ .input-decoration {
  width: 100%;
}

.textarea {
  min-height: 100px;
  resize: vertical;
}

/* Contacts */
.section-label {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin-bottom: var(--spacing-md);
  font-family: var(--font-family-sans);
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
  font-family: var(--font-family-sans);
}

.contact-input {
  flex: 1;
  border: none;
  background: transparent;
  color: var(--color-text);
  font-size: 0.9rem;
  font-family: var(--font-family-sans);
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
  font-family: var(--font-family-sans);
}

.remove-contact-btn:hover {
  background: var(--color-bg-muted);
}

.contact-display {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  font-family: var(--font-family-sans);
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
  font-family: var(--font-family-sans);
}

.add-contact-btn:hover {
  background: var(--color-primary-muted);
  border-style: solid;
}

.btn-icon {
  font-size: 1.2rem;
  font-weight: var(--font-weight-bold);
}

/* Summary Info */
.summary-info {
  width: 25%;
  padding: var(--spacing-2xl);
  background: linear-gradient(135deg, var(--color-bg-subtle) 0%, var(--color-bg-muted) 100%);
  border-left: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
}

.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
}

.summary-header h2 {
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  font-size: 1.5rem;
  font-family: var(--font-family-sans);
}

.online-status {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 0.9rem;
  color: var(--color-text-muted);
  font-family: var(--font-family-sans);
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
}

.stat-item {
  background: var(--color-bg);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-lg);
  text-align: center;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  transition: transform var(--transition-normal);
  font-family: var(--font-family-sans);
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
}

.achievements-section h3 {
  color: var(--color-text);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--spacing-md);
  font-size: 1.1rem;
  font-family: var(--font-family-sans);
}

.achievements-grid {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  max-height: 400px;
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
  font-family: var(--font-family-sans);
}

.achievement-item:hover {
  transform: translateX(4px);
  border-color: var(--color-primary-muted);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--color-bg);
  border-radius: var(--border-radius-2xl);
  padding: var(--spacing-2xl);
  width: 400px;
  max-width: 90vw;
  box-shadow: var(--shadow-2xl);
  border: 1px solid var(--color-border);
}

.modal-content h3 {
  margin: 0 0 var(--spacing-lg) 0;
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  text-align: center;
  font-family: var(--font-family-sans);
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.modal-buttons {
  display: flex;
  gap: var(--spacing-md);
  justify-content: flex-end;
}

.btn-primary,
.btn-secondary {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  border: none;
  transition: all var(--transition-normal);
  width: auto;
  margin: 0;
  font-family: var(--font-family-sans);
}

.btn-primary {
  background: var(--gradient-primary);
  color: var(--color-text-inverted);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-secondary {
  background: var(--color-bg-muted);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.btn-secondary:hover {
  background: var(--color-bg-subtle);
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
}
</style>
