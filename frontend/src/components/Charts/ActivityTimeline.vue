<template>
  <div class="activity-timeline">
    <div class="timeline-header">
      <h4>{{ title }}</h4>
      <button class="btn btn-sm" @click="$emit('view-all')">
        Все действия
      </button>
    </div>
    
    <div class="timeline">
      <div 
        v-for="activity in displayedActivities" 
        :key="activity.id"
        class="timeline-item"
        :class="`timeline-${activity.type}`"
      >
        <div class="timeline-marker">
          <div class="marker-dot"></div>
          <div class="marker-line" v-if="!activity.last"></div>
        </div>
        
        <div class="timeline-content">
          <div class="activity-header">
            <span class="activity-user">{{ activity.user }}</span>
            <span class="activity-time">{{ activity.time }}</span>
          </div>
          
          <div class="activity-action">
            {{ activity.action }}
          </div>
          
          <div 
            v-if="activity.details" 
            class="activity-details"
          >
            {{ activity.details }}
          </div>
          
          <div 
            v-if="activity.meta" 
            class="activity-meta"
          >
            <span 
              v-for="(value, key) in activity.meta" 
              :key="key"
              class="meta-tag"
            >
              {{ key }}: {{ value }}
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <div 
      v-if="activities.length > maxItems" 
      class="timeline-footer"
    >
      <button class="btn btn-link" @click="showAll = !showAll">
        {{ showAll ? 'Свернуть' : `Показать все (${activities.length})` }}
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'ActivityTimeline',
  props: {
    activities: {
      type: Array,
      default: () => []
    },
    title: {
      type: String,
      default: 'Последняя активность'
    },
    maxItems: {
      type: Number,
      default: 5
    }
  },
  emits: ['view-all'],
  setup(props) {
    const showAll = ref(false)

    const defaultActivities = [
      {
        id: 1,
        user: 'Иван Петров',
        action: 'создал новый заказ #12345',
        time: '5 минут назад',
        type: 'success',
        details: 'Заказ на сумму ₽15,000',
        meta: { category: 'Продажа', priority: 'Высокая' }
      },
      {
        id: 2,
        user: 'Мария Сидорова',
        action: 'обновила профиль компании',
        time: '12 минут назад',
        type: 'info'
      },
      {
        id: 3,
        user: 'Алексей Козлов',
        action: 'добавил новый товар в каталог',
        time: '25 минут назад',
        type: 'success',
        details: 'Товар "Премиум пакет"'
      },
      {
        id: 4,
        user: 'Система',
        action: 'завершено автоматическое резервное копирование',
        time: '1 час назад',
        type: 'warning'
      },
      {
        id: 5,
        user: 'Елена Новикова',
        action: 'отклонила запрос на возврат #678',
        time: '2 часа назад',
        type: 'danger',
        details: 'Причина: нарушение условий возврата'
      }
    ]

    const activities = ref(props.activities.length ? props.activities : defaultActivities)

    const displayedActivities = computed(() => {
      const items = showAll.value ? activities.value : activities.value.slice(0, props.maxItems)
      
      return items.map((item, index) => ({
        ...item,
        last: index === items.length - 1
      }))
    })

    return {
      showAll,
      displayedActivities
    }
  }
}
</script>

<style scoped>
.activity-timeline {
  background: white;
  border-radius: 8px;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.timeline-header h4 {
  margin: 0;
  color: #2d3748;
  font-size: 16px;
  font-weight: 600;
}

.btn-link {
  background: transparent;
  border: none;
  color: #4299e1;
  cursor: pointer;
  font-size: 14px;
}

.btn-link:hover {
  color: #3182ce;
  text-decoration: underline;
}

.timeline {
  padding: 16px;
}

.timeline-item {
  display: flex;
  position: relative;
  margin-bottom: 0;
}

.timeline-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 16px;
}

.marker-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid;
  z-index: 2;
  flex-shrink: 0;
}

.marker-line {
  flex: 1;
  width: 2px;
  background: #e2e8f0;
  margin-top: 4px;
}

.timeline-content {
  flex: 1;
  padding-bottom: 20px;
}

.timeline-success .marker-dot {
  border-color: #48bb78;
  background: #48bb78;
}

.timeline-info .marker-dot {
  border-color: #4299e1;
  background: #4299e1;
}

.timeline-warning .marker-dot {
  border-color: #ed8936;
  background: #ed8936;
}

.timeline-danger .marker-dot {
  border-color: #f56565;
  background: #f56565;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.activity-user {
  font-weight: 500;
  color: #2d3748;
}

.activity-time {
  font-size: 12px;
  color: #718096;
}

.activity-action {
  color: #4a5568;
  margin-bottom: 4px;
}

.activity-details {
  font-size: 14px;
  color: #718096;
  margin-bottom: 4px;
}

.activity-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}

.meta-tag {
  padding: 2px 6px;
  background: #f7fafc;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 11px;
  color: #718096;
}

.timeline-footer {
  padding: 16px;
  border-top: 1px solid #e2e8f0;
  text-align: center;
}

/* Анимации */
.timeline-item {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Адаптивность */
@media (max-width: 768px) {
  .activity-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
  
  .activity-meta {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>