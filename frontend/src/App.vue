<!-- frontend\src\App.vue -->
<template>
  <div :class="['app-container', { dark: isDark } ]">
    <header class="app-header">
      <div class="header-left">
        <h1 class="app-title">Sensor Dashboard</h1>
        <span v-if="lastUpdated" class="last-updated" aria-live="polite">
          Updated: {{ lastUpdated }}
        </span>
      </div>
      <div class="controls">
        <button
          @click="refreshAll"
          aria-label="Refresh all data"
          class="btn refresh-btn"
          :disabled="loading"
        >
          <span v-if="loading" class="spinner" aria-hidden="true"></span>
          <span v-else>⟳ Refresh</span>
        </button>
        <button
          @click="toggleTheme"
          aria-label="Toggle theme"
          class="btn theme-toggle"
        >
          {{ isDark ? '🌙 Dark' : '☀️ Light' }}
        </button>
      </div>
    </header>

    <main class="charts-grid">
      <section class="chart-card">
        <h2>Real-time Sensor Data</h2>
        <SensorChart ref="sensorChartRef" />
      </section>
      <section class="chart-card">
        <h2>Aggregated Statistics</h2>
        <AggregatedChart ref="aggregatedChartRef" />
      </section>
    </main>

    <footer class="app-footer">
      <p>&copy; {{ currentYear }} Test</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import SensorChart from './components/SensorChart.vue'
import AggregatedChart from './components/AggregatedChart.vue'

const sensorChartRef = ref<InstanceType<typeof SensorChart> | null>(null)
const aggregatedChartRef = ref<InstanceType<typeof AggregatedChart> | null>(null)

const loading = ref(false)
const lastUpdated = ref<string | null>(null)

async function refreshAll() {
  try {
    loading.value = true
    await Promise.all([
      sensorChartRef.value?.refreshData(),
      aggregatedChartRef.value?.refreshData(),
    ])
    const now = new Date()
    lastUpdated.value = now.toLocaleTimeString()
  } catch (error) {
    console.error('Refresh failed', error)
    // here you could show a toast notification
  } finally {
    loading.value = false
  }
}

const isDark = ref(false)
function toggleTheme() {
  isDark.value = !isDark.value
}

const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
:root {
  --bg-color: #ffffff;
  --text-color: #333333;
  --card-bg: #ffffff;
  --header-bg: #f5f5f5;
  --footer-bg: #f5f5f5;
  --btn-bg: #007bff;
  --btn-hover: #0056b3;
  --spinner-size: 1rem;
}
.dark {
  --bg-color: #1e1e1e;
  --text-color: #f0f0f0;
  --card-bg: #2e2e2e;
  --header-bg: #2a2a2a;
  --footer-bg: #2a2a2a;
  --btn-bg: #4a90e2;
  --btn-hover: #357ab8;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
  font-family:
    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.app-header {
  background-color: var(--header-bg);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(0,0,0,0.1);
}

.header-left {
  display: flex;
  flex-direction: column;
}

.last-updated {
  font-size: 0.85rem;
  color: var(--text-color);
  opacity: 0.7;
  margin-top: 0.25rem;
}

.controls {
  display: flex;
  gap: 0.75rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  background-color: var(--btn-bg);
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s, transform 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn:hover:enabled {
  background-color: var(--btn-hover);
  transform: translateY(-1px);
}

.spinner {
  width: var(--spinner-size);
  height: var(--spinner-size);
  border: 2px solid rgba(255,255,255,0.6);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  padding: 2rem;
  flex-grow: 1;
}

@media (min-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.chart-card {
  background-color: var(--card-bg);
  border: 1px solid rgba(0,0,0,0.1);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s;
}

.chart-card h2 {
  margin: 0 0 1rem;
  font-size: 1.25rem;
  font-weight: 600;
}

.app-footer {
  background-color: var(--footer-bg);
  text-align: center;
  padding: 1rem;
  border-top: 1px solid rgba(0,0,0,0.1);
}
</style>