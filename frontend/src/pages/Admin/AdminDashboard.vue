<template>
  <div class="admin-dashboard">
    <!-- Header -->
    <NavigationBar
      :navigation="[
        {
          title: 'Dashboard',
          link: '/admin/dashboard',
          icon: 'bi bi-speedometer2',
          active: true,
        },
        {
          title: 'All Users',
          link: '/admin/all_users',
          icon: 'bi bi-clock-history',
        },
        {
          title: 'All Lots',
          link: '/admin/all_lots',
          icon: 'bi bi-clock-history',
        },
        {
          title: 'Summary',
          link: '/admin/statistics',
          icon: 'bi bi-clock-history',
        },
        {
          title: 'Search',
          link: '/admin/search',
          icon: 'bi-search',
        },
      ]"
    />

    <!-- Main Content -->
    <main class="main-content">
      <div class="container-fluid px-4 py-4">
        <!-- Stats Cards -->
        <StatsOverview
          :lots="lots"
          :totalSpots="totalSpots"
          :users="users"
          :totalearnings="totalearnings"
          :loading="loading"
        />

        <!-- Main Content -->
        <div class="row g-4">
          <!-- Left Column -->
          <div class="col-lg-8">
            <!-- Lot Form -->
            <div class="card mb-4 border-0">
              <div class="card-header bg-transparent border-0 pb-0 pt-3 px-4">
                <h5
                  class="card-title fw-semibold mb-0 d-flex align-items-center"
                >
                  <i class="bi bi-plus-circle-fill me-2 text-primary"></i>
                  {{ form.id ? "Edit Parking Lot" : "Create New Parking Lot" }}
                </h5>
              </div>
              <div class="card-body px-4 pt-2 pb-4">
                <LotForm :model-value="form" @submit="handleSubmit" />
              </div>
            </div>

            <!-- Parking Lots List -->
            <div class="card border-0">
              <div class="card-header bg-transparent border-0 pb-0 pt-3 px-4">
                <div class="d-flex justify-content-between align-items-center">
                  <h5
                    class="card-title fw-semibold mb-0 d-flex align-items-center"
                  >
                    <i class="bi bi-list-ul me-2 text-primary"></i>
                    All Parking Lots
                  </h5>
                  <router-link to="/admin/all_lots" class="btn btn-action">
                    <i class="bi bi-eye"></i> View Spots
                  </router-link>
                </div>
              </div>

              <div class="card-body px-4">
                <div v-if="loading" class="text-center py-5">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
                <template v-else>
                  <div v-if="lots.length" class="row g-3">
                    <div v-for="lot in lots" :key="lot.id" class="col-md-6">
                      <LotCard :lot="lot" />
                    </div>
                  </div>
                  <EmptyState
                    v-else
                    icon="bi-p-square"
                    title="No parking lots available"
                    description="Get started by creating your first parking lot"
                    action-text="Add First Lot"
                    @action="resetForm"
                  />
                </template>
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="col-lg-4">
            <!-- Recent Reservations -->
            <div class="card mb-4 border-0">
              <div class="card-header bg-transparent border-0 p-3">
                <h5
                  class="card-title fw-semibold mb-0 d-flex align-items-center"
                >
                  <i class="bi bi-car-front-fill me-2 text-primary"></i>
                  Recent Reservations
                </h5>
              </div>
              <div class="card-body p-3">
                <div v-if="spotsLoading" class="text-center py-3">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
                <template v-else>
                  <LatestReservations
                    v-if="recenthistory"
                    :reservations="recenthistory"
                  />
                  <EmptyState
                    v-else
                    icon="bi-car-front"
                    title="No spots selected"
                    description="Select a parking lot to view available spots"
                    size="sm"
                  />
                </template>
              </div>
            </div>

            <!-- Recent Users -->
            <div class="card border-0">
              <div
                class="d-flex justify-content-between align-items-center bg-transparent border-0 pb-0 pt-3 px-4"
              >
                <h5
                  class="card-title fw-semibold mb-0 d-flex align-items-center"
                >
                  <i class="bi bi-people-fill me-2 text-primary"></i>
                  Recent Users
                </h5>
                <router-link to="/admin/all_users" class="btn btn-action">
                  View All Users
                </router-link>
              </div>
              <div class="card-body px-4 pt-2 pb-4">
                <div v-if="usersLoading" class="text-center py-4">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
                <template v-else>
                  <UserTable v-if="users.length" :users="recentUsers" />
                  <EmptyState
                    v-else
                    icon="bi-person-slash"
                    title="No users found"
                    description="There are currently no registered users"
                    size="sm"
                  />
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Error Toast -->
    <ErrorToast v-if="error" :message="error" @dismiss="error = null" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useAuthStore } from "@/store/auth";
import {
  createLot,
  updateLot,
  fetchDashboardData,
} from "@/services/adminService";

// Components
import StatsOverview from "@/components/AdminDashboard/StatsOverview.vue";
import LotForm from "@/components/AdminDashboard/LotForm.vue";
import LotCard from "@/components/AdminDashboard/LotCard.vue";
import UserTable from "@/components/AdminDashboard/UserTable.vue";
import EmptyState from "@/components/Common/EmptyState.vue";
import ErrorToast from "@/components/Common/ErrorToast.vue";
import NavigationBar from "@/components/Common/NavigationBar.vue";
import LatestReservations from "@/components/AdminDashboard/LatestReservations.vue";

// State
const auth = useAuthStore();
const error = ref(null);
const loading = ref(false);
const spotsLoading = ref(false);
const usersLoading = ref(false);

const dashboardData = ref(null);
const totalSpots = computed(() =>
  dashboardData.value ? dashboardData.value.stats.total_spots : 0
);

const lots = computed(() => dashboardData.value?.latest_lots || []);
const totalearnings = computed(() =>
  dashboardData.value ? dashboardData.value.stats.total_earnings : 0
);

const users = computed(() => dashboardData.value?.latest_users || []);
const recenthistory = computed(
  () => dashboardData.value?.latest_reservations || []
);

const form = ref({
  id: null,
  prime_location_name: "",
  address: "",
  pin_code: "",
  price: 0,
  number_of_spots: 0,
});

const recentUsers = computed(() => {
  return users.value.slice(0, 5);
});

// Methods
const loadDashboard = async () => {
  try {
    loading.value = true;
    const res = await fetchDashboardData();
    dashboardData.value = res.data;
  } catch (err) {
    error.value = err.response?.data?.msg || "Failed to load dashboard data";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const handleSubmit = async (data) => {
  try {
    loading.value = true;
    if (data.id) {
      await updateLot(data.id, data);
    } else {
      await createLot(data);
    }
    await loadDashboard();
    // resetForm();
  } catch (err) {
    error.value = err.response?.data?.msg || "Failed to save parking lot";
  } finally {
    loading.value = false;
  }
};

const resetForm = () => {
  form.value = {
    id: null,
    prime_location_name: "",
    address: "",
    pin_code: "",
    price: 0,
    number_of_spots: 0,
  };
};

// Lifecycle
onMounted(async () => {
  await auth.fetchUser();
  await loadDashboard();
});
</script>
<style scoped>
.admin-dashboard {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.main-content {
  flex: 1;
  padding-top: 1rem;
}

.card {
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  background-color: white;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.card-title {
  font-size: 1.05rem;
  color: #2c3e50;
}

.input-group-text {
  border-right: none;
}

.form-control-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.825rem;
}
</style>
