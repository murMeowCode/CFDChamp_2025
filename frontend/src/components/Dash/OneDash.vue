<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h2 class="dashboard-title">{{ title }}</h2>
      <div class="dashboard-actions">
        <slot name="actions"></slot>
      </div>
    </div>
    
    <div class="dashboard-content">
      <!-- Статистические карточки -->
      <div class="stats-grid" v-if="stats && stats.length">
        <div 
          v-for="(stat, index) in stats" 
          :key="index" 
          class="stat-card"
          :class="`stat-${stat.type || 'default'}`"
        >
          <div class="stat-icon">
            <i :class="stat.icon"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
            <div 
              v-if="stat.trend" 
              class="stat-trend"
              :class="`trend-${stat.trend.direction}`"
            >
              <i :class="trendIcon(stat.trend.direction)"></i>
              {{ stat.trend.value }}
            </div>
          </div>
        </div>
      </div>

      <!-- Графики -->
      <div class="charts-section" v-if="charts && charts.length">
        <div 
          v-for="(chart, index) in charts" 
          :key="index" 
          class="chart-container"
        >
          <h3 class="chart-title">{{ chart.title }}</h3>
          <div class="chart-content">
            <slot :name="`chart-${chart.type}`" :data="chart.data"></slot>
          </div>
        </div>
      </div>

      <!-- Таблицы -->
      <div class="tables-section" v-if="tables && tables.length">
        <div 
          v-for="(table, index) in tables" 
          :key="index" 
          class="table-container"
        >
          <h3 class="table-title">{{ table.title }}</h3>
          <div class="table-content">
            <slot :name="`table-${table.type}`" :data="table.data"></slot>
          </div>
        </div>
      </div>

      <!-- Произвольный контент -->
      <div class="custom-content">
        <slot name="custom"></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  props: {
    title: {
      type: String,
      default: 'Дашборд'
    },
    stats: {
      type: Array,
      default: () => []
    },
    charts: {
      type: Array,
      default: () => []
    },
    tables: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    trendIcon(direction) {
      return direction === 'up' ? 'fas fa-arrow-up' : 'fas fa-arrow-down'
    }
  }
}
</script>

<style scoped>
.dashboard {
  background: #f8fafc;
  min-height: 100vh;
  padding: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.dashboard-title {
  color: #1a202c;
  font-size: 28px;
  font-weight: 700;
  margin: 0;
}

.dashboard-actions {
  display: flex;
  gap: 10px;
}

/* Статистические карточки */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border-left: 4px solid #4299e1;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-card.stat-success {
  border-left-color: #48bb78;
}

.stat-card.stat-warning {
  border-left-color: #ed8936;
}

.stat-card.stat-danger {
  border-left-color: #f56565;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: #ebf8ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #4299e1;
}

.stat-card.stat-success .stat-icon {
  background: #f0fff4;
  color: #48bb78;
}

.stat-card.stat-warning .stat-icon {
  background: #fffaf0;
  color: #ed8936;
}

.stat-card.stat-danger .stat-icon {
  background: #fff5f5;
  color: #f56565;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #718096;
  margin-bottom: 8px;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 600;
}

.trend-up {
  color: #48bb78;
}

.trend-down {
  color: #f56565;
}

/* Секции с графиками и таблицами */
.charts-section,
.tables-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 30px;
}

.chart-container,
.table-container {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-title,
.table-title {
  color: #2d3748;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 16px 0;
}

.chart-content,
.table-content {
  min-height: 200px;
}

.custom-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Адаптивность */
@media (max-width: 768px) {
  .dashboard {
    padding: 15px;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .charts-section,
  .tables-section {
    grid-template-columns: 1fr;
  }
  
  .stat-value {
    font-size: 28px;
  }
}
</style>