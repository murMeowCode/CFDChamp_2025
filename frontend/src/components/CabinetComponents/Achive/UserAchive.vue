<template>
    <div class="UserAchivesMainPanel">
        <div class="Photo">
            <img :src="ph2" alt=""></img>
        </div>
        <div class="AchiveText">
            {{ Achive.text }}
        </div>
        <div class="AchiveProcent" :class="{ completed: Achive.procent === 100 }">
            <div class="progress-circle" v-if="Achive.procent < 100">
                <span class="progress-text">{{ Achive.procent }}%</span>
            </div>
            <div class="checkmark-container" v-else>
                <svg class="checkmark" viewBox="0 0 52 52">
                    <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
                    <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                </svg>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
import ph2 from '@/components/CabinetComponents/img/TunTunTun.jpg'

const props = defineProps({
    Achive: Object,
})
</script>

<style scoped>
.UserAchivesMainPanel {
  display: flex;
  align-items: center;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-xl);
  margin-bottom: var(--spacing-sm);
  height: 140px;
  padding: 0 var(--spacing-md);
  box-sizing: border-box;
  gap: var(--spacing-md);
  background: var(--color-bg);
  box-shadow: 
    var(--shadow-sm),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.UserAchivesMainPanel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    var(--color-primary-soft) 50%, 
    transparent 100%);
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.UserAchivesMainPanel:hover {
  border-color: var(--color-primary-muted);
  box-shadow: 
    var(--shadow-md),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.UserAchivesMainPanel:hover::before {
  opacity: 1;
}

.Photo {
  position: relative;
}

.Photo img {
  border-radius: var(--border-radius-full);
  width: 50px;
  height: 50px;
  object-fit: cover;
  border: 2px solid var(--color-bg-muted);
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all var(--transition-normal);
}

.UserAchivesMainPanel:hover .Photo img {
  border-color: var(--color-primary-muted);
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

/* Контейнер для текста — занимает оставшееся пространство и центрируется */
.AchiveText {
  flex: 1;
  text-align: center;
  font-size: 0.9rem;
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  user-select: none;
  font-family: var(--font-family-sans);
  transition: color var(--transition-normal);
}

.UserAchivesMainPanel:hover .AchiveText {
  color: var(--color-text);
}

/* Контейнер процентов — заменен на красивую галочку */
.AchiveProcent {
  min-width: 55px;
  height: 55px;
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
  position: relative;
}

/* Прогресс-круг для незавершенных достижений */
.progress-circle {
  width: 100%;
  height: 100%;
  background: var(--color-bg-muted);
  border-radius: var(--border-radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 
    var(--shadow-md),
    0 0 0 2px var(--color-bg),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all var(--transition-normal);
}

.progress-text {
  font-weight: var(--font-weight-bold);
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  transition: all var(--transition-normal);
}

/* Контейнер для галочки */
.checkmark-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-full);
  background: var(--color-success);
  box-shadow: 
    var(--shadow-md),
    0 0 0 2px var(--color-bg),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

/* Анимация галочки */
.checkmark {
  width: 60%;
  height: 60%;
  border-radius: 50%;
  display: block;
  stroke-width: 2;
  stroke: var(--color-text-inverted);
  stroke-miterlimit: 10;
  animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
}

.checkmark-circle {
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  stroke-width: 2;
  stroke-miterlimit: 10;
  stroke: var(--color-text-inverted);
  fill: none;
  animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.checkmark-check {
  transform-origin: 50% 50%;
  stroke-dasharray: 48;
  stroke-dashoffset: 48;
  animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
}

/* Анимации */
@keyframes stroke {
  100% {
    stroke-dashoffset: 0;
  }
}

@keyframes scale {
  0%, 100% {
    transform: none;
  }
  50% {
    transform: scale3d(1.1, 1.1, 1);
  }
}

@keyframes fill {
  100% {
    box-shadow: inset 0px 0px 0px 30px var(--color-success);
  }
}

/* Эффекты при наведении */
.UserAchivesMainPanel:hover .progress-circle {
  background: var(--color-bg-muted-hover);
  box-shadow: 
    var(--shadow-lg),
    0 0 0 2px var(--color-bg),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.UserAchivesMainPanel:hover .progress-text {
  color: var(--color-text);
}

.UserAchivesMainPanel:hover .checkmark-container {
  box-shadow: 
    var(--shadow-lg),
    0 0 0 2px var(--color-bg),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

/* Анимация пульсации для завершенных достижений */
@keyframes completed-pulse {
  0%, 100% {
    box-shadow: 
      var(--shadow-md),
      0 0 0 2px var(--color-bg),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }
  50% {
    box-shadow: 
      0 0 20px rgba(66, 185, 131, 0.6),
      0 0 0 2px var(--color-bg),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }
}

.AchiveProcent.completed .checkmark-container {
  animation: completed-pulse 2s ease-in-out infinite;
}

/* Мобильные устройства */
@media (max-width: 1080px) {
  .UserAchivesMainPanel {
    height: 60px;
    padding: 0 var(--spacing-sm);
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-xs);
  }

  .Photo img {
    width: 25px;
    height: 25px;
    border-width: 1.5px;
  }

  .AchiveText {
    font-size: 0.8rem;
    text-align: left;
    padding: 0 var(--spacing-xs);
    word-break: break-word;
    line-height: 1.2;
    display: flex;
    align-items: center;
  }

  .AchiveProcent {
    min-width: 35px;
    height: 35px;
  }

  .progress-text {
    font-size: 0.7rem;
  }
}

@media (max-width: 768px) {
  .UserAchivesMainPanel {
    height: 60px;
    padding: 0 var(--spacing-sm);
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-xs);
  }

  .Photo img {
    width: 25px;
    height: 25px;
    border-width: 1.5px;
  }

  .AchiveText {
    font-size: 0.8rem;
    text-align: left;
    padding: 0 var(--spacing-xs);
    word-break: break-word;
    line-height: 1.2;
    display: flex;
    align-items: center;
  }

  .AchiveProcent {
    min-width: 45px;
    height: 45px;
  }
}

/* Очень маленькие экраны */
@media (max-width: 480px) {
  .UserAchivesMainPanel {
    height: 55px;
    padding: 0 var(--spacing-xs);
    gap: var(--spacing-xs);
  }

  .Photo img {
    width: 35px;
    height: 35px;
    border-width: 1px;
  }

  .AchiveText {
    font-size: 0.75rem;
    padding: 0 8px;
  }

  .AchiveProcent {
    min-width: 25px;
    height: 25px;
  }

  .progress-text {
    font-size: 0.65rem;
  }

  /* Убираем некоторые эффекты на очень маленьких экранах для производительности */
  .UserAchivesMainPanel:hover {
    transform: none;
  }
  
  .UserAchivesMainPanel:hover .Photo img {
    transform: none;
  }
  
  .UserAchivesMainPanel:hover .AchiveProcent {
    transform: none;
  }
}

/* Горизонтальная ориентация на мобильных */
@media (max-width: 768px) and (orientation: landscape) {
  .UserAchivesMainPanel {
    height: 50px;
  }
  
  .Photo img {
    width: 15px;
    height: 15px;
  }
  
  .AchiveProcent {
    min-width: 25px;
    height: 25px;
  }
}

/* Очень маленькие высоты */
@media (max-height: 500px) {
  .UserAchivesMainPanel {
    height: 45px;
    padding: 0 var(--spacing-xs);
  }
  
  .AchiveProcent {
    min-width: 20px;
    height: 20px;
  }
  
  .progress-text {
    font-size: 0.6rem;
  }
}
</style>