<template>
  <div class="row mb-4">
    <div class="col-md-4">
      <StatCard
        title="Total Lots"
        :value="lots.length"
        icon="bi-p-square"
        color="primary"
        :loading="loading"
      />
    </div>
    <div class="col-md-4">
      <StatCard
        title="Total Spots"
        :value="totalSpots"
        icon="bi-car-front"
        color="success"
        :loading="loading"
      />
    </div>
    <div class="col-md-4">
      <StatCard
        title="Registered Users"
        :value="users.length"
        icon="bi-people"
        color="info"
        :loading="loading"
      />
    </div>
  </div>
</template>

<script setup>
import StatCard from "./StatsCard.vue";

defineProps({
  lots: {
    type: Array,
    required: true,
  },
  totalSpots: {
    type: Number,
    required: true,
  },
  users: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});
</script>
