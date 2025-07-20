<template>
  <div class="dashboard-container">
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
    <div class="container-fluid">
      <div class="row">
        <!-- Main Content -->
        <div class="w-100 main-content py-4">
          <!-- Page Header -->
          <div
            class="d-flex justify-content-between align-items-center mb-4 flex-wrap"
          >
            <div class="mb-2 mb-md-0">
              <h2 class="fw-bold mb-1">
                <i class="bi bi-clock-history text-primary me-2"></i>
                Reservation History
              </h2>
              <p class="text-muted mb-0">
                View your past and current parking reservations
              </p>
            </div>
            <div class="d-flex gap-2 flex-wrap">
              <div class="input-group" style="width: 200px">
                <span class="input-group-text">
                  <i class="bi bi-calendar"></i>
                </span>
                <input
                  type="date"
                  v-model="dateFilter"
                  class="form-control"
                  @change="loadHistory"
                />
              </div>
            </div>
          </div>

          <!-- Stats Cards -->
          <div class="row mb-4">
            <div class="col-md-4">
              <div class="card stat-card bg-white border-0 shadow-sm">
                <div class="card-body">
                  <div class="d-flex justify-content-between">
                    <div>
                      <h6 class="text-muted mb-2">Total Reservations</h6>
                      <h3 class="mb-0">{{ totalItems }}</h3>
                    </div>
                    <div
                      class="icon-circle bg-primary bg-opacity-10 text-primary"
                    >
                      <i class="bi bi-list-check"></i>
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
                      <h6 class="text-muted mb-2">Active Reservations</h6>
                      <h3 class="mb-0">{{ activeReservationsCount }}</h3>
                    </div>
                    <div
                      class="icon-circle bg-warning bg-opacity-10 text-warning"
                    >
                      <i class="bi bi-hourglass-split"></i>
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
                      <h6 class="text-muted mb-2">Total Spent</h6>
                      <h3 class="mb-0">₹{{ totalSpent.toFixed(2) }}</h3>
                    </div>
                    <div
                      class="icon-circle bg-success bg-opacity-10 text-success"
                    >
                      <i class="bi bi-cash-coin"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- History Table -->
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0 py-3">
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Your Reservations</h5>
                <div class="d-flex gap-2">
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="exportToCSV"
                  >
                    <i class="bi bi-download me-1"></i> Export
                  </button>
                </div>
              </div>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead class="table-light">
                    <tr>
                      <th>Date</th>
                      <th>Location</th>
                      <th>Spot</th>
                      <th>Time Slot</th>
                      <th>Duration</th>
                      <th>Status</th>
                      <th>Amount</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="entry in history" :key="entry.spot_id">
                      <td>
                        <div class="fw-semibold">
                          {{ formatDate(entry.reserved_at) }}
                        </div>
                        <small class="text-muted">{{
                          formatDay(entry.reserved_at)
                        }}</small>
                      </td>
                      <td>
                        <div>{{ entry.lot_name }}</div>
                        <small class="text-muted">{{ entry.address }}</small>
                      </td>
                      <td class="fw-semibold">#{{ entry.spot_id }}</td>
                      <td>
                        <div class="d-flex flex-column">
                          <span>{{ formatTime(entry.reserved_at) }}</span>
                          <span class="text-muted small">to</span>
                          <span>{{ formatTime(entry.reserved_till) }}</span>
                        </div>
                      </td>
                      <td class="fw-semibold">
                        {{
                          calculateDuration(
                            entry.reserved_at,
                            entry.reserved_till
                          )
                        }}h
                      </td>
                      <td>
                        <span
                          class="badge rounded-pill"
                          :class="getStatusClass(entry)"
                        >
                          <i :class="getStatusIcon(entry)" class="me-1"></i>
                          {{ getStatusText(entry) }}
                        </span>
                      </td>
                      <td class="fw-semibold">₹{{ calculateAmount(entry) }}</td>
                      <td>
                        <button
                          v-if="!entry.leaving_timestamp"
                          class="btn btn-sm btn-outline-danger"
                          @click="cancelReservationfunc(entry.id)"
                          title="Cancel Reservation"
                        >
                          <i class="bi bi-x-circle"></i>
                        </button>
                        <button
                          v-else
                          class="btn btn-sm btn-outline-secondary"
                          disabled
                          title="Completed"
                        >
                          <i class="bi bi-check-circle"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Empty State -->
              <div v-if="history.length === 0" class="text-center py-5">
                <i
                  class="bi bi-clock-history text-muted"
                  style="font-size: 3rem"
                ></i>
                <h5 class="mt-3">No reservations found</h5>
                <p class="text-muted">
                  You don't have any reservation history yet
                </p>
                <router-link to="/user/dashboard" class="btn btn-primary mt-2">
                  <i class="bi bi-car-front me-1"></i> Find Parking
                </router-link>
              </div>

              <!-- Pagination -->
              <div
                v-if="history.length > 0"
                class="d-flex justify-content-between align-items-center p-3 border-top"
              >
                <div class="text-muted small">
                  Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to
                  {{ Math.min(currentPage * itemsPerPage, totalItems) }} of
                  {{ totalItems }} entries
                </div>
                <nav>
                  <ul class="pagination mb-0">
                    <li
                      class="page-item"
                      :class="{ disabled: currentPage === 1 }"
                    >
                      <button class="page-link" @click="prevPage">
                        <i class="bi bi-chevron-left"></i>
                      </button>
                    </li>
                    <li
                      v-for="page in pages"
                      :key="page"
                      class="page-item"
                      :class="{ active: page === currentPage }"
                    >
                      <button class="page-link" @click="goToPage(page)">
                        {{ page }}
                      </button>
                    </li>
                    <li
                      class="page-item"
                      :class="{ disabled: currentPage === totalPages }"
                    >
                      <button class="page-link" @click="nextPage">
                        <i class="bi bi-chevron-right"></i>
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { getHistory, releaseSpot } from "@/services/userService";
import NavigationBar from "@/components/Common/NavigationBar.vue";

const history = ref([]);
const dateFilter = ref(new Date().toISOString().split("T")[0]);
const currentPage = ref(1);
const itemsPerPage = 10;
const totalItems = ref(0);
const loading = ref(false);

// Computed properties
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

  for (let i = start; i <= end; i++) {
    range.push(i);
  }
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
  } catch (error) {
    console.error("Error loading history:", error);
  } finally {
    loading.value = false;
  }
};

const formatDate = (timestamp) => {
  if (!timestamp) return "-";
  return new Date(timestamp).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
};

const formatDay = (timestamp) => {
  if (!timestamp) return "";
  return new Date(timestamp).toLocaleDateString("en-IN", {
    weekday: "short",
  });
};

const formatTime = (timestamp) => {
  if (!timestamp) return "-";
  return new Date(timestamp).toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
};

const calculateDuration = (start, end) => {
  if (!start || !end) return 0;

  const diff = new Date(end) - new Date(start);
  // console.log(start, end, (diff / (1000 * 60 * 60)).toFixed(1));
  return (diff / (1000 * 60 * 60)).toFixed(1);
};

const calculateAmount = (entry) => {
  const duration = calculateDuration(
    entry.reserved_at,
    entry.leaving_timestamp || entry.reserved_till
  );
  console.log(duration, entry);

  return (duration * entry.hourlyrate).toFixed(2);
};

const getStatusClass = (entry) => {
  if (entry.leaving_timestamp) return "bg-success bg-opacity-10 text-success";
  if (entry.parking_timestamp) return "bg-warning bg-opacity-10 text-warning";
  return "bg-info bg-opacity-10 text-info";
};

const getStatusIcon = (entry) => {
  if (entry.leaving_timestamp) return "bi bi-check-circle";
  if (entry.parking_timestamp) return "bi bi-car-front";
  return "bi bi-hourglass";
};

const getStatusText = (entry) => {
  if (entry.leaving_timestamp) return "Completed";
  if (entry.parking_timestamp) return "Occupied";
  return "Reserved";
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

const cancelReservationfunc = async (id) => {
  if (confirm("Are you sure you want to cancel this reservation?")) {
    try {
      await releaseSpot(id);
      await loadHistory();
    } catch (error) {
      console.error("Error cancelling reservation:", error);
    }
  }
};

const exportToCSV = () => {
  // Implement CSV export functionality
  console.log("Exporting to CSV...");
};

// Lifecycle
onMounted(loadHistory);
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.sidebar {
  min-height: calc(100vh - 56px);
  position: sticky;
  top: 56px;
  z-index: 1000;
}

.main-content {
  padding: 1.5rem;
}

.stat-card {
  border-radius: 0.75rem;
  transition: transform 0.2s;
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

.table th {
  background-color: #f8f9fa;
  position: sticky;
  top: 0;
  z-index: 10;
  white-space: nowrap;
}

.table-responsive {
  max-height: calc(100vh - 400px);
  overflow-y: auto;
}

.page-item.active .page-link {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.page-link {
  color: #0d6efd;
}

.nav-link.active {
  background-color: rgba(13, 110, 253, 0.1);
  color: #0d6efd;
  font-weight: 500;
}
</style>
