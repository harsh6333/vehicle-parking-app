<script setup>
import { onMounted, ref } from "vue";
import { fetchUserStats } from "@/services/userService";
import UserStatsChart from "@/components/Common/charts/UserStatsChart.vue";

const stats = ref(null);

onMounted(async () => {
  const res = await fetchUserStats();
  stats.value = res.data;
});
</script>

<template>
  <div>
    <UserStatsChart v-if="stats" :stats="stats" />
  </div>
</template>
