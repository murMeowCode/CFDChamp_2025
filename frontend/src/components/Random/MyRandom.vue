<template>
  <div class="cosmic-description">
    <!-- Фоновые элементы -->
    <div class="cosmic-bg">
      <div class="star-field">
        <div 
          v-for="i in 30" 
          :key="i"
          class="star"
          :style="{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 3}s`
          }"
        />
      </div>
      
      <!-- Орбиты планет -->
      <div class="orbits">
        <div 
          v-for="(size, index) in [1, 1.3, 1.6, 1.9, 2.2, 2.5]"
          :key="index"
          class="orbit" 
          :style="{ 
            width: `${size * 40}px`, 
            height: `${size * 40}px`,
            animationDelay: `${index * 0.5}s`
          }"
        />
      </div>
    </div>

    <!-- Контент -->
    <div class="cosmic-content">
      <div class="title-section">
        <div 
          class="accent-planet"
          :style="{ 
            backgroundColor: accentColor,
            boxShadow: `0 0 20px ${accentColor}80`
          }"
        />
        <h1 class="cosmic-title">{{ title }}</h1>
      </div>
      
      <p class="cosmic-subtitle">{{ description }}</p>
      
      <div class="features-grid">
        <div 
          v-for="(feature, index) in features"
          :key="index"
          class="feature-item"
          @mouseenter="hoverFeature(index)"
          @mouseleave="resetFeature"
        >
          <div 
            class="feature-dot"
            :style="{ backgroundColor: accentColor }"
          />
          <span class="feature-text">{{ feature }}</span>
        </div>
      </div>

      <!-- Декоративные планеты -->
      <div class="floating-planets">
        <div 
          class="planet planet-1"
          :style="{ animationDelay: '0s' }"
        />
        <div 
          class="planet planet-2"
          :style="{ animationDelay: '1.5s' }"
        />
        <div 
          class="planet planet-3"
          :style="{ animationDelay: '3s' }"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CosmicDescription',
  props: {
    title: {
      type: String,
      default: "Солнечная система"
    },
    description: {
      type: String,
      default: "Наша космическая обитель в бескрайней Вселенной"
    },
    features: {
      type: Array,
      default: () => [
        "8 планет, вращающихся вокруг звезды",
        "Более 200 спутников",
        "Возраст: 4.6 млрд лет",
        "Диаметр: 287 млрд км"
      ]
    },
    accentColor: {
      type: String,
      default: "#6366f1"
    }
  },
  methods: {
    hoverFeature(index) {
      console.log(`Hovered feature ${index}`);
    },
    resetFeature() {
      // Сброс состояний при уходе курсора
    }
  }
}
</script>

<style scoped>
.cosmic-description {
  position: relative;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  color: #ffffff;
  padding: 2rem 1.5rem;
  border-radius: 16px;
  overflow: hidden;
  font-family: 'Segoe UI', system-ui, sans-serif;
  min-height: 350px;
  max-width: 450px;
  width: 100%;
  border: 1px solid #2a2a4a;
  box-shadow: 
    0 0 30px rgba(99, 102, 241, 0.1),
    inset 0 0 60px rgba(99, 102, 241, 0.05);
}

/* Фоновые звезды */
.star-field {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.star {
  position: absolute;
  width: 1.5px;
  height: 1.5px;
  background: #ffffff;
  border-radius: 50%;
  animation: twinkle 3s infinite ease-in-out;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.3; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1.2); }
}

/* Орбиты */
.orbits {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.orbit {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 50%;
  animation: rotate 25s infinite linear;
}

@keyframes rotate {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

/* Контент */
.cosmic-content {
  position: relative;
  z-index: 2;
  max-width: 380px;
  margin: 0 auto;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 1rem;
}

.accent-planet {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  animation: pulse 2s infinite ease-in-out;
  flex-shrink: 0;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.cosmic-title {
  font-size: 1.8rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  line-height: 1.2;
}

.cosmic-subtitle {
  font-size: 1rem;
  color: #c7d2fe;
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

/* Список особенностей */
.features-grid {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 0.8rem;
  padding: 0.6rem 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(8px);
  transition: all 0.3s ease;
  cursor: pointer;
}

.feature-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
}

.feature-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 0.4rem;
}

.feature-text {
  font-size: 0.9rem;
  line-height: 1.3;
  color: #e2e8f0;
}

/* Плавающие планеты */
.floating-planets {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 60px;
}

.planet {
  position: absolute;
  border-radius: 50%;
  animation: float 6s infinite ease-in-out;
}

.planet-1 {
  width: 12px;
  height: 12px;
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
  top: 25%;
  right: 20%;
}

.planet-2 {
  width: 10px;
  height: 10px;
  background: linear-gradient(135deg, #10b981, #34d399);
  top: 65%;
  right: 30%;
}

.planet-3 {
  width: 14px;
  height: 14px;
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  top: 45%;
  right: 15%;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) scale(1); }
  50% { transform: translateY(-15px) scale(1.05); }
}

/* Адаптивность */
@media (max-width: 480px) {
  .cosmic-description {
    padding: 1.5rem 1rem;
    min-height: 320px;
    max-width: 100%;
  }
  
  .cosmic-title {
    font-size: 1.6rem;
  }
  
  .cosmic-content {
    max-width: 100%;
  }
  
  .floating-planets {
    width: 40px;
  }
  
  .orbits {
    transform: translate(-50%, -50%) scale(0.7);
  }
  
  .feature-text {
    font-size: 0.85rem;
  }
}
</style>