<template>
  <div class="row mb-4">
    <StatCard
      title="Total Reservations"
      :value="totalItems"
      icon="bi bi-list-check"
      iconClass="bg-primary bg-opacity-10 text-primary"
    />
    <StatCard
      title="Active Reservations"
      :value="activeCount"
      icon="bi bi-hourglass-split"
      iconClass="bg-warning bg-opacity-10 text-warning"
    />
    <StatCard
      title="Total Spent"
      :value="'₹' + totalSpent.toFixed(2)"
      icon="bi bi-cash-coin"
      iconClass="bg-success bg-opacity-10 text-success"
    />
  </div>
</template>

<script setup>
import StatCard from "./StatCard.vue";
defineProps(["totalItems", "activeCount", "totalSpent"]);
</script>
