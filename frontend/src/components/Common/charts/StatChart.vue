<template>
  <div>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import Chart from "chart.js/auto";

const props = defineProps({
  chartData: Object,
  chartOptions: Object,
});

const canvas = ref(null);
let chartInstance;

const renderChart = () => {
  if (chartInstance) chartInstance.destroy();
  chartInstance = new Chart(canvas.value, {
    type: props.chartData.type || "bar",
    data: props.chartData.data,
    options: props.chartOptions,
  });
};

onMounted(renderChart);
watch(() => props.chartData, renderChart, { deep: true });
</script>

<style scoped>
canvas {
  max-width: 100%;
}
</style>
