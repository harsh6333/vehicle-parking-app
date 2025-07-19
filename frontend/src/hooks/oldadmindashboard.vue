<template>
  <div class="admin-dashboard">
    <!-- Sidebar -->
    <aside class="sidebar bg-dark text-white">
      <div class="d-flex flex-column h-100">
        <div class="sidebar-header p-3 border-bottom border-secondary">
          <h4 class="mb-0 d-flex align-items-center gap-2">
            <i class="bi bi-car-front-fill text-primary"></i>
            <span>Parking Admin</span>
          </h4>
        </div>

        <nav class="nav flex-column flex-grow-1 p-3">
          <router-link
            to="/admin/dashboard"
            class="nav-link text-white d-flex align-items-center gap-2 py-2 active"
          >
            <i class="bi bi-speedometer2"></i>
            Dashboard
          </router-link>

          <router-link
            to="/users"
            class="nav-link text-white d-flex align-items-center gap-2 py-2"
          >
            <i class="bi bi-people"></i>
            Users
          </router-link>
        </nav>

        <div class="sidebar-footer p-3 border-top border-secondary">
          <div class="d-flex align-items-center gap-2">
            <div
              class="avatar bg-primary text-white rounded-circle d-flex align-items-center justify-content-center"
              style="width: 36px; height: 36px"
            >
              {{ userInitials.initials }}
            </div>
            <div>
              <div class="fw-semibold">{{ userInitials.username }}</div>
              <small class="text-muted">Administrator</small>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content bg-light">
      <div class="container-fluid py-4">
        <!-- Header -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <div>
            <h2 class="fw-bold mb-1">Parking Lot Management</h2>
            <p class="text-muted mb-0">Create and manage parking lots</p>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-outline-secondary">
              <i class="bi bi-question-circle me-1"></i> Help
            </button>
          </div>
        </div>

        <!-- Stats Cards -->
        <div class="row mb-4">
          <div class="col-md-4">
            <div class="card stat-card bg-white border-0 shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between">
                  <div>
                    <h6 class="text-muted mb-2">Total Lots</h6>
                    <h3 class="mb-0">{{ lots.length }}</h3>
                  </div>
                  <div
                    class="icon-circle bg-primary bg-opacity-10 text-primary"
                  >
                    <i class="bi bi-p-square"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card stat-card bg-white border-0 shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between">
                  <div>
                    <h6 class="text-muted mb-2">Total Spots</h6>
                    <h3 class="mb-0">{{ totalSpots }}</h3>
                  </div>
                  <div
                    class="icon-circle bg-success bg-opacity-10 text-success"
                  >
                    <i class="bi bi-car-front"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card stat-card bg-white border-0 shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between">
                  <div>
                    <h6 class="text-muted mb-2">Registered Users</h6>
                    <h3 class="mb-0">{{ users.length }}</h3>
                  </div>
                  <div class="icon-circle bg-info bg-opacity-10 text-info">
                    <i class="bi bi-people"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

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
                <h5 class="mb-0">
                  <i class="bi bi-list-ul me-2 text-primary"></i>
                  All Parking Lots
                </h5>
              </div>

              <div class="card-body">
                <div class="mb-4 d-flex justify-content-end">
                  <input
                    type="date"
                    v-model="selectedDate"
                    class="form-control w-auto"
                    @change="loadLots"
                  />
                </div>
                <div v-if="lots.length" class="row g-3">
                  <div v-for="lot in lots" :key="lot.id" class="col-md-6">
                    <LotCard
                      :lot="lot"
                      @editLot="editLot"
                      @deleteLot="deleteLot"
                      @viewSpots="loadSpots"
                    />
                  </div>
                </div>
                <div v-else class="text-center py-5">
                  <i
                    class="bi bi-p-square text-muted"
                    style="font-size: 3rem"
                  ></i>
                  <p class="text-muted mt-3">No parking lots available</p>
                  <button class="btn btn-primary" @click="resetForm">
                    <i class="bi bi-plus-circle me-1"></i> Add First Lot
                  </button>
                </div>
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
                <div
                  v-if="spots.length"
                  class="mb-3 d-flex justify-content-end"
                >
                  <!-- <input
                    type="date"
                    v-model="selectedDate"
                    class="form-control w-auto"
                    @change="() => selectedLotId && loadSpots(selectedLotId)"
                  /> -->
                  <SpotList
                    :spots="spots"
                    :date="selectedDate"
                    @dateChange="handleSpotDateChange"
                  />
                </div>

                <div v-else class="text-center py-4">
                  <i
                    class="bi bi-car-front text-muted"
                    style="font-size: 2rem"
                  ></i>
                  <p class="text-muted mt-2">
                    Select a parking lot to view spots
                  </p>
                </div>
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
                <UserTable :users="recentUsers" v-if="users.length" />
                <div v-else class="text-center py-4">
                  <i
                    class="bi bi-person-slash text-muted"
                    style="font-size: 2rem"
                  ></i>
                  <p class="text-muted mt-2">No users found</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import LotForm from "@/components/AdminDashboard/LotForm.vue";
import LotCard from "@/components/AdminDashboard/LotCard.vue";
import SpotList from "@/components/AdminDashboard/SpotList.vue";
import UserTable from "@/components/AdminDashboard/UserTable.vue";
import { useAuthStore } from "@/store/auth";
import {
  createLot,
  fetchLots,
  deleteLotById,
  fetchSpots,
  fetchUsers,
  updateLot,
} from "@/services/adminService";

// Data
const lots = ref([]);
const spots = ref([]);
const users = ref([]);

const auth = useAuthStore();
onMounted(async () => {
  await auth.fetchUser();
  await loadData();
});

const error = ref(null);
const form = ref({
  prime_location_name: "",
  address: "",
  pin_code: "",
  price: 0,
  number_of_spots: 0,
});

const userInitials = computed(() => {
  console.log(auth.user);
  return {
    username: auth?.user?.username,
    initials: auth.user?.username?.substring(0, 2).toUpperCase() || "",
  };
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
    error.value = null;
    const userRes = await fetchUsers();
    users.value = userRes.data;
  } catch (err) {
    error.value = "Failed to load user data. Please try again later.";
  }
};

const selectedDate = ref(new Date().toISOString().split("T")[0]);

const loadLots = async () => {
  try {
    const res = await fetchLots();
    lots.value = res.data;
  } catch (err) {
    error.value = "Failed to load lots";
  }
};
onMounted(async () => {
  await auth.fetchUser();
  await loadData();
  await loadLots(); // Load lots separately with selected date
});
const handleSubmit = async (data) => {
  try {
    if (data.id) {
      console.log(data.id);
      await updateLot(data.id, data);
    } else {
      await createLot(data);
    }
    await loadData();
    resetForm();
  } catch (err) {
    error.value = err.response?.data?.message || "Could not save parking lot.";
  }
};

const editLot = (lot) => {
  form.value = { ...lot };
};

const deleteLot = async (id) => {
  if (confirm("Are you sure you want to delete this parking lot?")) {
    await deleteLotById(id);
    await loadData();
  }
};
const selectedLotId = ref(null);

const handleSpotDateChange = async (newDate) => {
  selectedDate.value = newDate;
  if (selectedLotId.value) {
    await loadSpots(selectedLotId.value);
  }
};

const loadSpots = async (lotId) => {
  selectedLotId.value = lotId;
  try {
    const res = await fetchSpots(lotId, selectedDate.value);
    spots.value = res.data.spots;
  } catch (err) {
    console.error("Failed to load spots", err);
  }
};

const resetForm = () => {
  form.value = {
    prime_location_name: "",
    address: "",
    pin_code: "",
    price: 0,
    number_of_spots: 0,
  };
};

// Lifecycle
onMounted(loadData);
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: 280px;
  transition: all 0.3s;
}

.nav-link {
  border-radius: 6px;
  transition: all 0.2s;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.active {
  background-color: rgba(13, 110, 253, 0.2);
  color: #0d6efd !important;
}

/* Main Content */
.main-content {
  flex: 1;
  overflow-y: auto;
  min-height: 100vh;
}

/* Stats Cards */
.stat-card {
  border-radius: 10px;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-3px);
}

.icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

/* Responsive */
@media (max-width: 992px) {
  .sidebar {
    width: 80px;
    overflow: hidden;
  }

  .sidebar-header h4 span,
  .nav-link span {
    display: none;
  }

  .sidebar-footer > div > div {
    display: none;
  }

  .avatar {
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    z-index: 1000;
    height: 100vh;
    transform: translateX(-100%);
  }

  .sidebar.show {
    transform: translateX(0);
  }
}
</style>
