<template>
  <div class="dashboard-container">
    <NavigationBar :navigation="navigationItems" />

    <div class="container-fluid">
      <div class="row">
        <div class="w-100 main-content py-4">
          <HistoryHeader :modelValue="dateFilter" @update="loadHistory" />
          <HistoryStats
            :totalItems="totalItems"
            :activeCount="activeReservationsCount"
            :totalSpent="totalSpent"
          />
          <HistoryTable
            :history="history"
            :currentPage="currentPage"
            :itemsPerPage="itemsPerPage"
            :totalItems="totalItems"
            :totalPages="totalPages"
            :pages="pages"
            @cancel="cancelReservationfunc"
            @export="exportToCSV"
            @goToPage="goToPage"
            @prevPage="prevPage"
            @nextPage="nextPage"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import NavigationBar from "@/components/Common/NavigationBar.vue";
import HistoryHeader from "@/components/UserDashboard/HistoryPage/HistoryHeader.vue";
import HistoryStats from "@/components/UserDashboard/HistoryPage/HistoryStats.vue";
import HistoryTable from "@/components/UserDashboard/HistoryPage/HistoryTable.vue";

import { getHistory, releaseSpot } from "@/services/userService";

// State
const history = ref([]);
const dateFilter = ref(new Date().toISOString().split("T")[0]);
const currentPage = ref(1);
const itemsPerPage = 10;
const totalItems = ref(0);
const loading = ref(false);

const navigationItems = [
  {
    title: "Dashboard",
    link: "/user/dashboard",
    icon: "bi bi-speedometer2",
  },
  {
    title: "History",
    link: "/user/parking_history",
    icon: "bi bi-clock-history",
  },
];

// Computed
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage));
const activeReservationsCount = computed(
  () => history.value.filter((entry) => !entry.leaving_timestamp).length
);
const totalSpent = computed(() =>
  history.value.reduce(
    (sum, entry) => sum + parseFloat(calculateAmount(entry)),
    0
  )
);
const pages = computed(() => {
  const range = [];
  const maxVisiblePages = 5;
  let start = Math.max(1, currentPage.value - Math.floor(maxVisiblePages / 2));
  let end = Math.min(totalPages.value, start + maxVisiblePages - 1);
  if (end - start + 1 < maxVisiblePages) {
    start = Math.max(1, end - maxVisiblePages + 1);
  }
  for (let i = start; i <= end; i++) range.push(i);
  return range;
});

// Methods
const loadHistory = async () => {
  try {
    loading.value = true;
    const params = {
      page: currentPage.value,
      limit: itemsPerPage,
      date: dateFilter.value,
    };
    const res = await getHistory(params);
    history.value = res.data || [];
    totalItems.value = res.data.length || 0;
  } catch (err) {
    console.error("Failed to load history:", err);
  } finally {
    loading.value = false;
  }
};

const calculateDuration = (start, end) => {
  if (!start || !end) return 0;
  const diff = new Date(end) - new Date(start);
  return (diff / (1000 * 60 * 60)).toFixed(1);
};

const calculateAmount = (entry) => {
  const duration = calculateDuration(
    entry.reserved_at,
    entry.leaving_timestamp || entry.reserved_till
  );
  return (duration * entry.hourlyrate).toFixed(2);
};

const goToPage = (page) => {
  currentPage.value = page;
  loadHistory();
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    loadHistory();
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    loadHistory();
  }
};

const cancelReservationfunc = async (id, reserved_at) => {
  if (confirm("Are you sure you want to cancel this reservation?")) {
    try {
      await releaseSpot(id, reserved_at);
      await loadHistory();
    } catch (error) {
      console.error("Error cancelling reservation:", error);
    }
  }
};

const exportToCSV = () => {
  console.log("Export to CSV triggered");
};

onMounted(loadHistory);
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}
.main-content {
  padding: 1.5rem;
}
</style>
