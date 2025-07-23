<script setup>
import { onMounted, ref, computed } from "vue";
import { fetchUserStats } from "@/services/userService";
import UserStatsChart from "@/components/Common/charts/UserStatsChart.vue";
import NavigationBar from "@/components/Common/NavigationBar.vue";
import ErrorToast from "@/components/Common/ErrorToast.vue";

const stats = ref(null);
const isLoading = ref(true);
const lastUpdated = ref(null);
const error = ref(null);

// Calculate totals from stats
const totals = computed(() => {
  if (!stats.value) return null;
  return {
    totalHours: stats.value.hours.reduce((a, b) => a + b, 0).toFixed(1),
    totalSpent: stats.value.revenue.reduce((a, b) => a + b, 0).toFixed(2),
    totalBookings: stats.value.dates.length,
  };
});

onMounted(async () => {
  try {
    error.value = null;
    const res = await fetchUserStats();
    stats.value = res.data;
    lastUpdated.value = new Date().toLocaleString();
  } catch (err) {
    error.value =
      err.response?.data?.msg ||
      err.msg ||
      "Failed to load spots. Please try again later.";
  } finally {
    error.value = null;
    isLoading.value = false;
  }
});
</script>

<template>
  <div class="user-dashboard">
    <NavigationBar
      :navigation="[
        {
          title: 'Dashboard',
          link: '/user/dashboard',
          icon: 'bi-speedometer2',
        },
        {
          title: 'History',
          link: '/user/parking_history',
          icon: 'bi-clock-history',
        },
        {
          title: 'Statistics',
          link: '/user/statistics',
          icon: 'bi-graph-up',
          active: true,
        },
      ]"
    />

    <div class="dashboard-header my-4">
      <h4 class="mb-2">Your Parking Statistics</h4>
      <p class="text-muted">
        Insights into your parking history and spending
        <span v-if="lastUpdated" class="text-muted small ms-2">
          <i class="bi-clock-history me-1"></i>Updated: {{ lastUpdated }}
        </span>
      </p>
    </div>

    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading your statistics...</p>
    </div>

    <div v-else class="row g-4">
      <!-- Summary Cards -->
      <div class="col-md-4">
        <div class="card shadow-sm h-100">
          <div class="card-body text-center">
            <h5 class="card-title text-primary">
              <i class="bi-clock"></i> Total Hours
            </h5>
            <div class="display-5 my-2">{{ totals.totalHours }}</div>
            <p class="text-muted small mb-0">Parking time booked</p>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card shadow-sm h-100">
          <div class="card-body text-center">
            <h5 class="card-title text-success">
              <i class="bi-currency-rupee"></i> Total Spent
            </h5>
            <div class="display-5 my-2">₹{{ totals.totalSpent }}</div>
            <p class="text-muted small mb-0">On parking</p>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card shadow-sm h-100">
          <div class="card-body text-center">
            <h5 class="card-title text-info">
              <i class="bi-calendar-check"></i> Bookings
            </h5>
            <div class="display-5 my-2">{{ totals.totalBookings }}</div>
            <p class="text-muted small mb-0">Reservations made</p>
          </div>
        </div>
      </div>

      <!-- Main Chart -->
      <div class="col-12">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Your Parking History</h5>
            <p class="card-subtitle text-muted mb-3">
              Hours parked and amount spent over time
            </p>
            <UserStatsChart :stats="stats" />
            <div class="chart-footer mt-3 small text-muted">
              <i class="bi-info-circle me-1"></i>
              Shows your parking activity history by date
            </div>
          </div>
        </div>
      </div>

      <!-- Insights -->
      <div class="col-12">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">
              <i class="bi-lightbulb me-2 text-warning"></i>Your Parking
              Patterns
            </h5>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                <i class="bi-calendar-week me-2 text-primary"></i>
                <strong>Busiest day:</strong> {{ findBusiestDay(stats) }}
              </li>
              <li class="list-group-item">
                <i class="bi-cash-coin me-2 text-success"></i>
                <strong>Average cost:</strong> ₹{{
                  (totals.totalSpent / totals.totalBookings).toFixed(2)
                }}
                per booking
              </li>
              <li class="list-group-item">
                <i class="bi-clock-history me-2 text-info"></i>
                <strong>Average duration:</strong>
                {{ (totals.totalHours / totals.totalBookings).toFixed(1) }}
                hours per booking
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Error Toast -->
  <ErrorToast v-if="error" :message="error" @dismiss="error = null" />
</template>

<script>
export default {
  methods: {
    findBusiestDay(stats) {
      if (!stats || !stats.dates.length) return "Not enough data";
      const maxIndex = stats.hours.indexOf(Math.max(...stats.hours));
      return stats.dates[maxIndex];
    },
  },
};
</script>

<style scoped>
.user-dashboard {
  width: 100vw;
}

.dashboard-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 1rem;
}

.display-5 {
  font-size: 2rem;
  font-weight: 600;
}

.card {
  border-radius: 10px;
  border: none;
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}

.chart-footer {
  border-top: 1px dashed #eee;
  padding-top: 0.5rem;
}

.list-group-item {
  padding: 0.75rem 1.25rem;
  border-color: rgba(0, 0, 0, 0.05);
}
</style>
