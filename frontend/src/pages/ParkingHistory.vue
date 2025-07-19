<template>
  <div class="container py-5">
    <h3 class="mb-4">Parking History</h3>
    <HistoryTable :history="history" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getHistory } from "@/services/userService";
import HistoryTable from "@/components/UserDashboard/HistoryTable.vue";

const history = ref([]);
onMounted(async () => {
  const res = await getHistory();
  history.value = res.data;
});
</script>
