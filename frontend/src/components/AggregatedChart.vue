<template>
  <div class="chart-container">
    <canvas ref="chart"></canvas>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import Chart, { type ChartOptions } from 'chart.js/auto';
import axios from 'axios';

const chart = ref<HTMLCanvasElement>();
const error = ref<string | null>(null);

async function fetchAggregatedData(window: string) {
  try {
    const res = await axios.get(`http://localhost:8000/api/sensors/aggregated/?window=${window}`);
    return res.data;
  } catch (err) {
    error.value = 'ไม่สามารถดึงข้อมูลได้จาก API';
    console.error('API Error:', err);
    return null;
  }
}

function generateChartData(data: any) {
  return [
    {
      label: 'Temperature Mean',
      data: data.temperature_mean,
      borderColor: '#36A2EB',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      tension: 0.4,
      fill: true
    },
    {
      label: 'Temperature Max',
      data: data.temperature_max,
      borderColor: '#FF6384',
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      tension: 0.4,
      fill: false
    },
    {
      label: 'Temperature Min',
      data: data.temperature_min,
      borderColor: '#4BC0C0',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      tension: 0.4,
      fill: false
    }
  ];
}

function createChart(data: any) {
  const labels = Array.from({ length: data.temperature_mean.length }, (_, i) => `T${i + 1}`);
  const datasets = generateChartData(data);

  new Chart(chart.value!.getContext('2d')!, {
    type: 'line',
    data: {
      labels,
      datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top' },
        tooltip: { 
          mode: 'index', 
          intersect: false,
          titleFont: { size: 16 },
          bodyFont: { size: 14 },
          padding: 10
        },
        title: {
          display: true,
          text: 'Temperature Data Aggregation (Mean, Max, Min)',
          font: { size: 16, weight: 'bold' },
          padding: { bottom: 20 }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Time Slot',
            font: { size: 14, weight: 'bold' },
            padding: { top: 10 }
          }
        },
        y: {
          title: {
            display: true,
            text: 'Temperature (°C)',
            font: { size: 14, weight: 'bold' },
            padding: { bottom: 10 }
          },
          beginAtZero: true
        }
      },
      animation: {
        duration: 1000,
        easing: 'easeOutQuart',
      }
    } as ChartOptions<'line'>
  });
}

onMounted(async () => {
  const data = await fetchAggregatedData('1H');
  if (data) {
    createChart(data);
  }
});
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 500px;
  max-width: 900px;
  margin: 0 auto;
}

.error {
  color: red;
  text-align: center;
  margin-top: 20px;
}

@media screen and (max-width: 768px) {
  .chart-container {
    height: 400px;
  }
}
</style>
