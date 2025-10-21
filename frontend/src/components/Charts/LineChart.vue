<template>
  <div class="line-chart">
    <div class="chart-header">
      <h4>{{ title }}</h4>
      <div class="chart-legend" v-if="legend && legend.length">
        <div 
          v-for="item in legend" 
          :key="item.label"
          class="legend-item"
        >
          <span 
            class="legend-color" 
            :style="{ backgroundColor: item.color }"
          ></span>
          <span class="legend-label">{{ item.label }}</span>
        </div>
      </div>
    </div>
    <div class="chart-container">
      <canvas ref="chartRef" :width="width" :height="height"></canvas>
    </div>
    <div class="chart-footer" v-if="footerText">
      {{ footerText }}
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, onUnmounted } from 'vue'

export default {
  name: 'LineChart',
  props: {
    data: {
      type: Object,
      default: () => ({})
    },
    title: {
      type: String,
      default: 'Line Chart'
    },
    width: {
      type: Number,
      default: 400
    },
    height: {
      type: Number,
      default: 200
    },
    footerText: String,
    legend: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    const chartRef = ref(null)
    let chartInstance = null

    const defaultData = {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [
        {
          label: 'Dataset 1',
          data: [65, 59, 80, 81, 56, 55],
          borderColor: '#4299e1',
          backgroundColor: 'rgba(66, 153, 225, 0.1)',
          tension: 0.4,
          fill: true
        }
      ]
    }

    const renderChart = async () => {
      if (!chartRef.value) return

      // Динамический импорт Chart.js для уменьшения размера бандла
      const { Chart } = await import('chart.js/auto')
      
      if (chartInstance) {
        chartInstance.destroy()
      }

      const ctx = chartRef.value.getContext('2d')
      chartInstance = new Chart(ctx, {
        type: 'line',
        data: props.data.datasets ? props.data : defaultData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              mode: 'index',
              intersect: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0, 0, 0, 0.1)'
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          },
          interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
          }
        }
      })
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
      chartRef
    }
  }
}
</script>

<style scoped>
.line-chart {
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

.chart-legend {
  display: flex;
  gap: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-label {
  font-size: 12px;
  color: #718096;
}

.chart-container {
  position: relative;
  height: 300px;
}

.chart-footer {
  margin-top: 12px;
  font-size: 12px;
  color: #a0aec0;
  text-align: center;
}
</style>