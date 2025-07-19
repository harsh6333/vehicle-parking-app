<template>
  <div class="admin-dashboard">
    <!-- Header -->
    <NavigationBar
      :navigation="[
        {
          title: 'Dashboard',
          link: '/user/dashboard',
          icon: 'bi bi-speedometer2',
        },
        {
          title: 'History',
          link: '/user/parking_history',
          icon: 'bi bi-clock-history',
        },
      ]"
    />
    <!-- Main Content -->
    <main class="main-content">
      <div class="container-fluid">
        <!-- Stats Cards -->
        <StatsOverview
          :lots="lots"
          :totalSpots="totalSpots"
          :users="users"
          :loading="loading"
        />

        <!-- Main Content -->
        <div class="row">
          <!-- Left Column -->
          <div class="col-lg-8">
            <!-- Lot Form -->
            <div class="card mb-4 border-0 shadow-sm">
              <div class="card-header bg-white border-0 py-3">
                <h5 class="mb-0">
                  <i class="bi bi-plus-circle me-2 text-primary"></i>
                  {{ form.id ? "Edit Parking Lot" : "Create New Parking Lot" }}
                </h5>
              </div>
              <div class="card-body">
                <LotForm :model-value="form" @submit="handleSubmit" />
              </div>
            </div>

            <!-- Parking Lots List -->
            <div class="card border-0 shadow-sm">
              <div class="card-header bg-white border-0 py-3">
                <div class="d-flex justify-content-between align-items-center">
                  <h5 class="mb-0">
                    <i class="bi bi-list-ul me-2 text-primary"></i>
                    All Parking Lots
                  </h5>
                  <input
                    type="date"
                    v-model="selectedDate"
                    class="form-control form-control-sm w-auto"
                    @change="loadLots"
                  />
                </div>
              </div>

              <div class="card-body">
                <div v-if="loading" class="text-center py-4">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
                <template v-else>
                  <div v-if="lots.length" class="row g-3">
                    <div v-for="lot in lots" :key="lot.id" class="col-md-6">
                      <LotCard
                        :lot="lot"
                        @edit="editLot"
                        @delete="deleteLot"
                        @viewSpots="loadSpots"
                      />
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
            <!-- Spots Panel -->
            <div class="card mb-4 border-0 shadow-sm">
              <div class="card-header bg-white border-0 py-3">
                <h5 class="mb-0">
                  <i class="bi bi-car-front me-2 text-primary"></i>
                  Parking Spots
                </h5>
              </div>
              <div>
                <div v-if="spotsLoading" class="text-center py-4">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
                <template v-else>
                  <SpotList
                    v-if="spots.length"
                    :spots="spots"
                    :date="selectedDate"
                    @dateChange="handleSpotDateChange"
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

            <!-- Users Panel -->
            <div class="card border-0 shadow-sm">
              <div class="card-header bg-white border-0 py-3">
                <h5 class="mb-0">
                  <i class="bi bi-people me-2 text-primary"></i>
                  Recent Users
                </h5>
              </div>
              <div class="card-body">
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
  fetchLots,
  deleteLotById,
  fetchSpots,
  fetchUsers,
  updateLot,
} from "@/services/adminService";

// Components
import StatsOverview from "@/components/AdminDashboard/StatsOverview.vue";
import LotForm from "@/components/AdminDashboard/LotForm.vue";
import LotCard from "@/components/AdminDashboard/LotCard.vue";
import SpotList from "@/components/AdminDashboard/SpotList.vue";
import UserTable from "@/components/AdminDashboard/UserTable.vue";
import EmptyState from "@/components/Common/EmptyState.vue";
import ErrorToast from "@/components/Common/ErrorToast.vue";
import NavigationBar from "@/components/Common/NavigationBar.vue";

// State
const auth = useAuthStore();
const error = ref(null);
const loading = ref(false);
const spotsLoading = ref(false);
const usersLoading = ref(false);

const lots = ref([]);
const spots = ref([]);
const users = ref([]);
const selectedLotId = ref(null);
const selectedDate = ref(new Date().toISOString().split("T")[0]);

const form = ref({
  id: null,
  prime_location_name: "",
  address: "",
  pin_code: "",
  price: 0,
  number_of_spots: 0,
});

// Computed
const totalSpots = computed(() => {
  return lots.value.reduce((sum, lot) => sum + lot.total_spots, 0);
});

const recentUsers = computed(() => {
  return users.value.slice(0, 5);
});

// Methods
const loadData = async () => {
  try {
    loading.value = true;
    await Promise.all([loadUsers(), loadLots()]);
  } catch (err) {
    error.value = "Failed to load dashboard data";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const loadUsers = async () => {
  try {
    usersLoading.value = true;
    const res = await fetchUsers();
    users.value = res.data;
  } catch (err) {
    error.value = "Failed to load users";
    throw err;
  } finally {
    usersLoading.value = false;
  }
};

const loadLots = async () => {
  try {
    loading.value = true;
    const res = await fetchLots();
    lots.value = res.data;
  } catch (err) {
    error.value = "Failed to load parking lots";
    throw err;
  } finally {
    loading.value = false;
  }
};

const loadSpots = async (lotId) => {
  try {
    spotsLoading.value = true;
    selectedLotId.value = lotId;
    const res = await fetchSpots(lotId, selectedDate.value);
    spots.value = res.data.spots;
  } catch (err) {
    error.value = "Failed to load parking spots";
    console.error(err);
  } finally {
    spotsLoading.value = false;
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
    await loadLots();
    resetForm();
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to save parking lot";
  } finally {
    loading.value = false;
  }
};

const editLot = (lot) => {
  form.value = { ...lot };
};

const deleteLot = async (id) => {
  if (confirm("Are you sure you want to delete this parking lot?")) {
    try {
      loading.value = true;
      await deleteLotById(id);
      await loadLots();
    } catch (err) {
      error.value = "Failed to delete parking lot";
    } finally {
      loading.value = false;
    }
  }
};

const handleSpotDateChange = async (newDate) => {
  selectedDate.value = newDate;
  if (selectedLotId.value) {
    await loadSpots(selectedLotId.value);
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
  await loadData();
});
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  min-height: 100vh;
  transition: padding 0.3s ease;
}
</style>
