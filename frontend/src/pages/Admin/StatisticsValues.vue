<script setup>
import { ref, onMounted } from "vue";
import { fetchAdminStats } from "@/services/adminService"; 
import StatChart from "@/components/Common/charts/StatChart.vue";

const parkingStats = ref(null);
const revenueStats = ref(null);

onMounted(async () => {
  const res = await fetchAdminStats(); 
  parkingStats.value = {
    type: "bar",
    data: {
      labels: res.data.parking.labels,
      datasets: [
        {
          label: "Reservations per Day",
          backgroundColor: "#42a5f5",
          data: res.data.parking.values,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        title: { display: true, text: "Parking Stats" },
      },
    },
  };

  revenueStats.value = {
    type: "line",
    data: {
      labels: res.data.revenue.labels,
      datasets: [
        {
          label: "Revenue (₹)",
          borderColor: "#66bb6a",
          fill: false,
          data: res.data.revenue.values,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        title: { display: true, text: "Revenue Summary" },
      },
    },
  };
});
</script>

<template>
  <div class="container mt-4">
    <h4 class="mb-3">Statistics Overview</h4>
    <div class="row">
      <div class="col-md-6">
        <StatChart v-if="parkingStats" :chartData="parkingStats" />
      </div>
      <div class="col-md-6">
        <StatChart v-if="revenueStats" :chartData="revenueStats" />
      </div>
    </div>
  </div>
</template>
