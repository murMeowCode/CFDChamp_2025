<template>
  <div class="bar-chart">
    <div class="chart-header">
      <h4>{{ title }}</h4>
      <div class="chart-controls">
        <select v-model="selectedPeriod" @change="handlePeriodChange" class="period-select">
          <option value="week">За неделю</option>
          <option value="month">За месяц</option>
          <option value="year">За год</option>
        </select>
      </div>
    </div>
    <div class="chart-container">
      <canvas ref="chartRef" :width="width" :height="height"></canvas>
    </div>
    <div class="chart-summary" v-if="summary">
      <div class="summary-item">
        <span class="summary-label">Среднее:</span>
        <span class="summary-value">{{ summary.average }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">Максимум:</span>
        <span class="summary-value">{{ summary.max }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, onUnmounted } from 'vue'

export default {
  name: 'BarChart',
  props: {
    data: {
      type: Object,
      default: () => ({})
    },
    title: {
      type: String,
      default: 'Bar Chart'
    },
    width: {
      type: Number,
      default: 400
    },
    height: {
      type: Number,
      default: 200
    },
    summary: {
      type: Object,
      default: null
    }
  },
  setup(props) {
    const chartRef = ref(null)
    const selectedPeriod = ref('month')
    let chartInstance = null

    const generateBarData = (period) => {
      const periods = {
        week: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
        month: ['Нед 1', 'Нед 2', 'Нед 3', 'Нед 4'],
        year: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      }

      const labels = periods[period] || periods.month
      
      return {
        labels,
        datasets: [
          {
            label: 'Доход',
            data: labels.map(() => Math.floor(Math.random() * 1000) + 500),
            backgroundColor: '#48bb78',
            borderColor: '#48bb78',
            borderWidth: 1,
            borderRadius: 4
          },
          {
            label: 'Расход',
            data: labels.map(() => Math.floor(Math.random() * 800) + 300),
            backgroundColor: '#f56565',
            borderColor: '#f56565',
            borderWidth: 1,
            borderRadius: 4
          }
        ]
      }
    }

    const renderChart = async () => {
      if (!chartRef.value) return

      const { Chart } = await import('chart.js/auto')
      
      if (chartInstance) {
        chartInstance.destroy()
      }

      const chartData = props.data.datasets ? props.data : generateBarData(selectedPeriod.value)

      const ctx = chartRef.value.getContext('2d')
      chartInstance = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                usePointStyle: true,
                padding: 15
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0, 0, 0, 0.1)'
              },
              ticks: {
                callback: function(value) {
                  return '₽' + value
                }
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          }
        }
      })
    }

    const handlePeriodChange = () => {
      renderChart()
    }

    onMounted(() => {
      renderChart()
    })

    watch(() => props.data, () => {
      renderChart()
    }, { deep: true })

    onUnmounted(() => {
      if (chartInstance) {
        chartInstance.destroy()
      }
    })

    return {
      chartRef,
      selectedPeriod,
      handlePeriodChange
    }
  }
}
</script>

<style scoped>
.bar-chart {
  background: white;
  border-radius: 8px;
  padding: 16px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-header h4 {
  margin: 0;
  color: #2d3748;
  font-size: 16px;
  font-weight: 600;
}

.period-select {
  padding: 6px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 14px;
  background: white;
}

.chart-container {
  position: relative;
  height: 300px;
}

.chart-summary {
  display: flex;
  justify-content: space-around;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.summary-label {
  font-size: 12px;
  color: #718096;
  margin-bottom: 4px;
}

.summary-value {
  font-size: 14px;
  font-weight: 600;
  color: #2d3748;
}
</style>