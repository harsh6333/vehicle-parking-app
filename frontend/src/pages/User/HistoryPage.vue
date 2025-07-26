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
  <!-- Error Toast -->
  <ErrorToast v-if="error" :message="error" @dismiss="error = null" />
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import NavigationBar from "@/components/Common/NavigationBar.vue";
import HistoryHeader from "@/components/UserDashboard/HistoryPage/HistoryHeader.vue";
import HistoryStats from "@/components/UserDashboard/HistoryPage/HistoryStats.vue";
import HistoryTable from "@/components/UserDashboard/HistoryPage/HistoryTable.vue";

import {
  getHistory,
  releaseSpot,
  triggerCSVExport,
} from "@/services/userService";
import ErrorToast from "@/components/Common/ErrorToast.vue";

// State
const history = ref([]);
const dateFilter = ref(new Date().toISOString().split("T")[0]);
const currentPage = ref(1);
const itemsPerPage = 10;
const totalItems = ref(0);
const loading = ref(false);
const error = ref(null);

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
    active: true,
  },
  {
    title: "Statistics",
    link: "/user/statistics",
    icon: "bi-graph-up",
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

const loadHistory = async () => {
  error.value = null;
  loading.value = true;
  try {
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
    error.value = err?.response?.data?.msg || "Failed to load history.";
  } finally {
    loading.value = false;
  }
};

function calculateDuration(start, end) {
  const diff = (new Date(end) - new Date(start)) / 3600000;
  return Math.round(diff * 10) / 10;
}

function calculateAmount(entry) {
  const rate = entry.rate_per_hour || 20; // fallback if not present
  return Math.round(
    calculateDuration(entry.reserved_at, entry.reserved_till) * rate
  );
}

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
  error.value = null;
  if (confirm("Are you sure you want to cancel this reservation?")) {
    try {
      await releaseSpot(id, reserved_at);
      await loadHistory();
    } catch (err) {
      console.error("Error cancelling reservation:", err);
      error.value = err?.response?.data?.msg || "Failed to cancel reservation.";
    }
  }
};

const exportToCSV = async () => {
  error.value = null;
  try {
    await triggerCSVExport();
    alert("CSV export has been triggered. Check your email.");
  } catch (err) {
    console.error("CSV export failed:", err);
    error.value = err?.response?.data?.msg || "Failed to trigger CSV export.";
  }
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
