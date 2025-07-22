<template>
  <div class="card p-3 shadow-sm">
    <h5 class="mb-3">Your Parking Summary</h5>
    <Bar :data="chartData" :options="chartOptions" />
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
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
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
      label: "Total Parking Hours",
      backgroundColor: "#42A5F5",
      data: props.stats.hours,
    },
    {
      label: "Spent (₹)",
      backgroundColor: "#66BB6A",
      data: props.stats.revenue,
    },
  ],
};

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: "top" },
    title: { display: true, text: "Parking & Spent" },
  },
};
</script>
