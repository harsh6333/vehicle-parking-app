<script setup>
import { ref, onMounted } from "vue";
import { fetchAdminStats } from "@/services/adminService";
import StatChart from "@/components/Common/charts/StatChart.vue";
import NavigationBar from "@/components/Common/NavigationBar.vue";
import ErrorToast from "@/components/Common/ErrorToast.vue";

const stats = ref({
  parking: null,
  revenue: null,
  totals: {
    users: 0,
    lots: 0,
    spots: 0,
    activeReservations: 0,
  },
});

const isLoading = ref(true);
const error = ref(null);

onMounted(async () => {
  error.value = null;
  isLoading.value = true;
  try {
    const res = await fetchAdminStats();

    stats.value = {
      parking: {
        type: "bar",
        data: {
          labels: res.data.parking.labels,
          datasets: [
            {
              label: "Reservations",
              backgroundColor: "#3b82f6",
              data: res.data.parking.values,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            title: { display: true, text: "Daily Reservations" },
          },
        },
      },
      revenue: {
        type: "line",
        data: {
          labels: res.data.revenue.labels,
          datasets: [
            {
              label: "Revenue (₹)",
              borderColor: "#10b981",
              data: res.data.revenue.values,
              fill: true,
              backgroundColor: "rgba(16, 185, 129, 0.1)",
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            title: { display: true, text: "Daily Revenue" },
          },
        },
      },
      totals: res.data.totals || stats.value.totals,
    };
  } catch (err) {
    console.error("Error fetching admin stats:", err);
    error.value =
      err?.response?.data?.msg || "Failed to load dashboard statistics.";
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <div class="">
    <NavigationBar
      :navigation="[
        {
          title: 'Dashboard',
          link: '/admin/dashboard',
          icon: 'bi-speedometer2',
        },
        { title: 'Users', link: '/admin/all_users', icon: 'bi-people' },
        { title: 'Lots', link: '/admin/all_lots', icon: 'bi-p-square' },
        {
          title: 'Summary',
          link: '/admin/summary',
          icon: 'bi-graph-up',
          active: true,
        },
      ]"
    />

    <div class="row my-4">
      <div class="col-12">
        <h4>System Summary</h4>
        <p class="text-muted">Key metrics and performance indicators</p>
      </div>
    </div>

    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else class="row g-4">
      <!-- Summary Cards -->
      <div class="col-md-3">
        <div class="card shadow-sm h-100">
          <div class="card-body text-center">
            <h5 class="card-title text-primary">
              <i class="bi-people"></i> Users
            </h5>
            <div class="display-5 my-3">{{ stats.totals.users }}</div>
            <p class="text-muted small mb-0">Total registered</p>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow-sm h-100">
          <div class="card-body text-center">
            <h5 class="card-title text-success">
              <i class="bi-p-square"></i> Parking Lots
            </h5>
            <div class="display-5 my-3">{{ stats.totals.lots }}</div>
            <p class="text-muted small mb-0">Total locations</p>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow-sm h-100">
          <div class="card-body text-center">
            <h5 class="card-title text-info">
              <i class="bi-p-circle"></i> Spots
            </h5>
            <div class="display-5 my-3">{{ stats.totals.spots }}</div>
            <p class="text-muted small mb-0">Total spaces</p>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow-sm h-100">
          <div class="card-body text-center">
            <h5 class="card-title text-warning">
              <i class="bi-calendar-check"></i> Active
            </h5>
            <div class="display-5 my-3">
              {{ stats.totals.activeReservations }}
            </div>
            <p class="text-muted small mb-0">Current reservations</p>
          </div>
        </div>
      </div>

      <!-- Charts -->
      <div class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5 class="card-title">Reservation Activity</h5>
            <StatChart :chartData="stats.parking" />
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5 class="card-title">Revenue Trend</h5>
            <StatChart :chartData="stats.revenue" />
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Error Toast -->
  <ErrorToast v-if="error" :message="error" @dismiss="error = null" />
</template>

<style scoped>
.card {
  border-radius: 10px;
  border: none;
}
.display-5 {
  font-size: 2rem;
  font-weight: 600;
}
</style>
