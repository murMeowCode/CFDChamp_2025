<template>
  <div class="error-page">
    <div class="error-container">
      <div class="error-content">
        <h1 class="error-title">Страница не найдена</h1>
        <p class="error-description">
          Возможно, эта страница была перемещена или удалена.
        </p>
        
        <div class="error-animation">
          <svg 
            class="face" 
            viewBox="0 0 320 380" 
            width="320" 
            height="380" 
            aria-label="Анимированное лицо 404"
          >
            <g
              fill="none"
              :stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="25"
            >
              <g class="face__eyes" transform="translate(0, 112.5)">
                <g transform="translate(15, 0)">
                  <polyline class="face__eye-lid" points="37,0 0,120 75,120" />
                  <polyline 
                    class="face__pupil" 
                    points="55,120 55,155" 
                    stroke-dasharray="35 35" 
                  />
                </g>
                <g transform="translate(230, 0)">
                  <polyline class="face__eye-lid" points="37,0 0,120 75,120" />
                  <polyline 
                    class="face__pupil" 
                    points="55,120 55,155" 
                    stroke-dasharray="35 35" 
                  />
                </g>
              </g>
              <rect 
                class="face__nose" 
                rx="4" 
                ry="4" 
                x="132.5" 
                y="112.5" 
                width="55" 
                height="155" 
              />
              <g stroke-dasharray="102 102" transform="translate(65, 334)">
                <path 
                  class="face__mouth-left" 
                  d="M 0 30 C 0 30 40 0 95 0" 
                  stroke-dashoffset="-102" 
                />
                <path 
                  class="face__mouth-right" 
                  d="M 95 0 C 150 0 190 30 190 30" 
                  stroke-dashoffset="102" 
                />
              </g>
            </g>
          </svg>
        </div>

        <div class="error-actions">
          <button @click="goBack" class="btn btn-secondary">
            ← Назад
          </button>
          <button @click="goHome" class="btn btn-primary">
            На главную
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Error404',
  computed: {
    currentColor() {
      return getComputedStyle(document.documentElement).getPropertyValue('--color-text').trim() || '#1a1d23';
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    goHome() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.error-page {
  min-height: 75vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-bg);
  padding: var(--spacing-xl);
}

.error-container {
  max-width: 500px;
  width: 100%;
  text-align: center;
}

.error-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xl);
}

.error-title {
  font-size: 2.5rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin: 0;
  line-height: 1.2;
}

.error-description {
  font-size: 1.125rem;
  color: var(--color-text-muted);
  margin: 0;
  line-height: 1.6;
}

.error-animation {
  display: flex;
  justify-content: center;
  margin: var(--spacing-lg) 0;
}

.face {
  color: var(--color-primary);
  filter: drop-shadow(var(--shadow-lg));
}

.error-actions {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
  justify-content: center;
  margin-top: var(--spacing-lg);
}

.btn {
  padding: var(--spacing-md) var(--spacing-xl);
  border-radius: var(--border-radius-lg);
  font-weight: var(--font-weight-medium);
  font-size: 1rem;
  text-decoration: none;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all var(--transition-normal);
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.btn-primary {
  background-color: var(--color-primary);
  color: var(--color-text-inverted);
  border-color: var(--color-primary);
}

.btn-primary:hover {
  background-color: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-secondary {
  background-color: transparent;
  color: var(--color-text);
  border-color: var(--color-border);
}

.btn-secondary:hover {
  background-color: var(--color-bg-muted);
  border-color: var(--color-border-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* Animations */
.face__eyes,
.face__eye-lid,
.face__mouth-left,
.face__mouth-right,
.face__nose,
.face__pupil {
  animation: eyes 1s 0.3s cubic-bezier(0.65, 0, 0.35, 1) forwards;
}

.face__eye-lid,
.face__pupil {
  animation-duration: 4s;
  animation-delay: 1.3s;
  animation-iteration-count: infinite;
}

.face__eye-lid {
  animation-name: eye-lid;
}

.face__mouth-left,
.face__mouth-right {
  animation-timing-function: cubic-bezier(0.33, 1, 0.68, 1);
}

.face__mouth-left {
  animation-name: mouth-left;
}

.face__mouth-right {
  animation-name: mouth-right;
}

.face__nose {
  animation-name: nose;
}

.face__pupil {
  animation-name: pupil;
}

/* Keyframes */
@keyframes eye-lid {
  from,
  40%,
  45%,
  to {
    transform: translateY(0);
  }
  42.5% {
    transform: translateY(17.5px);
  }
}

@keyframes eyes {
  from {
    transform: translateY(112.5px);
  }
  to {
    transform: translateY(15px);
  }
}

@keyframes pupil {
  from,
  37.5%,
  40%,
  45%,
  87.5%,
  to {
    stroke-dashoffset: 0;
    transform: translate(0, 0);
  }
  12.5%,
  25%,
  62.5%,
  75% {
    stroke-dashoffset: 0;
    transform: translate(-35px, 0);
  }
  42.5% {
    stroke-dashoffset: 35;
    transform: translate(0, 17.5px);
  }
}

@keyframes mouth-left {
  from,
  50% {
    stroke-dashoffset: -102;
  }
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes mouth-right {
  from,
  50% {
    stroke-dashoffset: 102;
  }
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes nose {
  from {
    transform: translate(0, 0);
  }
  to {
    transform: translate(0, 22.5px);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .error-title {
    font-size: 2rem;
  }
  
  .error-description {
    font-size: 1rem;
  }
  
  .face {
    width: 280px;
    height: 332px;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 200px;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .error-page {
    padding: var(--spacing-md);
  }
  
  .error-title {
    font-size: 1.75rem;
  }
  
  .face {
    width: 240px;
    height: 285px;
  }
}
</style>