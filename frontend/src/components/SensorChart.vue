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

async function fetchData() {
  try {
    const res = await axios.get('http://localhost:8000/api/sensors/processed/');
    return res.data;
  } catch (err) {
    error.value = 'ไม่สามารถดึงข้อมูลได้';
    console.error('API Error:', err);
    return [];
  }
}

function processAnomalies(data: any[]) {
  const temps = data.map((d: any) => d.temperature);
  return data.map((d: any, i: number) => d.temperature_anomaly ? temps[i] : null);
}

onMounted(async () => {
  const data = await fetchData();
  if (data.length === 0) return;

  const labels = data.map((d: any) => new Date(d.timestamp).toLocaleTimeString());
  const temps = data.map((d: any) => d.temperature);
  const anomalies = processAnomalies(data);

  const ctx = chart.value!.getContext('2d')!;
  new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        { 
          label: 'Temperature (°C)', 
          data: temps,
          borderColor: '#FF5733',
          backgroundColor: 'rgba(255, 87, 51, 0.2)',
          borderWidth: 3,
          fill: true,
          tension: 0.3,
          pointRadius: 3,
          pointHoverRadius: 6,
          pointBackgroundColor: '#FF5733',
        },
        { 
          label: 'Anomalies', 
          data: anomalies, 
          pointRadius: 6, 
          pointBackgroundColor: '#FFC300',
          pointBorderColor: '#FF5733',
          pointBorderWidth: 2,
          showLine: false,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: { top: 20, right: 20, bottom: 10, left: 10 }
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: {
            font: { size: 14 },
            padding: 20,
          }
        },
        tooltip: {
          mode: 'index',
          intersect: false,
          padding: 10,
          titleFont: { size: 16 },
          bodyFont: { size: 14 },
        },
        title: {
          display: true,
          text: 'Temperature Data and Anomalies', // หัวข้อหลักที่เพิ่มขึ้น
          font: { size: 16, weight: 'bold' },
          padding: { bottom: 20 }
        }
      },
      scales: {
        x: {
          type: 'category',
          grid: {
            display: false
          },
          title: {
            display: true,
            text: 'Time',
            font: { size: 14, weight: 'bold' },
            padding: { top: 10 }
          },
          ticks: {
            autoSkip: true,
            maxTicksLimit: 12,
            maxRotation: 45,
            minRotation: 0,
          }
        },
        y: {
          grid: {
            color: 'rgba(200,200,200,0.2)',
            borderDash: [4, 4],
          },
          title: {
            display: true,
            text: 'Temperature (°C)',
            font: { size: 14, weight: 'bold' },
            padding: { bottom: 10 }
          },
          beginAtZero: true,
          ticks: {
            stepSize: 5
          }
        }
      },
      animation: {
        duration: 1000,
        easing: 'easeOutQuart',
      }
    } as ChartOptions<'line'>
  });
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
  margin-top: 10px;
}
</style>
