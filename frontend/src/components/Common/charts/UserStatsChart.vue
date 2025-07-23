<template>
  <div class="chart-container">
    <Bar :data="chartData" :options="chartOptions" class="user-stats-chart" />
  </div>
</template>

<script setup>
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  Colors,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  Colors
);

const props = defineProps({
  stats: {
    type: Object,
    required: true,
  },
});

const chartData = {
  labels: props.stats.dates,
  datasets: [
    {
      label: "Parking Hours",
      backgroundColor: "#3b82f6",
      borderRadius: 4,
      data: props.stats.hours,
      yAxisID: "y",
    },
    {
      label: "Amount Spent (₹)",
      backgroundColor: "#10b981",
      borderRadius: 4,
      data: props.stats.revenue,
      yAxisID: "y1",
    },
  ],
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "top",
      labels: {
        usePointStyle: true,
      },
    },
    tooltip: {
      callbacks: {
        label: function (context) {
          let label = context.dataset.label || "";
          if (label) {
            label += ": ";
          }
          if (context.datasetIndex === 0) {
            label += context.parsed.y + " hours";
          } else {
            label += "₹" + context.parsed.y.toFixed(2);
          }
          return label;
        },
      },
    },
  },
  scales: {
    y: {
      type: "linear",
      display: true,
      position: "left",
      title: {
        display: true,
        text: "Parking Hours",
      },
    },
    y1: {
      type: "linear",
      display: true,
      position: "right",
      title: {
        display: true,
        text: "Amount (₹)",
      },
      grid: {
        drawOnChartArea: false,
      },
      ticks: {
        callback: function (value) {
          return "₹" + value;
        },
      },
    },
  },
};
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}

.user-stats-chart {
  width: 100%;
  height: 100%;
}
</style>
